# -*- coding: utf-8 -*-
import pytest

from bs4 import BeautifulSoup
from nmr_html_parser import souping

## Add some real unit tests

## Example


def test_inputs():
    # Need to make this better
    soup = souping.inputs("./tests/test_table.html")
    assert isinstance(soup, BeautifulSoup)
    assert soup.prettify()
    # This next line causes test to fail on purpose as a demonstration
    # assert False
