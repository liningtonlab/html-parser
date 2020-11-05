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
    inp_file = Path("html_files/type11.html") # This example has no C/CH/CHn in Carbon column
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)
    compound_num = souping.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping.get_columns(rows, headers)

    print(headers)
    print(comps)
    print(compound_num)
    print(columns)

    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(columns)
    float_hspec = souping.column2dlist_string_to_float(hspec)
    float_cspec = souping.column2dlist_string_to_float(cspec)

    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)
    if float_cspec and float_hspec:
        souping.tableto_csv(*souping.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))
    elif not float_cspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec,hspec = souping.get_float_avg(columns)
        float_cspec = cspec
        ctype = souping.blanks_list(float_cspec)
    elif not float_hspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec, hspec = souping.get_float_avg(columns)
        float_hspec = hspec
        hmult,jcoup = souping.blanks_list(float_hspec) # might have to make variables separate
    print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)

    # Turn compound tables into CSV
    #  TODO: def function for each H/C if only one type
    if float_cspec and float_hspec:
        souping.tableto_csv(*souping.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup))
    elif not float_cspec:
        souping.tableto_csv(*souping.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup))
    # Means have neither cspec or ctype after using float avg search. Add everything but float_cpsec/ctype
    elif not ctype:
       souping.tableto_csv(*souping.data_to_grid_Cb(compound_num,float_cspec, atom_index, float_hspec, hmult, jcoup))
    # Means have float_cspec, but not ctype. Add everything but ctype

    elif not float_hspec:
        souping.tableto_csv(*souping.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype))
    elif not hmult:
        souping.tableto_csv(*souping.data_to_grid_Hb(compound_num, atom_index, float_cspec, ctype, float_hspec, jcoup))
    elif not jcoup:
        souping.tableto_csv(*souping.data_to_grid_Hc(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult))
    elif not hmult and jcoup:
        souping.tableto_csv(*souping.data_to_grid_Hc(compound_num, atom_index, float_cspec, ctype, float_hspec))
    # Then the cases for Proton
    # if not float_hspec:
    # all but float_hspec,hmulti,jcoup
    # if not hmulti:
    # all but hmulti
    # if not jcoup:
    # all but jcoup
    # if not hmulti and jcoup:
    # all but hmulti,jcoup
    # Need four functions, one for each case

# Best practice to use this for scripts
if __name__ == "__main__":
    main()
