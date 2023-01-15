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


deps = [""]
test_deps = ["pytest>=7", "pytest-asyncio", "pytest-cov"]
black_deps = ["black==22.8.0"]
isort_deps = ["isort==5.10.1"]
mypy_deps = ["mypy==0.991", *test_deps, "types-setuptools", "packaging"]
flake8_deps = ["flake8==6.0.0", "flake8-pyproject>=1.2.0"]
dev_deps = [*test_deps, *black_deps, *isort_deps, *mypy_deps, *flake8_deps]

setup(
    # General
    name="pyshell2",
    version=str(get_version()),
    description="Python library for running shell commands.",
    url="https://github.com/Olindholm/pyshell2",
    # Dependencies
    python_requires=">=3.8",
    install_requires=deps,
    extras_require={
        "test": test_deps,
        "black": black_deps,
        "isort": isort_deps,
        "mypy": mypy_deps,
        "flake8": flake8_deps,
        "dev": dev_deps,
    },
)
