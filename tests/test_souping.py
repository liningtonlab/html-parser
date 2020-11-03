# -*- coding: utf-8 -*-
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from bs4 import BeautifulSoup
from nmr_html_parser import souping, runner

# Add some real unit tests

FILES = ["test_1", "test_2"]


def load_expected(fname):
    fpath = Path() / "outputs" / fname
    return pd.read_csv(fpath)


@pytest.mark.parametrize("fname", FILES)
def test_parse(fname):
    expected = load_expected(fname)
    output = runner.parse(Path() / "inputs" / fname)
    assert_frame_equal(expected, output)


def test_inputs():
    # Need to make this better
    soup = souping.inputs("./tests/test_table.html")
    assert isinstance(soup, BeautifulSoup)
    assert soup.prettify()
    # This next line causes test to fail on purpose as a demonstration
    # assert False
