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
    return soup

def no_space_list(list):
    return [x for x in list if x != ""]

def no_space_2dlist(list_list):
    return [[x for x in list if x != ""] for list in list_list]

def soup_id_headers(soup):
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="colsep0 rowsep0")]
    return no_space_list(header_1)

def num_columns(headers):
    ncol = len(headers)
    return ncol

def cell_clean(i):
    return i.text.replace("\n", "").strip()

def soup_comp_id(soup):
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="rowsep1 colsep0")]
    return header_1

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

def soup_id_rows(soup):
    rows =  [[cell_clean(j) for j in i.find_all("td")] for i in soup.tbody.find_all("tr")]
    return rows

def get_columns(rows, headers):
    columns = [[x[j] for x in rows] for j in range(len(headers))]
    return columns

def get_atom_index_column(columns):
    # enumerate the list of columns so that positional index and atom_index can be returned
    return list(enumerate(columns))[0]
    # returns atom_index_column_index, atom_index_column
    # atom_index should be first column so can take that list and go from there

def attach_headers_to_columns(headers,columns):
    # assign headers to columns, with dictionaries
    dictionary = {}
    same_header_variator = ""
    for header, column in zip(headers, columns):
        if header in dictionary:
            same_header_variator = same_header_variator + " "
            dictionary[header + same_header_variator] = column
        else:
            dictionary[header] = column
    return dictionary
    
    # TODO: Column type detection
    # first detect the table type to determine which column type could be present??
    # def detect_column_type(headers, idx, col):
    # might make based on numerical value, 0-13 for H, 15 - 200 for carbon; but numbers could go outside of ranges
    # might have to assign the headers to the column and then search headers for C, since C/CH2 not always in column
    # Carbon = looking for C in header, 15-200ppm and sometimes C,CH,CH2 in column cells
    # Proton = looking for H/ mult. (J in Hz) in header, 0-13ppm and splitting/coupling constants in column cell

def column_id_cleaner(dict):
    # Below ids the column based on headers, so this first then if it fails have to look in each cell
    CNMR_pattern_1 = re.compile(r'\,\sCH3|\,\sCH2|\,\sCH|\,\sC')
    CNMR_pattern_2 = re.compile(r'CH3|CH2|CH|C')
    regex_pattern_1 = re.compile(r'Î´C, type *')
    C_type = []
    Carbon_spec = []
    for item in dict:
      c_type1 = []
      Carbon_spec1 = []
      Carbon_spec.append(Carbon_spec1)
      C_type.append(c_type1)
      if regex_pattern_1.search(item): #
        print(item + '\nColumn Data Type: CARBON' + '\n' + str(dict[item]))
      elif 'Î´H' in item:
        print(item + '\nColumn Data Type: PROTON' + '\n' + str(dict[item]))
      else:
        print(item + '\nColumn data type unknown, must be atom position or non-C/H NMR!' + '\n' + str(dict[item]))
      for value in dict[item]:
        if CNMR_pattern_1.search(value): #if CNMR_pattern_1 found with .search regex:
            c_type1.append(CNMR_pattern_2.search(value).group()) #append item to new list
            Carbon_spec1.append(CNMR_pattern_1.sub("", value)) # while removing from original
        #elif HNMR_pattern_1.search(value):
            # same for Proton; make pattern for splitting,
            # coupling constanst(6.12 (dd, 16.0, 6.4)/4.85 (td, 7.3, 4.2)/7.26 (m)/8.14 (brs) or , dddd (18.6, 13.2, 5.4, 2.4)/dd (10.2, 1.9)/d (2.8)/1.09, s/3.62, m/br d (11.0))
        elif "" == value: # elif " "(blank space, could be from regex search; append to list, but keep in original
            c_type1.append(value)
            Carbon_spec1.append(value)
        else: # Might need other cleaning method if random stuff appears with different tables(ones that return special charcters)
            None
    dict[item] = Carbon_spec

    dict['Carbon Type'] = C_type # Currently adding C_type as one list of values, need to break it up(check if list is empty; if so remove from 2d list) into a different key for each set of values.
        # Also determine which compound number its for; otherwise make 1,2,3... etc based on occurence from left to right in table
    return C_type, Carbon_spec

 # TODO: Get table type function
# Have Auto-detect, if fails to return type then ask for input
# 1. ***SEMI-WORKING*** - REGEX(see oct6th_test_regex.py for code/info)
# def is_match(regex, text):
# pattern = re.compile(regex, search_character)
# return pattern.search(search_character) is not None
# 2. ***REQUIRES READING*** - String arguments
# Search through strings in HTML, not searching by HTML <tags>
# BUT it pulls entire tag with it, could use to search for pattern in whole table and pull tag and have input to confirm

# Detection method
# 1. If primary headers contain I^C/I^H can tell what types;if I^C, carbon; if I^H, proton and if I^C and I^H, both
# 2. If no headers(just numbers)
# Search rows for splitting(s,d,t,m)/Values between 1-10 to see if H
# If values 10-100 and nothing else them must be C

