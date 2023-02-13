"""Package configuration."""
from setuptools import find_packages, setup

setup(
    name="manifest-app",
    version="0.1",
    packages=find_packages(where="manifest-app"),
    package_dir={"": "manifest-app"},
)