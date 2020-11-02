# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""
# Use this file as a personal testing group to make sure all the functions
# work (return what you expect) and work as part of the overall data pipeline

from pprint import pprint  # Pretty Printer
from pathlib import Path
from nmr_html_parser import souping_V2


def main():
    # The ultimate aim here is to create a function which takes as an input and HTML file
    # and writes the output file somewhere
    inp_file = Path("html_files/test_example_2.html")
    soup = souping_V2.inputs(inp_file)
    headers = souping_V2.soup_id_headers(soup)
    rows = souping_V2.soup_id_rows(soup)
    comps = souping_V2.soup_comp_id(soup)
    compound_num = souping_V2.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping_V2.get_columns(rows, headers)

    print(headers)
    print(comps)
    print(compound_num)
    print(columns)

    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping_V2.column_id_cleaner_list(columns)
    float_hspec = souping_V2.column2dlist_string_to_float(hspec)
    float_cspec = souping_V2.column2dlist_string_to_float(cspec)
    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)

    # Turn compound tables into CSV
    souping_V2.tableto_csv(*souping_V2.data_to_grid(compound_num, atom_index, float_hspec, float_cspec, hmult, jcoup, ctype))

# Best practice to use this for scripts
if __name__ == "__main__":
    main()
