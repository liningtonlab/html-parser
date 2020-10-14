# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""
# Use this file as a personal testing group to make sure all the functions
# work (return what you expect) and work as part of the overall data pipeline
from pprint import pprint  # Pretty Printer
from pathlib import Path
from nmr_html_parser import souping


def main():

    # The ultimate aim here is to create a function which takes as an input and HTML file
    # and writes the output file somewhere
    inp_file = Path(r"C:\Users\maras\Desktop\JNP_html_tables\terps.html")
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    # You call these functions but do nothing with them
    # And don't store the returns
    souping.num_columns(headers)
    comps = souping.soup_comp_id(soup)
    # Used stored results from previous function calls to run
    columns = souping.get_columns(rows, headers)
    compound_num = souping.compound_number(comps,headers)
    print(rows)
    print(columns)
    print(headers)
    print(comps)
    print(compound_num)



# Best practice to use this for scripts
if __name__ == "__main__":
    main()
