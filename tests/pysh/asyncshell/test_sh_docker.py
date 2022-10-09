from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

import pytest

from pysh.asyncshell import (
    DEFAULT_CHECK_EXITCODE,
    DEFAULT_STDERR_LOG_LEVEL,
    DEFAULT_STDOUT_LOG_LEVEL,
    ProcessInfo,
    sh_docker,
)


@pytest.mark.parametrize(
    "sh_docker_kwargs, docker_run_kwargs",
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
                "image": "pysh/echo",
                "args": ["Hello World!"],
                "detached": False,
                "cleanup": True,
                "user": None,
                "entrypoint": None,
                "volumes": {},
                "network": None,
                "stdout_log_level": 9000,
                "stderr_log_level": -9000,
                "check_exitcode": False,
            },
        ),
        (
            {
                "image": "pysh/echo",
                "args": ["Hello World!"],
            },
            {
                "image": "pysh/echo",
                "args": ["Hello World!"],
                "detached": False,
                "cleanup": True,
                "user": None,
                "entrypoint": None,
                "volumes": {},
                "network": None,
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/ls",
                "args": [Path("dir")],
            },
            {
                "image": "pysh/ls",
                "args": ["/mnt/0/dir"],
                "detached": False,
                "cleanup": True,
                "user": None,
                "entrypoint": None,
                "volumes": {Path("dir"): Path("/mnt/0/dir")},
                "network": None,
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/cat",
                "args": [Path("chp0.txt"), Path("chp1.txt")],
            },
            {
                "image": "pysh/cat",
                "args": ["/mnt/0/chp0.txt", "/mnt/1/chp1.txt"],
                "detached": False,
                "cleanup": True,
                "user": None,
                "entrypoint": None,
                "volumes": {
                    Path("chp0.txt"): Path("/mnt/0/chp0.txt"),
                    Path("chp1.txt"): Path("/mnt/1/chp1.txt"),
                },
                "network": None,
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
        (
            {
                "image": "pysh/cat",
                "args": [Path("story.txt"), Path("story.txt")],
            },
            {
                "image": "pysh/cat",
                "args": ["/mnt/0/story.txt", "/mnt/0/story.txt"],
                "detached": False,
                "cleanup": True,
                "user": None,
                "entrypoint": None,
                "volumes": {
                    Path("story.txt"): Path("/mnt/0/story.txt"),
                },
                "network": None,
                "stdout_log_level": DEFAULT_STDOUT_LOG_LEVEL,
                "stderr_log_level": DEFAULT_STDERR_LOG_LEVEL,
                "check_exitcode": DEFAULT_CHECK_EXITCODE,
            },
        ),
    ],
)
@pytest.mark.asyncio
@patch("pysh.asyncshell.docker_run")
async def test_pysh_asyncshell_sh_called(
    docker_run_mock: MagicMock,
    sh_docker_kwargs: Dict[str, Any],
    docker_run_kwargs: Dict[str, Any],
) -> None:
    # Arrange
    docker_run_mock.return_value = ProcessInfo(0, "stdout", "stderr")

    # Act
    await sh_docker(**sh_docker_kwargs)

    # Assert
    assert docker_run_mock.call_args_list == [call(**docker_run_kwargs)]


@pytest.mark.asyncio
@patch("pysh.asyncshell.docker_run")
async def test_return_value(
    sh_mock: MagicMock,
) -> None:
    # Arrange
    sh_mock.return_value = ProcessInfo(9000, "Hello World!", "ERROR")

    # Act
    process_info = await sh_docker(
        image="pysh/test:latest",
        args=["echo", "Hello World!"],
    )

    # Assert
    assert process_info == ProcessInfo(9000, "Hello World!", "ERROR")
