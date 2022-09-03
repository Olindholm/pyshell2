import logging
import asyncio
from typing import List
from asyncio import subprocess, StreamReader
from subprocess import CalledProcessError


async def sh(args: List[str], check_exitcode=True):
    cmd = " ".join(args)
    process = await subprocess.create_subprocess_shell(
        cmd=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    async def read_stream(stream: StreamReader, loglevel: int):
        lines: List[str] = []

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

    return exitcode, stdout, stderr
