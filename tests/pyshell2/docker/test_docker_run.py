import inspect
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

from pyshell2 import asyncdocker
from pyshell2.docker import docker_run
from pyshell2.shell import ProcessInfo


def test_signature() -> None:
    assert inspect.signature(docker_run) == inspect.signature(asyncdocker.docker_run)


def test_docstring() -> None:
    assert inspect.getdoc(docker_run) == inspect.getdoc(asyncdocker.docker_run)


@patch("pyshell2.asyncdocker.docker_run")
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


@patch("pyshell2.asyncdocker.docker_run")
def test_return_value(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    asyncshell_sh_mock.return_value = ProcessInfo(292, "stdout", "stderr")

    # Act
    process_info = docker_run("docker-image", [])

    # Assert
    assert process_info == ProcessInfo(292, "stdout", "stderr")
