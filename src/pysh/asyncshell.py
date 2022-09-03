import asyncio
import logging
from asyncio import StreamReader, subprocess
from collections import namedtuple
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, List, Optional, Tuple

ProcessInfo = namedtuple("ProcessInfo", "exitcode stdout stderr")


DEFAULT_CHECK_EXITCODE = True


async def sh(
    args: List[str],
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    cmd = " ".join(args)
    process = await subprocess.create_subprocess_shell(
        cmd=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    async def read_stream(stream: Optional[StreamReader], loglevel: int) -> str:
        lines: List[str] = []

        if stream is not None:
            while bdata := await stream.readline():
                line = bdata.decode().rstrip("\n")  # Decode and remove trailing newline

                lines.append(line)
                logging.log(loglevel, line)

        return "\n".join(lines)

    exitcode, stdout, stderr = await asyncio.gather(
        process.wait(),
        read_stream(process.stdout, logging.INFO),
        read_stream(process.stderr, logging.ERROR),
    )

    if check_exitcode and exitcode != 0:
        raise CalledProcessError(exitcode, cmd, stdout, stderr)

    return ProcessInfo(exitcode, stdout, stderr)


async def docker_run(
    image: str,
    args: List[str],
    volumes: Dict[Path, Path] = {},
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    cmd = [
        "docker run",
        *[f"-v {src.resolve()}:{dst.as_posix()}" for src, dst in volumes.items()],
        image,
        *args,
    ]
    return await sh(cmd, check_exitcode=check_exitcode)
