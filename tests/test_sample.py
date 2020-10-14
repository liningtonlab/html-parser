# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""


from html_parser import souping


a_variable = souping.inputs(r'C:\Users\maras\Desktop\JNP_html_tables\terps.html')

souping.soup_id_headers(a_variable)

souping.num_columns(souping.soup_id_headers(a_variable)) #

souping.soup_comp_id(a_variable)

souping.soup_id_rows(a_variable)

souping.get_columns(souping.soup_id_rows(a_variable), souping.soup_id_headers(a_variable)) #
