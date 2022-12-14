from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

import pytest

from pyshell2.asyncdocker import DOCKER_USER_ME, docker_run
from pyshell2.asyncshell import (
    DEFAULT_CHECK_EXITCODE,
    DEFAULT_STDERR_LOG_LEVEL,
    DEFAULT_STDOUT_LOG_LEVEL,
    ProcessInfo,
)

EQ = '\\"'  # Esacped quote


@pytest.mark.parametrize(
    "docker_run_kwargs, sh_kwargs",
    [
        (
            {
                "image": "pyshell2/echo",
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
                    "pyshell2/echo",
                    "Hello World!",
                ],
                "stdout_log_level": 9000,
                "stderr_log_level": -9000,
                "check_exitcode": False,
            },
        ),
        (
            {
                "image": "pyshell2/echo",
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
                    "pyshell2/echo",
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
                "image": "pyshell2/ping",
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
                    "pyshell2/ping",
                    "google.com",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pyshell2/ls",
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
                    "--mount",
                    ",".join(
                        [
                            "type=bind",
                            f"{EQ}src={Path('.').resolve()}{EQ}",
                            f"{EQ}dst={Path('/mnt/dir').resolve()}{EQ}",
                        ]
                    ),
                    "pyshell2/ls",
                    "/mnt/dir",
                ],
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pyshell2/cat",
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
                    "--mount",
                    ",".join(
                        [
                            "type=bind",
                            f"{EQ}src={Path('chp0.txt').resolve()}{EQ}",
                            f"{EQ}dst={Path('/mnt/chp0.txt').resolve()}{EQ}",
                        ]
                    ),
                    "--mount",
                    ",".join(
                        [
                            "type=bind",
                            f"{EQ}src={Path('chp1.txt').resolve()}{EQ}",
                            f"{EQ}dst={Path('/mnt/chp1.txt').resolve()}{EQ}",
                        ]
                    ),
                    "pyshell2/cat",
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
@patch("pyshell2.asyncdocker.sh")
async def test_pyshell2_asyncshell_sh_called(
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
@patch("pyshell2.asyncdocker.sh")
async def test_return_value(
    sh_mock: MagicMock,
) -> None:
    # Arrange
    sh_mock.return_value = ProcessInfo(9000, "Hello World!", "ERROR")

    # Act
    process_info = await docker_run(
        image="pyshell2/test:latest",
        args=["echo", "Hello World!"],
    )

    # Assert
    assert process_info == ProcessInfo(9000, "Hello World!", "ERROR")
