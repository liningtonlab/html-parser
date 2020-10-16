# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:04:54 2020

@author: maras

## STRATEGY
    # 1. Detect type of table
    #   - Types = C + H, C, H
    #   - Option 1: User defined (function arguement) (USE THIS ONE)
    #   - Option 2: Auto-detect
    # 2. Detect header organization system
    # 3. Parse each column

#def parse_table(soup, table_type, number_compounds):
    "Takes BeautifulSoup table and parse based on inputs
   # Args:
       # soup (BeautifulSoup): soup object with table contents
       # table_type (str): One of "C, H, CH"
       # number_compounds (int): Number of compounds in table"""

from pathlib import Path
from bs4 import BeautifulSoup
import re


def inputs(filepath):
    inp_file1 = Path(filepath)
    with inp_file1.open() as f:
        soup = BeautifulSoup(f.read(), "lxml")
    # print(soup.prettify())
    return soup


def soup_id_headers(soup):
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="colsep0 rowsep0")]
    header_2 = [x for x in header_1 if x != ""]
    # print(header_2)
    return header_2


def num_columns(headers):
    ncol = len(headers)
    # print(ncol)
    return ncol


def cell_clean(i):
    return i.text.replace("\n", "").strip()


def soup_comp_id(soup):
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="rowsep1 colsep0")]
    # print(header_1)
    return header_1


def soup_id_rows(soup):
    rows = [
        [cell_clean(j) for j in i.find_all("td")] for i in soup.tbody.find_all("tr")
    ]
    # print(rows)
    return rows


def get_columns(rows, headers):
    columns = [[x[j] for x in rows] for j in range(len(headers))]
    # print(columns)
    return columns


def clean_celler(i):
    return i.split(",", 1)


# Column parser functions
# Split each peice of data in cell into new columns and convert numbers from strings to float


def column_parser_splitcomma(columns):
    # Take columns into function, which is list of list of each column
    # 1. Have a list of columns of Carbon shifts/CHs and HNMR shifts splitting
    # [['40.8, C', '45.6, CH', '32.1, CH2', '', '38.7, CH2', '', '150.0, C', '55.4, CH', '27.3, CH2', '', '150.1, CH'], ['5.02, d (6.1)', '', '4.47, dd (10.2, 6.1)', '4.17, dd (10.2, 1.9)']]
    # Spliting cell up by first occurence of comma(using split(",", 1))
    # Giving: [['40.8', ' C'], ['45.6', ' CH'], ['32.1', ' CH2'], [''], ['38.7', ' CH2'], [''], ['150.0', ' C'], ['55.4', ' CH'], ['27.3', ' CH2'], [''], ['150.1', ' CH'], ['5.02', ' d (6.1)'], [''], ['4.47', ' dd (10.2, 6.1)'], ['4.17', ' dd (10.2, 1.9)']]
    # result_1 = []
    RESULT_1 = [[clean_celler(item) for item in list] for list in columns]
    # for list in text:
    # for item in list:
    #       textnew = item.split(",", 1)
    #       result_1.append(textnew)
    return RESULT_1


def column_parser_Carbonclean(input):
    # destroys entire list of list of list, now which column is what.
    # Search through each column in the list, if it has "C" or "CH" or "CH2" or "CH3" in it. then format it
    # Might need to have be like get_rows where multiple list made then appended together
    # Carbon_search = re.complie(r'C',r'CH',r'CH2',r'CH3')
    result_2 = []
    for column in input:
        for item in column:
            if type(item) is list:
                result_2.append((item))
    return result_2

    # 2. Move C,CH,CH2,CH3 into new columns(lists), need to separate HNMR splitting and coupling constants ['76.7'],['CH2']/ ['4,47'],['dd (10.2, 6.1)']
    # Separate splitting from coupling constant by splitting at commas(brackets) and converting into separate lists of splitting pattern and coupling constants
    # ['dd (10.2, 6.1)'] into ["dd", "(10.2, 6.1)"], separate the lists ["dd"], ["(10.2,6.1)"]
    # For most cases removing brackets would allow conversion to float, but with special case of dd with two coupling constants the comma would through it off
    # If multiple numbers(2 at most), likely convert to list of string numbers with brackets/commas removed, can be iterated over to convert to float

    # 3. Columns of chemical shifts should only have numbers in string and can convert to float ['76.7'],['4,47']
    # Same for the coupling contants

    # In the end have: Columns with Carbon and Hydrogen chemical shifts with numbers in float not string, Columns with Carbon type(ex. CH/CH3) and splitting pattern in strings,
    # and Columns with coupling constants in float

    # Need to check column to see to if C/H NMR
    # Carbon = simple, just split at column and separate into 2 lists by looking for CH/CH2...etc
    # Proton is more complex since the splitting can vary and have multiple numbers.
    # First separate H chemical shifts from the splitting/coupling into 2 separate lists by if first character thats not space is/is not a number
    # Then separate splitting/coupling into 2 separate lists by if first character a number or letter
    # Most splitting usually m or s, occasionally d (6.1) or dd (4.3,10.2)
    # Make case for if d or dd, or has number(or brackets) then split into another list and can convert everything to float


# Get table type function
# Have Auto-detect, if fails to return type then ask for input
# 1. ***SEMI-WORKING*** - REGEX(see oct6th_test_regex.py for code/info)
# def is_match(regex, text):
# pattern = re.compile(regex, search_character)
# return pattern.search(search_character) is not None
# 2. ***REQUIRES READING*** - String arguments
# Search through strings in HTML, not searching by HTML <tags>
# BUT it pulls entire tag with it

# Detection method
# 1. If primary headers contain I^C/I^H can tell what types;if I^C, carbon; if I^H, proton and if I^C and I^H, both
# 2. If no headers(just numbers)
# Search rows for splitting(s,d,t,m)/Values between 1-10 to see if H
# If values 10-100 and nothing else them must be C


def compound_number(compounds, headers):
    if compounds:  # 1
        return len(compounds)
    elif any("1" or "2" in s for s in headers):  # 2
        return len(headers) - 1
    elif any("Î´C" or "Î´H" in s for s in headers):  # 3
        search = ["Î´H", "Î´C"]
        result = {k: 0 for k in search}
        for item in headers:
            for search_item in search:
                if search_item in item:
                    result[search_item] += 1
        if result["Î´H"] == result["Î´C"]:
            return result.get("Î´H")
        else:
            return max(result.values())
    else:
        return None
