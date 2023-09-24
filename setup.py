import os
import sys
from setuptools import setup

VERSION = "1.0.2"

setup(
    name="Markdown Inline Graphviz Extension",
    version=VERSION,
    py_modules=["mdx_inline_graphviz"],
    install_requires=[
        "Markdown >= 3, < 4",
        "graphviz >= 0.20.1, < 1"
    ],
    author="Luis Medel",
    author_email="luis@luismedel.com",
    description="Render inline graphs with Markdown and Graphviz",
    license="MIT",
    url="https://github.com/luismedel/markdown-inline-graphviz",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
