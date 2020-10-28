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
    '''Takes filepath as input and returns BeautifulSoup object'''
    inp_file1 = Path(filepath)
    with inp_file1.open() as f:
        soup = BeautifulSoup(f.read(), "lxml")
    return soup
# TODO: ADD function to parse html source code(soup) to find and replace error-causing characters like: &nbsp; and '

# Simple Functions
def num_columns(headers):
    ncol = len(headers)
    return ncol
def if_blank(i):
    if i == "":
        return True
def no_space_list(list):
    return [x for x in list if x != ""]
def no_space_2dlist(list_list):
    return [[x for x in list if x != ""] for list in list_list]
def cell_clean(i):
    '''Takes string converting to text, removing line breaks/empty elements, strips extra whitespace'''
    return i.text.replace("\n", "").strip()
def all_same(items):
    '''Takes list and checks if all the elements in said list are the same, returning True if so'''
    return all( map(lambda x: x == items[0], items ) )

# html Table Parsing Functions
def soup_id_headers(soup):
    '''Takes soup object and returns column headers'''
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="colsep0 rowsep0")]
    return no_space_list(header_1)
def soup_comp_id(soup):
    '''Takes soup object and returns compound identification headers'''
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="rowsep1 colsep0")]
    return header_1
def soup_id_rows(soup):
    '''Takes soup object and returns rows'''
    rows =  [[cell_clean(j) for j in i.find_all("td")] for i in soup.tbody.find_all("tr")]
    return rows

def compound_number(compounds, headers):
    '''Takes primary headers and compound id headers and returns the number of compounds.
    Based on len of compound id headers, numbers in main headers or number of hits of IH/IC'''
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

def get_columns(rows, headers):
    '''Takes rows and length of headers to get columns based on 2D list index from rows'''
    columns = [[x[j] for x in rows] for j in range(len(headers))]
    return columns

def get_atom_index_column(columns):
    '''Enumerate the list of columns so that positional index and atom_index can be returned'''
    return list(enumerate(columns))[0]
    # atom_index should be first column so can take that list and go from there

def attach_headers_to_columns(headers,columns):
    '''Takes header as key assigning to list of column values using a dictionary'''
    dictionary = {}
    same_header_variator = "" # Might need to modify, but could be blank spaces affecting results
    for header, column in zip(headers, columns):
        if header in dictionary:
            same_header_variator = same_header_variator + " "
            dictionary[header + same_header_variator] = column
        else:
            dictionary[header] = column
    return dictionary

# TODO: modify to accept columns(2dlist) by removing 2 dict inputs and puting 2dlist, and it should work
def table_detect(soup,dict,dict2):
    # Detection method
 # 1. If primary headers contain I^C/I^H(Most cases) can detect table type;if I^C, carbon; if I^H, proton and if I^C and I^H, both
    '''"<th align="center" class="colsep0 rowsep0">Î´<sub>H</sub>","<th align="center" class="colsep0 rowsep0">Î´<sub>C</sub>","(m<sub>,</sub><i>J</i> in Hz)","mult. (<i>J</i>, Hz)"'''
    # a. Use regex to find th tag then sub tag with string to determine if H and/or C from headers
    # if Carbon,Proton == True, contains both C/HNMR data in table; elif Carbon == True, contains CNMR data in table;elif Proton == True, contains HNMR data in table
    # else: have to look further, ex.
 # 2. If no headers(just numbers)
    # a. Search rows for splitting(s,d,t,m) and/or  contains C|CH|CH[2-3]
    '''"1.09, s","3.62, m","3.71, br d (11.0)","4.17, dd (10.2, 1.9)","1.09, dddd (18.6,13.2, 5.4, 2.4)","7.26 (m)","6.12 (dd, 16.0, 6.4)","4.85 (td, 7.3, 4.2)"'''
    # b. Or else can maybe search strings of numbers in rows, get ones w/ decimal(float) and make a list
    # Use REGEX to search with pattern that has('\d*[0-9].{1}\d*[0-9],{1}\s{1}'). Convert list to float, take average if: Values between 1-10 to see if H; values 10-250 and nothing else them must be C

    '''Takes soup object, dictionary of column cells, dictionary of cell floats. Uses regex/string arguments and calculates float averages to detect and return table type'''
    Carbon = soup.find("sub", string=re.compile("C"))#Don't use findall, look in through th for <sub> w/ string='C'or'H'
    Proton = soup.find("sub", string=re.compile("H"))
    if Carbon and Proton:
        return ('Both H1/C13 NMR Table Detected!')
    elif Carbon:
        return ('C13 NMR Table Detected!')
    elif Proton:
        return (('H1 NMR Table Detected!'))
    else:
        for item in dict:  # Iterating over each element(column) in dictionary
            for value in dict[item]:
                if re.search(r'(\d*[0-9]\.\d*[0-9]\,\s{1}\w*[s,t,d,m,q,b,r]\s{1})|(\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\))', value):
                    HNMR_Search = True
                elif re.search(r'(\d*[0-9]\.\d*[0-9])(\,\sCH3|\,\sCH2|\,\sCH|\,\sC)', value):
                    CNMR_Search = True
                else:
                    continue
        if HNMR_Search and CNMR_Search:
            return ("Both H1/C13 NMR Detected! - From Cells!")
        elif HNMR_Search and not CNMR_Search:
            return ("H1 NMR Detected! -  From Cells!")
        elif CNMR_Search and not HNMR_Search:
            return ('H1 NMR Table Detected! - From cells')
        else:
            average_list = []
            for item in dict2:
                value_list = []
                for value in dict2[item]:
                    if type(value) == float:
                        value_list.append(value)
                if all_same(value_list) == False:
                    average = sum(value_list) / len(value_list)
                    average_list.append(average)
                    print(average_list)
                    if 14.0 <= average <= 250.0:
                        CNMR = True
                        continue
                    elif 0.0 <= average <= 13.5:
                        HNMR = True
                        continue
            if CNMR and HNMR == True:
                return ("Both H1/C13 NMR Detected! - From chemical shifts!")
            elif HNMR and not CNMR:
                return ("H1 NMR Detected! -  From chemical shifts!")
            elif CNMR and not HNMR:
                return ('H1 NMR Table Detected! - From chemical shifts!')
            else:
                 # TODO: USER input if failure
                '''while True:
                    ask = input("Detection Failure - What kind of table if this? (H,C or Both)")
                    if ask.lower().upper() == "H":
                        HNMR = True
                        print('HNMR')
                        break
                    elif ask.lower().upper() == "C":
                        CNMR = True
                        print('CNMR')
                        break
                    elif ask.lower().upper() == "BOTH":
                        CNMR = True
                        HNMR = True
                        print('Both')
                        break
                    else:
                        print("I don't understand, please try again.")'''

def column_id_cleaner(dict):
    '''Takes dictionary of columns with headers. Searchs keys first for regex patterns to detect if column will contain H/C NMR, then each cell for regex patterns'''
    # Column type detection
    # first detect the table type to determine which column type could be present??def detect_column_type(headers, idx, col):
    # might make based on numerical value, 0-13 for H, 15 - 200 for carbon; but numbers could go outside of ranges
    # might have to assign the headers to the column and then search headers for C, since C/CH2 not always in column
    # Carbon = looking for C in header, 15-200ppm and sometimes C,CH,CH2 in column cells
    # Proton = looking for H/ mult. (J in Hz) in header, 0-13ppm and splitting/coupling constants in column cell

    # Regex patterns
    # TODO: Add other possible multiplicity regex patterns
    CNMR_pattern_1 = re.compile(r'\,\sCH3|\,\sCH2|\,\sCH|\,\sC')
    CNMR_pattern_2 = re.compile(r'CH3|CH2|CH|C')
    regex_pattern_1 = re.compile(r'Î´C')
    regex_pattern_2 = re.compile(r'Î´H')
    HNMR_pattern_1 = re.compile(r'(\,{1}\s\w*[s,t,d,m,q,b,r,q]\s?\w*[s,t,d,m,q,b,r,q]\s?|\,{1}\s\w*[s,t,d,m,q,b,r,q]\s?|\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\))')
    HNMR_pattern_2 = re.compile(r'(\s\w*[s,t,d,m,q,b,r,q]\s?\w*[s,t,d,m,q,b,r,q]\s?\([0-9]+\.[0-9]\)|\s\w*[s,t,d,m,q,b,r,q]\s?\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\)|\s\w*[s,t,d,m,q,b,r,q]\s?)')

    #2D lists
    C_type = []
    Carbon_spec = []
    H_spec = []
    H_multiplicity = []
    for item in dict: # Iterating over each element(column) in dictionary
      c_type1 = []
      Carbon_spec1 = []
      H_spec1 = []
      H_multiplicity1 = []

      if regex_pattern_1.search(item): # If headers match regex pattern
          print(item + '\nColumn Data Type: CARBON' + '\n' + str(dict[item]))
      elif regex_pattern_2.search(item):
          print(item + '\nColumn Data Type: PROTON' + '\n' + str(dict[item]))
      else:
        print(item + '\nColumn data type unknown, must be atom position or non-C/H NMR!' + '\n' + str(dict[item]))
        None
        # Might need other cleaning method if random stuff appears with different tables(ones that return special charcters)

      for value in dict[item]:
        if CNMR_pattern_1.search(value): #if CNMR_pattern_1 found with .search regex:
            c_type1.append(CNMR_pattern_2.search(value).group()) #append item to new list
            Carbon_spec1.append(CNMR_pattern_1.sub("", value)) # while removing from original
        elif HNMR_pattern_1.search(value): # Same as CNMR, but for HNMR
            H_multiplicity1.append(HNMR_pattern_2.search(value).group())
            H_spec1.append(HNMR_pattern_1.sub("", value))
        elif "" == value: # elif " "(blank space, could be from regex search; append to list, but keep in original
            c_type1.append(value)
            Carbon_spec1.append(value)
            H_spec1.append(value)
            H_multiplicity1.append(value)
        else:
            None
      # Removing irrelevant list, also replacing dict with new cleaned chemical shift column
      if all_same(c_type1) == False:
        C_type.append(c_type1)
      if all_same(Carbon_spec1) == False:
          Carbon_spec.append(Carbon_spec1)
          dict[item] = Carbon_spec1
      if all_same(H_multiplicity1) == False:
          H_multiplicity.append(H_multiplicity1)
      if all_same(H_spec1) == False:
          H_spec.append(H_spec1)
          dict[item] = H_spec1

    # Counter to id compound C-type and appending new columns to dict
    Counter = 0
    for i in C_type:
        Counter = Counter + 1
        dict['Carbon Type ' + str(Counter)] = i
    Counter_2 = 0
    for x in H_multiplicity:
        Counter_2 = Counter_2 + 1
        dict['Multiplicity & Coupling Constants ' + str(Counter_2)] = x
    return dict

def column_id_cleaner_list(d2_list):
    '''Takes dictionary of columns with headers. Searchs keys first for regex patterns to detect if column will contain H/C NMR, then each cell for regex patterns'''
    # Column type detection
    # first detect the table type to determine which column type could be present??def detect_column_type(headers, idx, col):
    # might make based on numerical value, 0-13 for H, 15 - 200 for carbon; but numbers could go outside of ranges
    # might have to assign the headers to the column and then search headers for C, since C/CH2 not always in column
    # Carbon = looking for C in header, 15-200ppm and sometimes C,CH,CH2 in column cells
    # Proton = looking for H/ mult. (J in Hz) in header, 0-13ppm and splitting/coupling constants in column cell

    # Regex patterns
    # TODO: Add other possible multiplicity regex patterns
    CNMR_pattern_1 = re.compile(r'\,\sCH3|\,\sCH2|\,\sCH|\,\sC')
    CNMR_pattern_2 = re.compile(r'CH3|CH2|CH|C')
    regex_pattern_1 = re.compile(r'Î´C')
    regex_pattern_2 = re.compile(r'Î´H')
    HNMR_pattern_1 = re.compile(r'(\,{1}\s\w*[s,t,d,m,q,b,r,q]\s?\w*[s,t,d,m,q,b,r,q]\s?|\,{1}\s\w*[s,t,d,m,q,b,r,q]\s?|\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\))')
    HNMR_pattern_2 = re.compile(r'(\s\w*[s,t,d,m,q,b,r,q]\s?\w*[s,t,d,m,q,b,r,q]\s?\([0-9]+\.[0-9]\)|\s\w*[s,t,d,m,q,b,r,q]\s?\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\)|\s\w*[s,t,d,m,q,b,r,q]\s?)')

    #2D lists
    C_type = []
    Carbon_spec = []
    H_spec = []
    H_multiplicity = []
    for item in d2_list: # Iterating over each element(column) in dictionary
      c_type1 = []
      Carbon_spec1 = []
      H_spec1 = []
      H_multiplicity1 = []

      for value in item:
        if CNMR_pattern_1.search(value): #if CNMR_pattern_1 found with .search regex:
            c_type1.append(CNMR_pattern_2.search(value).group()) #append item to new list
            Carbon_spec1.append(CNMR_pattern_1.sub("", value)) # while removing from original
        elif HNMR_pattern_1.search(value): # Same as CNMR, but for HNMR
            H_multiplicity1.append(HNMR_pattern_2.search(value).group())
            H_spec1.append(HNMR_pattern_1.sub("", value))
        elif "" == value: # elif " "(blank space, could be from regex search; append to list, but keep in original
            c_type1.append(value)
            Carbon_spec1.append(value)
            H_spec1.append(value)
            H_multiplicity1.append(value)
        else:
            None
      # Removing irrelevant list, also replacing dict with new cleaned chemical shift column
      if all_same(c_type1) == False:
        C_type.append(c_type1)
      if all_same(Carbon_spec1) == False:
          Carbon_spec.append(Carbon_spec1)

      if all_same(H_multiplicity1) == False:
          H_multiplicity.append(H_multiplicity1)
      if all_same(H_spec1) == False:
          H_spec.append(H_spec1)

    # Counter to id compound C-type and appending new columns to dict
    Counter = 0
    '''for i in C_type:
        Counter = Counter + 1
        dict['Carbon Type ' + str(Counter)] = i
    Counter_2 = 0
    for x in H_multiplicity:
        Counter_2 = Counter_2 + 1
        dict['Multiplicity & Coupling Constants ' + str(Counter_2)] = x'''
    return H_spec,Carbon_spec #,H_multiplicity,C_type
def column2dlist_string_to_float(d2_list):
    ''' Takes dictionary that has been cleaned by column_id_cleaner()(or any dictionary), will just take decimal number
    if string begins with it (regex pattern(^\d*[0-9].{1}\d*[0-9]) recognized) and convert to float in a new list, then
    replace dict[item](for item in dict(INPUT)) with new list.
    INPUT: dictionary
    OUTPUT: returns dictionary with float numbers if regex pattern recognized'''
    float_pattern = re.compile(r'(^\d*[0-9].{1}\d*[0-9])')# change to must begin with
    new_result = []
    for item in d2_list:
        spec_float1 = []
        for value in item:
            if float_pattern.search(value):
                for spec_value in float_pattern.findall(value):
                    spec_float1.append(spec_value)
            elif "" == value:
                spec_float1.append(value)
        if all_same(spec_float1)== False:
            spec_results = []
            for i in spec_float1:
                if not if_blank(i):
                    spec_results.append(float(i))
                elif "" == i:
                    spec_results.append(i)
            new_result.append(spec_results)
    return new_result



def columndict_string_to_float(dict):
    ''' Takes dictionary that has been cleaned by column_id_cleaner()(or any dictionary), will just take decimal number
    if string begins with it (regex pattern(^\d*[0-9].{1}\d*[0-9]) recognized) and convert to float in a new list, then
    replace dict[item](for item in dict(INPUT)) with new list.
    INPUT: dictionary
    OUTPUT: returns dictionary with float numbers if regex pattern recognized'''
    float_pattern = re.compile(r'(^\d*[0-9].{1}\d*[0-9])')# change to must begin with
    for item in dict:
        spec_float1 = []
        for value in dict[item]:
            if float_pattern.search(value):
                for spec_value in float_pattern.findall(value):
                    spec_float1.append(spec_value)
            elif "" == value:
                spec_float1.append(value)
        if all_same(spec_float1)== False:
            spec_results = []
            for i in spec_float1:
                if not if_blank(i):
                    spec_results.append(float(i))
                elif "" == i:
                    spec_results.append(i)
            dict[item] = spec_results
    return dict

# TODO: Sort each data column into appropriate compounds
#def from_float_to_sorted_data(float_dict):
    # 1. Since dict are ordered, put first index(atom position).

    # 2. Use num_comp to determine number of compounds and table_detect to determine if H/C present; data sorted into the right final place
        # This will determine layout pattern: (First item in dict will be atom position)
            # Usually for both pattern is: atom_position + (IH + IC)n, n = # of comps
            # Then for single: atom_position + (IC or IH)n, n = # of comps
            # Since NMR tables don't expect to see many other column types beside 2DNMR(Could ID if 1D works out), label as other
            ## for 2 comps, 2 C types and 2 multiplicity; that is added to end of dictionary after column cleaning

   # 3. Sort column data into either: atom position, Proton, Carbon or other. Which then can be dumped into JSON file to output(See Goal in README.md).


