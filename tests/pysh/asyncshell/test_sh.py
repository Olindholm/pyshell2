import pytest
import logging
from typing import List
from subprocess import CalledProcessError
from asyncio import subprocess, StreamReader
from unittest.mock import AsyncMock, MagicMock, patch, call

from pysh.asyncshell import sh

# TODO
# test_check_exitcode


def stream(lines: List[str] = []) -> StreamReader:
    stream = StreamReader()
    if lines:
        stream.feed_data("\n".join(lines).encode())
    stream.feed_eof()

    return stream


def process_mock(
    exitcode: int,
    stdout: List[str] = [],
    stderr: List[str] = [],
) -> MagicMock:
    process = MagicMock()
    process.wait = AsyncMock(return_value=exitcode)
    process.stdout = stream(stdout)
    process.stderr = stream(stderr)
    return process


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_create_subprocess_shell_called(
    create_subprocess_shell: MagicMock,
) -> None:
    # Arrange
    create_subprocess_shell.return_value = process_mock(0)

    # Act
    await sh(["ls", "-a"])

    # Assert
    assert create_subprocess_shell.call_args_list == [
        call(
            cmd="ls -a",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    ]


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_stdout(
    create_subprocess_shell: MagicMock,
) -> None:
    # Arrange
    stdout = [".", "..", "folder0", "folder1", "file0", "file1", "file2"]
    create_subprocess_shell.return_value = process_mock(0, stdout=stdout)

    # Act
    _, output, _ = await sh(["ls", "-a"])

    # Assert
    assert output == "\n".join(stdout)


@pytest.mark.asyncio
@patch("logging.log", return_value=MagicMock(wraps=logging.log))
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_stdout_logged(
    create_subprocess_shell: MagicMock,
    logging_log: MagicMock,
) -> None:
    # Arrange
    stdout = [".", "..", "folder0", "folder1", "file0", "file1", "file2"]
    create_subprocess_shell.return_value = process_mock(0, stdout=stdout)

    # Act
    await sh(["ls", "-a"])

    # Assert
    assert logging_log.mock_calls == [call(logging.INFO, line) for line in stdout]


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_stderr(
    create_subprocess_shell: MagicMock,
) -> None:
    # Arrange
    stderr = ["file0: Permission Denied", "file1: Permission Denied"]
    create_subprocess_shell.return_value = process_mock(0, stderr=stderr)

    # Act
    _, _, errors = await sh(["ls", "-a"])

    assert errors == "\n".join(stderr)


@pytest.mark.asyncio
@patch("logging.log", return_value=MagicMock(wraps=logging.log))
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_stderr_logged(
    create_subprocess_shell: MagicMock,
    logging_log: MagicMock,
) -> None:
    # Arrange
    stderr = ["file0: Permission Denied", "file1: Permission Denied"]
    create_subprocess_shell.return_value = process_mock(0, stderr=stderr)

    # Act
    await sh(["ls", "-a"])

    # Assert
    assert logging_log.mock_calls == [call(logging.ERROR, line) for line in stderr]


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_check_exitcode_true(
    create_subprocess_shell: MagicMock,
) -> None:
    # Arrange
    create_subprocess_shell.return_value = process_mock(1)

    # Act & Assert
    with pytest.raises(CalledProcessError):
        await sh(["ls", "-a"], check_exitcode=True)


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_check_exitcode_false(
    create_subprocess_shell: MagicMock,
) -> None:
    # Arrange
    create_subprocess_shell.return_value = process_mock(1)

    # Act & Assert
    await sh(["ls", "-a"], check_exitcode=False)
