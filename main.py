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
    inp_file = Path("html_files/test_example_1.html") # This example has no C/CH/CHn in Carbon column
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
    if not float_cspec:
        columns = souping_V2.column2dlist_string_to_float(columns)
        cspec1,hspec1 = souping_V2.get_float_avg(columns)
        float_cspec = cspec1
        ctype = souping_V2.blanks_list(float_cspec)
    elif not float_hspec:
        columns = souping_V2.column2dlist_string_to_float(columns)
        cspec1, hspec1 = souping_V2.get_float_avg(columns)
        float_hspec = hspec1
        hmult,jcoup = souping_V2.blanks_list(float_hspec) # might have to make variables separate
    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)
    # Turn compound tables into CSV
    #souping_V2.tableto_csv(*souping_V2.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup))
    #  TODO: def function for each H/C if only one type
   # if not float_cspec or ctype:
        #souping_V2.tableto_csv(*souping_V2.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup))
        # Means have neither cspec or ctype after using float avg search. Add everything but float_cpsec/ctype
   # if not ctype:
        #souping_V2.tableto_csv(*souping_V2.data_to_grid_Cb(compound_num,float_cspec, atom_index, float_hspec, hmult, jcoup))
        # Means have float_cspec, but not ctype. Add everything but ctype

        # Need two functions, one for each case that takes the according amount of variable to add to CSV
    # Then the cases for Proton
    #if not float_hspec:
        # all but float_hspec,hmulti,jcoup
    #if not hmulti:
        #all but hmulti
   # if not jcoup:
        #all but jcoup
    #if not hmulti and jcoup:
        # all but hmulti,jcoup

        # Need four functions, one for each case
    if float_cspec and float_hspec:
        souping_V2.tableto_csv(*souping_V2.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))

# Best practice to use this for scripts
if __name__ == "__main__":
    main()
