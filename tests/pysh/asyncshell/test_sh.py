import pytest
from asyncio import StreamReader
from typing import Optional
from unittest.mock import AsyncMock, MagicMock, patch

from pysh.asyncshell import sh

# test_create_subprocess_shell
# test_stdout
# test_stderr
# test_check_exitcode


def stream(data: Optional[str] = None) -> StreamReader:
    stream = StreamReader()
    if data:
        stream.feed_data(data.encode())
    stream.feed_eof()

    return stream


def process_mock(
    exitcode: int,
    stdout: str = None,
    stderr: str = None,
) -> MagicMock():
    process = MagicMock()
    process.wait = AsyncMock(return_value=exitcode)
    process.stdout = stream(stdout)
    process.stderr = stream(stderr)
    return process


@pytest.fixture
def process_success() -> MagicMock:
    return process_mock(0)


@pytest.mark.asyncio
@patch("asyncio.subprocess.create_subprocess_shell")
async def test_create_subprocess_shell(
    create_subprocess_shell: MagicMock,
    process_success: MagicMock,
) -> None:
    # Arrange
    create_subprocess_shell.return_value = process_success

    # Act
    await sh(["ls", "-a"])

    # Assert
    assert create_subprocess_shell.call_count == 1
    assert create_subprocess_shell.call_args.kwargs["cmd"] == "ls -a"
