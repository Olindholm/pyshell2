import inspect
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

from pyshell2 import asyncshell
from pyshell2.shell import ProcessInfo, sh_docker


def test_signature() -> None:
    assert inspect.signature(sh_docker) == inspect.signature(asyncshell.sh_docker)


def test_docstring() -> None:
    assert inspect.getdoc(sh_docker) == inspect.getdoc(asyncshell.sh_docker)


@patch("pyshell2.asyncshell.sh_docker")
def test_kwargs(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    signature = inspect.signature(sh_docker)
    params: Dict[str, Any] = {
        param: index for index, param in enumerate(signature.parameters)
    }

    # Act
    sh_docker(**params)

    # Assert
    assert asyncshell_sh_mock.call_args_list == [call(**params)]


@patch("pyshell2.asyncshell.sh_docker")
def test_return_value(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    asyncshell_sh_mock.return_value = ProcessInfo(292, "stdout", "stderr")

    # Act
    process_info = sh_docker("docker-image", [])

    # Assert
    assert process_info == ProcessInfo(292, "stdout", "stderr")
