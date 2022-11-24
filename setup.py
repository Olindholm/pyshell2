import logging
import os

from packaging.version import Version
from setuptools import setup


def get_env_var(env_var: str, default: str) -> str:
    value = os.getenv(env_var)

    if not value:
        logging.warning(
            f"Environment variable, ({env_var}), was not set. "
            f"Defaulting to '{default}'."
        )
        return default

    return value


def get_version() -> Version:
    version = get_env_var("PACKAGE_VERSION", "0+dev")
    build = int(get_env_var("BUILD_NUMBER", "1")) - 1

    if build > 0:
        version = f"{version}.{build}"

    return Version(version)


deps = {
    "",
}
test_deps = {
    "pytest>=7",
    "pytest-asyncio",
    "pytest-cov",
}
typing_deps = {
    "mypy",
    *test_deps,
    "types-setuptools",
}
dev_deps = {
    *test_deps,
    "black",
    "isort",
    *typing_deps,
    "flake8",
    "flake8-pyproject>=1.2.0",
}

setup(
    # General
    name="pyshell2",
    version=str(get_version()),
    description="Python library for running shell commands.",
    url="https://github.com/Olindholm/pyshell2",
    # Dependencies
    python_requires=">=3.8",
    install_requires=[deps],
    extras_require={
        "test": test_deps,
        "typing": typing_deps,
        "dev": dev_deps,
    },
)
