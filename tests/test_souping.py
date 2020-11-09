# -*- coding: utf-8 -*-
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from nmr_html_parser import runner
from nmr_html_parser import column_test

# Add some real unit tests
TESTDIR = Path(__file__).parent

FILES = ["test_1","test_Both_no_CHn","test_CNMR_no_headers","test_CNMR_number_headers","test_CNMR_ONLY","test_HNMR_no_headers","test_HNMR_ONLY"]


def load_expected(fname):
    fpath = TESTDIR / "outputs" / fname
    return pd.read_csv(fpath)


@pytest.mark.parametrize("fname", FILES)
def test_parse(fname):
    filepath = Path() / "test_outputs" / f"{fname}.csv"
    expected = load_expected(f"{fname}.csv")
    runner.parse(TESTDIR / "inputs" / f"{fname}.html", filepath)
    output = pd.read_csv(filepath)
    print(output, expected)
    assert_frame_equal(expected, output)

def load_columns(fname):
    fpath = TESTDIR / "column_outputs" / fname
    inp_file1 = Path(fpath)
    with inp_file1.open() as f:
        f = f.read()
    return f

@pytest.mark.parametrize("fname", FILES)
def test_columns(fname):
    # take file with expected columns results
    filepath = Path() / "test_outputs" / f"{fname}.py"
    expected = load_columns(f"{fname}.py")
    # run input file, and create column
    output = column_test.column(TESTDIR / "inputs" / f"{fname}.html", filepath)
    # Run assertions to check if output matches expected
    assert expected == output

# def test_inputs():
#     # Need to make this better
#     soup = souping.inputs(TESTDIR / "test_table.html")
#     assert isinstance(soup, BeautifulSoup)
#     assert soup.prettify()
#     # This next line causes test to fail on purpose as a demonstration
#     # assert False
