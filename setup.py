# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:48:09 2020

@author: maras
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE.txt", "r") as f:
    license = f.read()

setuptools.setup(
    name="nmr_html_parser",  # Replace with your own username
    version="0.0.2",
    author="Andrew Maras",
    author_email="andrew_maras@sfu.ca",
    description="html parser extracts data from ACS table HTML tables and gathers information about the table.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liningtonlab/html-parser",
    license_agreement=license,
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
