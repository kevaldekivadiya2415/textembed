"""Setup script for the TextEmbed package."""

import os
import re

from setuptools import find_packages, setup


def get_version():
    """
    Reads the version of the package from the __init__.py file.

    Returns:
        str: The version string.
    """
    with open(
        os.path.join("src", "textembed", "__init__.py"), "r", encoding="utf-8"
    ) as f:
        file_content = f.read()
        pattern = r"__version__\W*=\W*\"([^\"]+)\""
        (version,) = re.findall(pattern, file_content)
        return version


def get_requires():
    """
    Reads the list of dependencies from the requirements.txt file.

    Returns:
        list: A list of dependency strings.
    """
    with open("requirements.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = [
            line.strip()
            for line in file_content.strip().split("\n")
            if line and not line.startswith("#")
        ]
        return lines


def main():
    """
    Main function to setup the package using setuptools.
    """
    setup(
        name="textembed",
        version=get_version(),
        author="Keval Dekivadiya",
        author_email="kevaldekivadiya2415@gmail.com",
        description="TextEmbed inference",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords=["Embedding"],
        license="Apache License 2.0",
        url="",
        package_dir={"": "src"},
        packages=find_packages("src"),
        python_requires=">=3.10.0",
        install_requires=get_requires(),
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )


if __name__ == "__main__":
    main()
