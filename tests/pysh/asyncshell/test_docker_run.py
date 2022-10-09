from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

import pytest

from pysh.asyncshell import (
    DEFAULT_CHECK_EXITCODE,
    DEFAULT_STDERR_LOG_LEVEL,
    DEFAULT_STDOUT_LOG_LEVEL,
    DOCKER_USER_ME,
    ProcessInfo,
    docker_run,
)


@pytest.mark.parametrize(
    "docker_run_kwargs, sh_kwargs",
    [
        (
            {
                "image": "pysh/echo",
                "args": ["Hello World!"],
                "stdout_log_level": 9000,
                "stderr_log_level": -9000,
                "check_exitcode": False,
            },
            {
                "args": [
                    "docker",
                    "run",
                    "-d=false",
                    "--rm=true",
                    "pysh/echo",
                    "Hello World!",
                ],
                "stdout_log_level": 9000,
                "stderr_log_level": -9000,
                "check_exitcode": False,
            },
        ),
        (
            {
                "image": "pysh/echo",
                "args": ["echo", "Hello World!"],
                "user": DOCKER_USER_ME,
                "entrypoint": "/bin/bash",
            },
            {
                "args": [
                    "docker",
                    "run",
                    "-d=false",
                    "--rm=true",
                    "--user",
                    DOCKER_USER_ME,
                    "--entrypoint",
                    "/bin/bash",
                    "pysh/echo",
                    "echo",
                    "Hello World!",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/ping",
                "args": ["google.com"],
                "network": "host",
            },
            {
                "args": [
                    "docker",
                    "run",
                    "-d=false",
                    "--rm=true",
                    "--network",
                    "host",
                    "pysh/ping",
                    "google.com",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/ls",
                "args": ["/mnt/dir"],
                "volumes": {
                    Path("."): Path("/mnt/dir"),
                },
            },
            {
                "args": [
                    "docker",
                    "run",
                    "-d=false",
                    "--rm=true",
                    "-v",
                    f"{Path('.').resolve()}:{Path('/mnt/dir').as_posix()}",
                    "pysh/ls",
                    "/mnt/dir",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/cat",
                "args": ["/mnt/chp0.txt", "/mnt/chp1.txt"],
                "volumes": {
                    Path("chp0.txt"): Path("/mnt/chp0.txt"),
                    Path("chp1.txt"): Path("/mnt/chp1.txt"),
                },
            },
            {
                "args": [
                    "docker",
                    "run",
                    "-d=false",
                    "--rm=true",
                    "-v",
                    f"{Path('chp0.txt').resolve()}:{Path('/mnt/chp0.txt').as_posix()}",
                    "-v",
                    f"{Path('chp1.txt').resolve()}:{Path('/mnt/chp1.txt').as_posix()}",
                    "pysh/cat",
                    "/mnt/chp0.txt",
                    "/mnt/chp1.txt",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
    ],
)
@pytest.mark.asyncio
@patch("pysh.asyncshell.sh")
async def test_pysh_asyncshell_sh_called(
    sh_mock: MagicMock,
    docker_run_kwargs: Dict[str, Any],
    sh_kwargs: Dict[str, Any],
) -> None:
    # Arrange
    sh_mock.return_value = ProcessInfo(0, "stdout", "stderr")

    # Act
    await docker_run(**docker_run_kwargs)

    # Assert
    assert sh_mock.call_args_list == [call(**sh_kwargs)]


@pytest.mark.asyncio
@patch("pysh.asyncshell.sh")
async def test_return_value(
    sh_mock: MagicMock,
) -> None:
    # Arrange
    sh_mock.return_value = ProcessInfo(9000, "Hello World!", "ERROR")

    # Act
    process_info = await docker_run(
        image="pysh/test:latest",
        args=["echo", "Hello World!"],
    )

    # Assert
    assert process_info == ProcessInfo(9000, "Hello World!", "ERROR")
