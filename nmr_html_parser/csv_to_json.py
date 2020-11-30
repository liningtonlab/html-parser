import csv, json


# File_paths
csvFilePath = "table_example.csv"
jsonFilePath = "happy.json"


def no_blank(input_string):
    if input_string == "":
        return False
    else:
        return True


# CSV reformatting to structure for JSON
#def input_file(filepath)
with open(csvFilePath, encoding="UTF-8") as csvFile:
    csvReader = csv.DictReader(csvFile)
    new_dict = {}
    for d in list(csvReader):
        for k, v in d.items():
            if k in new_dict:
                new_dict[k] = new_dict[k] + [v]
            else:
                new_dict[k] = [v]
    #  print(new_dict)  # New dictionary created


    def dictionary_parser(num_comps):
        comps_shift_data = {}
        for i in range(1,num_comps + 1):
            possible_variables = [
                str(i) + "_cspec",
                str(i) + "_hspec",
                str(i) + "_multi",
                str(i) + "_coupling"]

            found_variables = {
                key: val for key, val in new_dict.items() if key in possible_variables and bool(new_dict.get(k))}

            comps_shift_data["compound_"+str(i)] = found_variables
        return comps_shift_data


    comps_data = dictionary_parser(2)


    #  Collect nmr data together
    def c_nmr_shift_creator(shifts_list, atom_input_list):
        return [({"shift": shift, "atom_index": atom})
                for shift, atom in zip(shifts_list, atom_input_list) if no_blank(shift)]

    def h_nmr_shift_multi_coup_creator(shifts_list, multi_list, coup_list, atom_input_list):
        return [({"shift": shift, "atom_index": atom, "multiplicity": multi, "coupling": coup})
                for shift, atom, multi, coup in zip(shifts_list, multi_list, coup_list, atom_input_list)
                if no_blank(shift)]


    #if new_dict["residues"]:
    #else: new_dict["atom_index"]
    #print(shift_creator(shift_comps["compound_"+str(index+1)][str(index+1)+"_cspec"], new_dict["atom_index"]))

    # New Nested template dictionary for each compound, that becomes list of dictionaries in the end
    list_comp_dictionary = []
    # iterating over each compound
    for index, (kk, vv) in enumerate(comps_data.items()):
        comp_dictionary = {}
        comp_dictionary["name"] = kk
        comp_dictionary["c_nmr"] = {"spectrum":c_nmr_shift_creator(comps_data["compound_" + str(index + 1)][str(index + 1) + "_cspec"], new_dict["atom_index"])}
        comp_dictionary["h_nmr"] = {"spectrum":h_nmr_shift_multi_coup_creator(
            comps_data["compound_" + str(index + 1)][str(index + 1) + "_cspec"],
            new_dict["atom_index"],
            comps_data["compound_" + str(index + 1)][str(index + 1) + "_multi"],
            comps_data["compound_" + str(index + 1)][str(index + 1) + "_coupling"])}

        list_comp_dictionary.append(comp_dictionary)

    print(list_comp_dictionary)


    # Structured format for JSON output (list of dictionaries)
    data = [
        {"name": "Compound 1",
            "smiles": None,
            "c_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {"shift": 118.6,
                     "atom_index": 2},
                    {"shift": 117.5,
                     "atom_index": 3}
                ]
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {
                        "shift": 4.76,
                        "atom_index": 2,
                        "multiplicity": "d",
                        "coupling": [9.8]
                    },
                    {
                        "shift": 5.73,
                        "atom_index": 3,
                        "multiplicity": "d",
                        "coupling": [9.9]
                    }
                ]
            }
        },
        {"name": "Compound 2",
         "smiles": None,
         "c_nmr": {
             "solvent": None,
             "temperature": None,
             "reference": None,
             "frequency": None,
             "spectrum": [
                 {"shift": 117.6,
                  "atom_index": 2},
                 {"shift": 117.0,
                  "atom_index": 3}
             ]
         },
         "h_nmr": {
             "solvent": None,
             "temperature": None,
             "reference": None,
             "frequency": None,
             "spectrum": [
                 {
                     "shift": 5.67,
                     "atom_index": 3,
                     "multiplicity": "d",
                     "coupling": [9.9]
                 }
             ]
         }
         }
    ]


    # JSON dump
    with open("table_test_output.json", "w") as f:
        # json.dump(data, f)
        # nicer output
        f.write(json.dumps(data, indent=2))  # indent=2 instead of just f.
