from nmr_html_parser import csv_to_json
import pprint

# File_paths
import glob


def main():
    for csv in sorted(glob.glob("tests/outputs_acs/*csv")):
        print(csv)
        if "ai" in csv:
            print("SKIPPING MULTI ATOM INDEX")
            continue
        csv_reader_dict = csv_to_json.input_file(csv)
        condensed_dict = csv_to_json.csv_dict_reader_extraction(csv_reader_dict)
        # Applies changes inplace
        print(condensed_dict)
        csv_to_json.merge_atom_indices(condensed_dict)
        print(condensed_dict)

        def parse_key(k):
            try:
                return int(k.split("_")[0])
            except:
                return -1

        num_comp = max((parse_key(k) for k in condensed_dict.keys()))
        comps_data = csv_to_json.dictionary_parser(num_comp, condensed_dict)

        json_structured_output = csv_to_json.json_structuring(
            comps_data, condensed_dict
        )
        pprint.pprint(json_structured_output)

        # csv_to_json.json_dump(json_structured_output, "table_test_output.json")


if __name__ == "__main__":
    main()
