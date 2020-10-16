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
    inp_file = Path("./html_files/terps.html")
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    # You call these functions but do nothing with them
    # And don't store the returns
    souping.num_columns(headers)
    comps = souping.soup_comp_id(soup)
    compound_num = souping.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping.get_columns(rows, headers)

    # TODO: implement parsing logic for data types
    # You don't have to do you all at once, so just start on the carbon detection
    # Now that we have all the columns, we want to split this into atom_index, data columns (C and/or H), and other
    # I would do something like the following
    # Make sure to filter out empty rows within a given column
    # atom_index_column, atom_index_idx = souping.get_atom_index_column(columns)
    # for idx, col in enumerate(columns):
        # 1. If atom index, ignore because we detected this about
        # if idx == atom_index_idx:
            # continue
        # 2. Detect if C or H (you can use the headers to help with this)
        # And parse appropriately into dict output
        # col_type = souping.detect_column_type(headers, idx, col)
        # if col_type == "carbon":
            # data = souping.parse_carbon_column(atom_index_column, col)
        # elif col_type == "proton":
            # data = souping.parse_proton_column(atom_index_column, col)
        # else:
            # print("Probably not a data column")
            # This is either because of bad detection or just a non-useful column

        # You'll also need some sort of mechanism for sorting the data from the above
        # loop into the appropriate compounds

    column_parse = souping.column_parser_splitcomma(columns)
    tester = souping.column_parser_Carbonclean(column_parse)
    # print(rows)
    # print(columns)
    print(headers)
    print(comps)
    # print(compound_num)
    # print(column_parse)
    # print(tester)


# Best practice to use this for scripts
if __name__ == "__main__":
    main()
