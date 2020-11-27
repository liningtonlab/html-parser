import csv,json


# Filepaths
csvFilePath = "table_example.csv"
jsonFilePath = "happy.json"


# CSV reformatting to structure for JSON

with open(csvFilePath,encoding="UTF-8") as csvFile:
  csvReader = csv.DictReader(csvFile)
  new_dict = {}
  for d in list(csvReader):
    for k, v in d.items():
      if k in new_dict:
        new_dict[k] = new_dict[k] + [v]
      else:
        new_dict[k] = [v]
  print(new_dict)






# Structured format for JSON output (list of dictionaries)
  my_data = [{"example - name": "Compound 1"}]
  with open("path/to/file.json", "w") as f:
    json.dump(my_data, f)
    # nicer output
    f.write(json.dumps(my_data, indent=2))

