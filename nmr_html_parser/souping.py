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

def inputs(filepath):
    inp_file1 = Path(filepath)
    with inp_file1.open() as f:
        soup = BeautifulSoup(f.read(), "lxml")
    # print(soup.prettify())
    return soup

def soup_id_headers(soup):
    header_1 = [
        cell_clean(i)
        for i in soup.find_all("th", class_="colsep0 rowsep0")
    ]
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
    header_1 = [
        cell_clean(i)
        for i in soup.find_all("th", class_="rowsep1 colsep0")
    ]
    # print(header_1)
    return header_1

def soup_id_rows(soup):
    rows = [
        [cell_clean(j) for j in i.find_all("td")]
        for i in soup.tbody.find_all("tr")
    ]
    # print(rows)
    return rows

def get_columns(rows, headers):
    columns = [[x[j] for x in rows] for j in range(len(headers))]
    # print(columns)
    return columns

# Column parser function
    # Split each peice of data in cell into new columns and convert numbers from strings to float
#def column_parser(columns):
    #Take columns into function, which is list of list of each column,
        #if: ', C(H,H2,H3)',' m(s,d...etc)' - ***MIGHT be able to split after comma
            # some have ', d (6.1)' or ', dd (10.2, 6.1)' - ***WILL be split after comma, so then can be split by brackets()
    # TRY spliting cell up by comma first(Hopefully it doesn't split stuff in brackets***IT DOES...***) ['76.7, CH2'],['4.47, dd (10.2, 6.1)']
        # Have a list of columns of CHs and HNMR splitting ['76.7','CH2'] + ['4,47','dd (10.2,' 6.1)']
            #move C,CH,CH2,CH3 into new columns(lists), need to separate HNMR splitting and coupling constants ['76.7'],['CH2']/ ['4,47'],['dd (10.2,' 6.1)']
                # Separate splitting from coupling constant by brackets
        # original 2D list of columns should only have numbers in string and can convert to float ['76.7'],['4,47']

    #Need to check column to see to if C/H NMR
        # Carbon = simple, just split at column and separate into 2 lists
        # Proton is more complex since it the splitting can also have commas if dd (10.2,6.1)
            # Maybe just make a special case for 

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

def compound_number(compounds,headers):
    if compounds: # 1
        return len(compounds)
    elif any("1" or "2" in s for s in headers): # 2
        return len(headers)-1
    elif any("Î´C" or "Î´H" in s for s in headers): # 3
        search = ['Î´H', 'Î´C']
        result = {k: 0 for k in search}
        for item in headers:
            for search_item in search:
                if search_item in item:
                    result[search_item] += 1
        if result['Î´H'] == result['Î´C']:
            return result.get('Î´H')
        else:
            return max(result.values())
    else:
        return None