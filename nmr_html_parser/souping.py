# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:04:54 2020

@author: maras"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import csv


def inputs(filepath):
    """Takes filepath as input and returns BeautifulSoup object"""
    inp_file1 = Path(filepath)  # UTF-8
    with inp_file1.open() as f:
        f = f.read()
        # TODO: Ensure this is working properly to clear junk; check other parts that used I^ in search b/c now δ
        f = str(f).replace("&nbsp;", " ")
        # f = f.encode("cp1252")
        soup = BeautifulSoup(f, "lxml")
    return soup


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
    """Takes string converting to text, removing line breaks/empty elements, strips extra whitespace"""
    return i.text.replace("\n", "").strip()


def all_same(items):
    """Takes list and checks if all the elements in said list are the same, returning True if so"""
    return all(map(lambda x: x == items[0], items))


def blanks_list(list_length):
    blanks = []
    for i in list_length:
        blanks1 = []
        for x in range(len(i)):
            blanks1.append(r"")
        blanks.append(blanks1)
    return blanks


# html Table Parsing Functions
def soup_id_headers(soup):
    """Takes soup object and returns column headers"""
    # if soup.find_all("th", class_="colsep0 rowsep0"):
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="colsep0 rowsep0")]
    return no_space_list(header_1)


# TODO: fix for test_CNM_number_headers.html, because headers swapped will compnum and only detected as 1 comp
def soup_comp_id(soup):
    """Takes soup object and returns compound identification headers"""
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="rowsep1 colsep0")]
    return header_1


def soup_id_rows(soup):
    """Takes soup object and returns rows"""
    rows = [
        [cell_clean(j) for j in i.find_all("td")] for i in soup.tbody.find_all("tr")
    ]
    print(rows)
    return rows


# TODO: fixed above TODO by swapping if and first elif statment; must be better solution
def compound_number(compounds, headers):
    """Takes primary headers and compound id headers and returns the number of compounds.
    Based on len of compound id headers, numbers in main headers or number of hits of IH/IC"""
    if compounds:
        return len(compounds)
    elif any(
        "1" or "2" in s for s in headers
    ):  # 2 Call before if compounds, so that one isnt return for wrong headers
        return len(headers) - 1
    elif any("Î´C" or "Î´H" in s for s in headers):
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
    """Takes rows and length of headers to get columns based on 2D list index from rows"""
    if headers:
        columns = [[x[j] for x in rows] for j in range(len(headers))]
    else:
        columns = [[x[j] for x in rows] for j in range(len(headers_2))]
    return columns


def get_atom_index_column(columns):
    """Enumerate the list of columns so that positional index and atom_index can be returned"""
    return list(enumerate(columns))[0]
    # atom_index should be first column so can take that list and go from there


def table_detect(soup, d2list, float_d2list):
    """Takes soup object, 2dlist of column cells, 2dlist of cell floats. Uses regex/string arguments and calculates float averages to detect and return table type"""
    # TODO: If use this, can do soup.find("th",string=re.compile("δ")).find("sub",string=re.compile("C"))
    Carbon = soup.find(
        "sub", string=re.compile("C")
    )  # Don't use findall, look in through th for <sub> w/ string='C'or'H'
    Proton = soup.find("sub", string=re.compile("H"))
    if Carbon and Proton:
        return "Both H1/C13 NMR Table Detected!"
    elif Carbon:
        return "C13 NMR Table Detected!"
    elif Proton:
        return "H1 NMR Table Detected!"
    else:
        for item in d2list:
            for value in item:
                if re.search(
                    r"(\d*[0-9]\.\d*[0-9]\,\s{1}\w*[s,t,d,m,q,b,r]\s{1})|(\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\))",
                    value,
                ):
                    HNMR_Search = True
                elif re.search(
                    r"(\d*[0-9]\.\d*[0-9])(\,\sCH3|\,\sCH2|\,\sCH|\,\sC)", value
                ):
                    CNMR_Search = True
                else:
                    continue
        if HNMR_Search and CNMR_Search:
            return "Both H1/C13 NMR Detected! - From Cells!"
        elif HNMR_Search and not CNMR_Search:
            return "H1 NMR Detected! -  From Cells!"
        elif CNMR_Search and not HNMR_Search:
            return "H1 NMR Table Detected! - From cells"
        else:
            average_list = []
            for item in float_d2list:
                value_list = []
                for value in item:
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
                return "Both H1/C13 NMR Detected! - From chemical shifts!"
            elif HNMR and not CNMR:
                return "H1 NMR Detected! -  From chemical shifts!"
            elif CNMR and not HNMR:
                return "H1 NMR Table Detected! - From chemical shifts!"
            else:
                return None


def column_id_cleaner_list(d2_list):
    """Takes 2dlist of columns . Searchs cells first for regex patterns to detect if column will contain H/C NMR, then each cell for regex patterns"""
    # Regex patterns; detect the table type to determine which column type
    # TODO: Add other possible multiplicity regex patterns
    # 1. Other less common H splitting pattern

    CNMR_pattern_1 = re.compile(r"\,\sCH3|\,\sCH2|\,\sCH|\,\sC")
    CNMR_pattern_2 = re.compile(r"CH3|CH2|CH|C")
    regex_pattern_1 = re.compile(r"Î´C")
    regex_pattern_2 = re.compile(r"Î´H")
    HNMR_pattern_1 = re.compile(
        r"(\,{1}\s\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?|\,{1}\s\w*[stdmqbrqh]\s?|\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\,?\))"
    )
    HNMR_pattern_2 = re.compile(
        r"(\s?\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?\([0-9]+\.[0-9]\)|\s?\w*[stdmqbrqh]\s?\([0-9]+\.[0-9](?:\,\s?[0-9]+\.[0-9])*\,?\)|\s?\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?\([0-9]+\.[0-9](?:\,\s?[0-9]+\.[0-9])*\,?\)|\s?\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?|\s?\w*[stdmqbrqh]\s?)"
    )
    HNMR_pattern_2a = re.compile(
        r"(\s?\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?$|\s?\w*[stdmqbrqh]\s?$)"
    )

    HNMR_pattern_2b = re.compile(
        r"(\s\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?\([0-9]+\.[0-9]\)|\s\w*[stdmqbrqh]\s?\([0-9]+\.[0-9](?:\,\s?[0-9]+\.[0-9])*\)|\s\w*[stdmqbrqh]\s?\w*[stdmqbrqh]\s?\([0-9]+\.[0-9](?:\,\s?[0-9]+\.[0-9])*\))"
    )
    HNMR_pattern_2ba = re.compile(r"(?<=\()([^\)]+)(?=\))")
    HNMR_pattern_2bb = re.compile(r"(\w*[stdmqbrqh]\s?\w*[stdmqbrqh]|\w*[stdmqbrqh])")

    C_type = []
    Carbon_spec = []
    H_spec = []
    H_multiplicity_J = []
    for item in d2_list:
        c_type1 = []
        Carbon_spec1 = []
        H_spec1 = []
        H_multiplicity_J1 = []

        for value in item:
            if CNMR_pattern_1.search(
                value
            ):  # if CNMR_pattern_1 found with .search regex:
                c_type1.append(
                    CNMR_pattern_2.search(value).group()
                )  # append item to new list
                Carbon_spec1.append(
                    CNMR_pattern_1.sub("", value)
                )  # while removing from original by adding everything but pattern to new list
            elif HNMR_pattern_1.search(value):  # Same as CNMR, but for HNMR
                H_multiplicity_J1.append(HNMR_pattern_2.search(value).group())
                H_spec1.append(HNMR_pattern_1.sub("", value))
            elif (
                "" == value
            ):  # elif " "(blank space, could be from regex search; append to list, but keep in original
                c_type1.append(value)
                Carbon_spec1.append(value)
                H_spec1.append(value)
                H_multiplicity_J1.append(value)
            else:
                None
        # Removing irrelevant list, also replacing dict with new cleaned chemical shift column
        if all_same(c_type1) == False:
            C_type.append(c_type1)
        if all_same(Carbon_spec1) == False:
            Carbon_spec.append(Carbon_spec1)
        if all_same(H_multiplicity_J1) == False:
            H_multiplicity_J.append(H_multiplicity_J1)
        if all_same(H_spec1) == False:
            H_spec.append(H_spec1)

    # Split up coupling and multiplicity into separate lists
    J_coupling = []
    H_multiplicity = []
    for compound in H_multiplicity_J:
        J_coupling1 = []
        H_multiplicity1 = []
        for val in compound:
            if HNMR_pattern_2b.search(val):
                J_coupling1.append(HNMR_pattern_2ba.search(val).group())
                H_multiplicity1.append(HNMR_pattern_2bb.search(val).group())
            elif HNMR_pattern_2a.search(val):
                H_multiplicity1.append(HNMR_pattern_2bb.search(val).group())
                J_coupling1.append("")
            elif "" == val:
                J_coupling1.append(val)
                H_multiplicity1.append(val)
        J_coupling.append(J_coupling1)
        H_multiplicity.append(H_multiplicity1)
    return H_spec, Carbon_spec, H_multiplicity, J_coupling, C_type


def column2dlist_string_to_float(d2_list):
    """ Takes 2dlist that has been cleaned by column_id_cleaner()(or any dictionary), will just take decimal number
    if string begins with it (regex pattern(^\d*[0-9].{1}\d*[0-9]) recognized) and convert to float in a new list
    INPUT: 2dlist
    OUTPUT: returns 2dlist with float numbers if regex pattern recognized"""
    float_pattern = re.compile(r"(^\d*[0-9].{1}\d*[0-9])")
    new_result = []
    for item in d2_list:
        spec_float1 = []
        for value in item:
            if float_pattern.search(value):
                for spec_value in float_pattern.findall(value):
                    spec_float1.append(spec_value)
            elif "" == value:
                spec_float1.append(value)
        if all_same(spec_float1) == False:
            spec_results = []
            for i in spec_float1:
                if not if_blank(i):
                    spec_results.append(float(i))
                elif "" == i:
                    spec_results.append(i)
            new_result.append(spec_results)
    return new_result


def data_to_grid(numcomps, aindex, cspec, ctype, hspec, hmult, hcoup):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_ctype,{0}_hspec,{0}_multi,{0}_coupling"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], ctype[j], hspec[j], hmult[j], hcoup[j]])
    return headers, data


def data_to_grid_Ca(numcomps, aindex, hspec, hmult, hcoup):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_hspec,{0}_multi,{0}_coupling"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([hspec[j], hmult[j], hcoup[j]])
    return headers, data


def data_to_grid_Cb(numcomps, aindex, cspec, hspec, hmult, hcoup):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_hspec,{0}_multi,{0}_coupling"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], hspec[j], hmult[j], hcoup[j]])
    return headers, data


#  TODO: def function for each H/C if only one type
def data_to_grid_Ha(numcomps, aindex, cspec, ctype):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_ctype,"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], ctype[j]])
    return headers, data


def data_to_grid_Hb(numcomps, aindex, cspec, ctype, hspec, hcoup):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_ctype,{0}_hspec,{0}_coupling"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], ctype[j], hspec[j], hcoup[j]])
    return headers, data


def data_to_grid_Hc(numcomps, aindex, cspec, ctype, hspec):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_ctype,{0}_hspec"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], ctype[j], hspec[j]])
    return headers, data


def data_to_grid_Hd(numcomps, aindex, cspec, ctype, hspec, hmult):
    headers = ["atom_index"]
    data = [aindex]
    hstring = "{0}_cspec,{0}_ctype,{0}_hspec,{0}_multi"
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)
    for j in range(numcomps):
        data.extend([cspec[j], ctype[j], hspec[j], hmult[j]])
    return headers, data


def tableto_csv(headers, data, filename):
    rows = zip(*data)
    with open(filename, "w", encoding="UTF-8", newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)
        for row in rows:
            wr.writerow(row)


def get_float_avg(dict2):
    average_list = []
    cspec = []
    hspec = []

    for item in dict2:
        value_list = []
        for value in item:
            if type(value) == float:
                value_list.append(value)
        if not all_same(value_list):
            average = sum(value_list) / len(value_list)
            average_list.append(average)
            if 14.0 <= average <= 250.0:
                cspec.append(list(item))
            elif 0.0 <= average <= 13.5:
                hspec.append(list(item))
    return cspec, hspec

