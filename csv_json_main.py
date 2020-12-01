from nmr_html_parser import csv_to_json

# File_paths
csv = "nmr_html_parser/table_example.csv"


csv_reader_dict = csv_to_json.input_file(csv)

condensed_dict = csv_to_json.csv_dict_reader_extraction(csv_reader_dict)
print(condensed_dict)
comps_data = csv_to_json.dictionary_parser(2, condensed_dict)

json_structured_output = csv_to_json.json_structuring(comps_data, condensed_dict)
print(json_structured_output)

csv_to_json.json_dump(json_structured_output, "table_test_output.json")