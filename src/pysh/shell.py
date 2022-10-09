import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from . import asyncshell
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
    """Runs a shell command.

    Args:
        args: Command arguments to run in shell. Arguments containing spaces will be
            wrapped in quotes.'
        stdout_log_level: Log level of the stdout of the shell command.
        stderr_log_level: Log level of the stderr of the shell command.
        check_exitcode: Whether to check if the exit code is zero or not. If true and
            exitcode is non-zero, a CalledProcessError will be raised.
    Returns:
        A ProcessInfo containing the exitcode, stdout, and stderr from the command.
    Raises:
        CalledProcessError: If the shell command exited with a non-zero exitcode and
            check_exitcode is true.
    """
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
    detached: bool = False,
    cleanup: bool = True,
    user: Optional[str] = None,
    entrypoint: Optional[str] = None,
    volumes: Dict[Path, Path] = None,
    network: Optional[str] = None,
    stdout_log_level: int = DEFAULT_STDOUT_LOG_LEVEL,
    stderr_log_level: int = DEFAULT_STDERR_LOG_LEVEL,
    check_exitcode: bool = DEFAULT_CHECK_EXITCODE,
) -> ProcessInfo:
    """Runs a docker run command."""
    return asyncio.run(
        asyncshell.docker_run(
            image=image,
            args=args,
            detached=detached,
            cleanup=cleanup,
            user=user,
            entrypoint=entrypoint,
            volumes=volumes,
            network=network,
            stdout_log_level=stdout_log_level,
            stderr_log_level=stderr_log_level,
            check_exitcode=check_exitcode,
        )
    )
