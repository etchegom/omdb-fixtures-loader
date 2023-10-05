from __future__ import annotations

import os.path as op

from setuptools import find_packages, setup


def read(fname):
    return open(op.join(op.dirname(__file__), fname)).read()


setup(
    name="omdb_fixtures_loader",
    version="1.0.0",
    author="Matthieu Etchegoyen",
    author_email="etchegom@gmail.com",
    description="Simple tool used to build fixtures data by fetching OMDB data.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="fixtures OMDB",
    url="https://github.com/etchegom/omdb-fixtures-loader.git",
    packages=find_packages(),
    install_requires=["requests"],
    license="MIT License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.7",
    ],
)
