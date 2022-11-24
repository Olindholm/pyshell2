from setuptools import setup

deps = {
    "",
}
test_deps = {
    "pytest>=7",
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
    "flake8-pyproject",
}

setup(
    # General
    name="pyshell2",
    version="0+dev",
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
