import asyncio
import logging
import os
from asyncio import StreamReader, subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, List, NamedTuple, Optional

# Defaults
DEFAULT_STDOUT_LOG_LEVEL = logging.INFO
DEFAULT_STDERR_LOG_LEVEL = logging.ERROR
DEFAULT_CHECK_EXITCODE = True

# Constants
DOCKER_USER_ME = f"{os.getuid()}:{os.getgid()}"
DOCKER_USER_ROOT = "0:0"


class ProcessInfo(NamedTuple):
    exitcode: int
    stdout: str
    stderr: str


def _cmd(args: List[str]) -> str:
    # Wrap args containing whitespace with quotes
    args = [f'"{arg}"' if " " in arg else arg for arg in args]
    return " ".join(args)


async def _read_stream(stream: Optional[StreamReader], loglevel: int) -> str:
    lines: List[str] = []

    if stream is not None:
        while bdata := await stream.readline():
            line = bdata.decode().rstrip("\n")  # Decode and remove trailing newline

            lines.append(line)
            logging.log(loglevel, line)

    return "\n".join(lines)


async def sh(
    args: List[str],
    stdout_log_level: int = DEFAULT_STDOUT_LOG_LEVEL,
    stderr_log_level: int = DEFAULT_STDERR_LOG_LEVEL,
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    cmd = _cmd(args)
    process = await subprocess.create_subprocess_shell(
        cmd=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    exitcode, stdout, stderr = await asyncio.gather(
        process.wait(),
        _read_stream(process.stdout, stdout_log_level),
        _read_stream(process.stderr, stderr_log_level),
    )

    if check_exitcode and exitcode != 0:
        raise CalledProcessError(exitcode, cmd, stdout, stderr)

    return ProcessInfo(exitcode, stdout, stderr)


async def docker_run(
    image: str,
    args: List[str],
    user: Optional[str] = None,
    entrypoint: Optional[str] = None,
    volumes: Dict[Path, Path] = {},
    stdout_log_level: int = DEFAULT_STDOUT_LOG_LEVEL,
    stderr_log_level: int = DEFAULT_STDERR_LOG_LEVEL,
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    cmd = ["docker", "run"]

    if user:
        cmd += ["--user", user]

    if entrypoint:
        cmd += ["--entrypoint", entrypoint]

    for src, dst in volumes.items():
        cmd += ["-v", f"{src.resolve()}:{dst.as_posix()}"]

    cmd += [image, *args]

    return await sh(
        cmd,
        stdout_log_level=stdout_log_level,
        stderr_log_level=stderr_log_level,
        check_exitcode=check_exitcode,
    )
