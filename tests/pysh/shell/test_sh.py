import inspect
from typing import Any, Dict
from unittest.mock import MagicMock, call, patch

from pysh import asyncshell
from pysh.shell import ProcessInfo, sh


def test_signature() -> None:
    assert inspect.signature(sh) == inspect.signature(asyncshell.sh)


@patch("pysh.shell.asyncshell.sh")
def test_kwargs(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    signature = inspect.signature(sh)
    params: Dict[str, Any] = {
        param: index for index, param in enumerate(signature.parameters)
    }

    # Act
    sh(**params)

    # Assert
    assert asyncshell_sh_mock.call_args_list == [call(**params)]


@patch("pysh.shell.asyncshell.sh")
def test_return_value(asyncshell_sh_mock: MagicMock) -> None:
    # Arrange
    asyncshell_sh_mock.return_value = ProcessInfo("exitcode", "stdout", "stderr")

    # Act
    process_info = sh([])

    # Assert
    assert process_info == ProcessInfo("exitcode", "stdout", "stderr")
