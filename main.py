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
    # Function which takes as an input and HTML file and writes output .csv file
    inp_file = Path("tests/inputs/test_1.html")

    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    columns = souping.get_columns(rows, headers)
    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(columns)
    float_hspec = souping.column2dlist_string_to_float(hspec)
    float_cspec = souping.column2dlist_string_to_float(cspec)

    print(headers)
    print(comps)
    print(compound_num)
    print(columns)
    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)

    # 1. First check for float_spec
    if float_cspec and float_hspec:
       souping.tableto_csv(*souping.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))

    # 1A. If not either spec, with columns containing specific data check float averages as last resort.
    elif not float_cspec:
        columns = souping.column2dlist_string_to_float(columns)
        float_cspec,float_hspec = souping.get_float_avg(columns)
        ctype = souping.blanks_list(float_cspec)
    elif not float_hspec:
        columns = souping.column2dlist_string_to_float(columns)
        float_cspec, hspec = souping.get_float_avg(columns)
        if hspec:
            float_hspec = hspec
            hmult = souping.blanks_list(float_hspec)
            jcoup = souping.blanks_list(float_hspec)
    # 2. Second pass for float of either spec
    if float_cspec and float_hspec and not ctype:
        souping.tableto_csv(*souping.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup))
    elif float_cspec and float_hspec:
        souping.tableto_csv(*souping.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))
    elif not float_hspec:
        souping.tableto_csv(*souping.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype))
    elif float_hspec and not hmult and not jcoup:
       souping.tableto_csv(*souping.data_to_grid_Hb(compound_num, atom_index, float_cspec, ctype, float_hspec))
    elif not float_cspec:
        souping.tableto_csv(*souping.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup))
    elif not ctype:
       souping.tableto_csv(*souping.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup))

# Best practice to use this for scripts
if __name__ == "__main__":
    main()
