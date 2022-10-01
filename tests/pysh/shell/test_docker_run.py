import inspect
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

from pysh import asyncshell
from pysh.shell import ProcessInfo, docker_run


def test_signature() -> None:
    assert inspect.signature(docker_run) == inspect.signature(asyncshell.docker_run)


@patch("pysh.shell.asyncshell.docker_run")
def test_kwargs(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    signature = inspect.signature(docker_run)
    params: Dict[str, Any] = {
        param: index for index, param in enumerate(signature.parameters)
    }

    # Act
    docker_run(**params)

    # Assert
    assert asyncshell_sh_mock.call_args_list == [call(**params)]


@patch("pysh.shell.asyncshell.docker_run")
def test_return_value(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    asyncshell_sh_mock.return_value = ProcessInfo(292, "stdout", "stderr")

    # Act
    process_info = docker_run("docker-image", [])

    # Assert
    assert process_info == ProcessInfo(292, "stdout", "stderr")
