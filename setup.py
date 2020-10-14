# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:48:09 2020

@author: maras
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('LICENSE') as f:
    license = f.read()    
    
setuptools.setup(
    name="html_parser_A-Maras", # Replace with your own username
    version="0.0.1",
    author="Andrew Maras",
    author_email="andrew_maras@sfu.ca",
    description="html parser extracts html tables from Journal of Natural Products and gathers information about the table.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Maras/TBD",
    license_agreement = license, 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.3',
)