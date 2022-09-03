import asyncio
from pathlib import Path
from typing import Dict, List

from . import asyncshell
from .asyncshell import DEFAULT_CHECK_EXITCODE, ProcessInfo


def sh(
    args: List[str],
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    return asyncio.run(
        asyncshell.sh(
            args,
            check_exitcode,
        )
    )


def docker_run(
    image: str,
    args: List[str],
    volumes: Dict[Path, Path] = {},
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    return asyncio.run(
        asyncshell.docker_run(
            image,
            args,
            volumes,
            check_exitcode,
        )
    )
