import json
import os

#TODO: You must be able to do the below in a prettier way
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from source.databases import fetch_table


def create_datastructure():
    dsk_table = fetch_table("carbon_footprint")

    result = {}

    for i, row in dsk_table.iterrows():
        words : list[str] = row['product'].split(",")
        base = words[0]
        description = ' '.join(words[1:]).strip()
        if description == "": description = None

        res_tuple = (row['id'],row['kg_co2e_pr_kg'],description)

        res_dict = {
            "id" : row['id'],
            "kg_co2e_pr_kg" : row['kg_co2e_pr_kg'],
            "description" : description
        }

        if base in result:
            if description != None:
                result[base].append(res_dict)
        else:
            result[base] = [res_dict]

    result

    base_dir = os.path.dirname(__file__)

    with open(base_dir + "/base_datastructure.json", "w", encoding='utf8') as f:
        result_json = json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False)
        f.write(result_json) 


def main() -> None:
    create_datastructure()


if __name__ == "__main__":
    main()