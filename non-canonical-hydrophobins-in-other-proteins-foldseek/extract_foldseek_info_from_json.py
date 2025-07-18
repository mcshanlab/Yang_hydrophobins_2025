import os
import json
from collections import defaultdict
import pandas as pd

def filter_descriptions(input_json_path):
    with open(input_json_path, 'r') as f:
        data = json.load(f)

    results_by_db = defaultdict(list)

    for entry in data:
        for result in entry.get("results", []):
            db = result.get("db", "unknown-db")
            alignments = result.get("alignments", {})

            for alignment_group in alignments.values():
                for alignment in alignment_group:
                    description = alignment.get("description", "")
                    desc_lower = description.lower()
                    prob = alignment.get("prob", "")

                    try:
                        if float(prob) < 0.1:
                            continue
                    except (ValueError, TypeError):
                        continue

                    if "hydrophobin" in desc_lower and \
                       "hydrophobin-domain-containing protein" not in desc_lower:
                        continue

                    if ("uncharacterized protein" in desc_lower or
                        "fruiting body" in desc_lower or
                        "cerato-ulmin" in desc_lower or
                        "cryparin" in desc_lower):
                        continue

                    result_entry = {
                        "DB": db,
                        "Target": alignment.get("target", ""),
                        "Description": description,
                        "Scientific Name": alignment.get("taxName", ""),
                        "Prob.": prob,
                        "Seq. Id.": alignment.get("seqId", ""),
                        "E-Value": alignment.get("eval", "")
                    }
                    results_by_db[db].append(result_entry)

    return results_by_db

def export_results_to_excel(results_by_db, output_path):
    all_entries = []
    for db, entries in results_by_db.items():
        all_entries.extend(entries)

    if not all_entries:
        print(f"No valid entries to export for {output_path}")
        return

    df = pd.DataFrame(all_entries)
    df.to_excel(output_path, index=False)
    print(f"Results exported to {output_path}")

if __name__ == "__main__":
    base_dir = os.getcwd()

    for folder in os.listdir(base_dir):
        full_path = os.path.join(base_dir, folder)
        if not os.path.isdir(full_path):
            continue

        for file in os.listdir(full_path):
            if file.endswith(".json"):
                input_json_path = os.path.join(full_path, file)
                print(f"Processing {input_json_path}")

                filtered_results = filter_descriptions(input_json_path)

                # Save the XLSX in the same folder as the JSON file
                json_dir = os.path.dirname(input_json_path)
                base_name = os.path.splitext(file)[0]
                output_filename = f"{base_name}_filtered.xlsx"
                output_path = os.path.join(json_dir, output_filename)

                export_results_to_excel(filtered_results, output_path)
