import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from . import asyncshell
from .asyncshell import DOCKER_USER_ME  # noqa: F401
from .asyncshell import DOCKER_USER_ROOT  # noqa: F401
from .asyncshell import (
    DEFAULT_CHECK_EXITCODE,
    DEFAULT_STDERR_LOG_LEVEL,
    DEFAULT_STDOUT_LOG_LEVEL,
    ProcessInfo,
)


def sh(
    args: List[str],
    stdout_log_level: int = DEFAULT_STDOUT_LOG_LEVEL,
    stderr_log_level: int = DEFAULT_STDERR_LOG_LEVEL,
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    return asyncio.run(
        asyncshell.sh(
            args=args,
            stdout_log_level=stdout_log_level,
            stderr_log_level=stderr_log_level,
            check_exitcode=check_exitcode,
        )
    )


def docker_run(
    image: str,
    args: List[str],
    user: Optional[str] = None,
    entrypoint: Optional[str] = None,
    volumes: Dict[Path, Path] = {},
    stdout_log_level: int = DEFAULT_STDOUT_LOG_LEVEL,
    stderr_log_level: int = DEFAULT_STDERR_LOG_LEVEL,
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    return asyncio.run(
        asyncshell.docker_run(
            image=image,
            args=args,
            user=user,
            entrypoint=entrypoint,
            volumes=volumes,
            stdout_log_level=stdout_log_level,
            stderr_log_level=stderr_log_level,
            check_exitcode=check_exitcode,
        )
    )
