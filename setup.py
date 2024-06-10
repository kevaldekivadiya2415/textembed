"""Setup script for the TextEmbed package."""

import os
import re

from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))


def get_version() -> str:
    """
    Reads the version of the package from the __init__.py file.

    Returns:
        str: The version string.
    """
    with open(
        os.path.join("src", "textembed", "__init__.py"), "r", encoding="utf-8"
    ) as f:
        version = ""
        file_content = f.read()
        pattern = r'__version__ = "([^"]+)"'
        match_group = re.search(pattern, file_content)
        if match_group:
            version = match_group.group(1)
        return version


def get_requires():
    """
    Reads the list of dependencies from the requirements.txt file.

    Returns:
        list: A list of dependency strings.
    """
    with open(
        os.path.join(this_directory, "requirements.txt"), "r", encoding="utf-8"
    ) as f:
        file_content = f.read()
        lines = [
            line.strip()
            for line in file_content.strip().split("\n")
            if line and not line.startswith("#")
        ]
        return lines


FASTAPI_DESCRIPTION = (
    "TextEmbed provides a robust and scalable REST API for generating vector embeddings from text. "
    "Built for performance and flexibility, it supports various sentence-transformer models, allowing "
    "users to easily integrate state-of-the-art NLP techniques into their applications. Whether you need "
    "embeddings for search, recommendation, or other NLP tasks, TextEmbed delivers with high efficiency."
)


def main():
    """
    Main function to setup the package using setuptools.
    """
    setup(
        name="textembed",
        version=get_version(),
        author="Keval Dekivadiya",
        author_email="kevaldekivadiya2415@gmail.com",
        description=FASTAPI_DESCRIPTION,
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords=["Embedding", "RAG"],
        license="Apache License 2.0",
        url="https://github.com/kevaldekivadiya2415/textembed",
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
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )


if __name__ == "__main__":
    main()
