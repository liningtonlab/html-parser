# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""
# Use this file as a personal testing group to make sure all the functions
# work (return what you expect) and work as part of the overall data pipeline

from pprint import pprint  # Pretty Printer
from pathlib import Path
from nmr_html_parser import souping_work


def main():
    # The ultimate aim here is to create a function which takes as an input and HTML file
    # and writes the output file somewhere
    inp_file = Path("tests/inputs/test_CNMR_ONLY.html") # This example has no C/CH/CHn in Carbon column
    soup = souping_work.inputs(inp_file)
    headers = souping_work.soup_id_headers(soup)

    rows = souping_work.soup_id_rows(soup)
    comps = souping_work.soup_comp_id(soup)
    compound_num = souping_work.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping_work.get_columns(rows, headers)

    print(headers)
    print(comps)
    print(compound_num)
    print(columns)

    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping_work.column_id_cleaner_list(columns)

    float_hspec = souping_work.column2dlist_string_to_float(hspec)
    if len(float_hspec) < 1:
        float_hspec = False
    float_cspec = souping_work.column2dlist_string_to_float(cspec)

    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)
    #if float_cspec and float_hspec:
       # souping_work.tableto_csv(*souping_work.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))
    if not float_cspec:
        columns = souping_work.column2dlist_string_to_float(columns)
        float_cspec,float_hspec = souping_work.get_float_avg(columns)
        ctype = souping_work.blanks_list(float_cspec)
    if not float_hspec:
        columns = souping_work.column2dlist_string_to_float(columns)
        float_cspec, hspec = souping_work.get_float_avg(columns)
        if hspec:
            float_hspec = hspec
            hmult = souping_work.blanks_list(float_hspec)
            jcoup = souping_work.blanks_list(float_hspec)

    # might have to make variables separate
    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)

    #souping_work.tableto_csv(*souping_work.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))

    # Turn compound tables into CSV
    #  TODO: def function for each H/C if only one type
    if float_cspec and float_hspec and not ctype:
        souping_work.tableto_csv(*souping_work.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup))
    elif float_cspec and float_hspec:
        souping_work.tableto_csv(*souping_work.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))
    elif not float_hspec:
        souping_work.tableto_csv(*souping_work.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype))
    elif float_hspec and not hmult and not jcoup:
       souping_work.tableto_csv(*souping_work.data_to_grid_Hb(compound_num, atom_index, float_cspec, ctype, float_hspec))
    elif not float_cspec:
        souping_work.tableto_csv(*souping_work.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup))
    elif not ctype:
       souping_work.tableto_csv(*souping_work.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup))



# Best practice to use this for scripts
if __name__ == "__main__":
    main()
