import os
import re

from setuptools import find_packages, setup


def get_version():
    with open(
        os.path.join("src", "textembed", "__init__.py"), "r", encoding="utf-8"
    ) as f:
        file_content = f.read()
        pattern = r"{0}\W*=\W*\"([^\"]+)\"".format("__version__")
        (version,) = re.findall(pattern, file_content)
        return version


def get_requires():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = [
            line.strip()
            for line in file_content.strip().split("\n")
            if not line.startswith("#")
        ]
        return lines


def main():
    setup(
        name="textembed",
        version=get_version(),
        author="Keval",
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
            "Development Status :: 1 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )


if __name__ == "__main__":
    main()
