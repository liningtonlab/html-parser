# -*- coding: utf-8 -*-
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from nmr_html_parser import runner
from nmr_html_parser import column_test
from bs4 import BeautifulSoup

# Add some real unit tests
TESTDIR = Path(__file__).parent

FILES_RESULTS = [("test_1", [['2', '', '3a', '4', '4a', '5', '7a', '8', '8a', '9', '10', '11', '12', '12a', '12b', '12c', '12d', '1′', '', '2′', 'NH', '', 'OMe-9', 'OMe-11', 'OMe-12'], ['102.5, CH2', '', '153.9, C', '105.4, CH', '118.6, C', '163.4, C', '152.3, C', '39.0, CH', '121.0, C', '150.5, C', '113.2, CH', '113.1, CH', '151.5, C', '118.0, C', '111.7, C', '150.6, C', '119.7, C', '34.7, CH2', '', '170.4, C', '', '', '56.6, CH3', '', '56.3, CH3'], ['6.21, d (0.9)', '6.35, d (0.9)', '', '7.59, s', '', '', '', '5.48, s', '', '', '7.03, d (9.2)', '7.02, d (9.2)', '', '', '', '', '', '3.09, d (16.9)', '3.48, d (16.9)', '', '5.69, br s', '6.96, br s', '3.95, s', '', '3.89, s'], ['103.1, CH2', '', '153.4, C', '106.4, CH', '119.2, C', '163.3, C', '152.0, C', '38.7, CH', '111.9, C', '157.7, C', '99.8, CH', '161.4, C', '104.5, CH', '128.9, C', '114.9, C', '149.8, C', '118.2, C', '34.3, CH2', '', '170.6, C', '', '', '56.2, CH3', '55.6, CH3', ''], ['6.30, d (0.9)', '6.42, d (0.9)', '', '7.65, s', '', '', '', '5.47, s', '', '', '6.59, d (2.3)', '', '7.54, d (2.3)', '', '', '', '', '3.08, d (16.9)', '3.59, d (16.9)', '', '5.55, br s', '6.95, br s', '3.97, s', '3.89, s', '']]
)]

FILES = ["rowspan2_test","test_1","test_2","test_3","test_4","test_5_c","test_5_h","test_6_c","test_6_h_overlapped","test_7_c","test_8_c","test_8_h","test_Both_no_CHn","test_CNMR_no_headers","test_CNMR_number_headers","test_CNMR_ONLY","test_HNMR_no_headers","test_HNMR_ONLY"]

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

# Useless as using list with parametrize
#def load_columns(fname):
    #fpath = TESTDIR / "column_outputs" / fname
    #inp_file1 = Path(fpath)
    #with inp_file1.open() as f:
      #  f = f.read()
      #  f = str(f).replace("&nbsp;", " ")
      #  f = f.encode("cp1252")
      #  soup = BeautifulSoup(f, "lxml")
    #return soup.get_text()


@pytest.mark.parametrize("fname, expected", FILES_RESULTS)
def test_columns(fname,expected):
    # take file with expected columns results
    filepath = Path() / "test_outputs" / f"{fname}.txt"
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
