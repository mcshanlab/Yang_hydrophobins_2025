import os
import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import sys
import io

def find_classI_folders(base_dir):
    """Find folders containing 'classI_' in the name."""
    classI_folders = []
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if 'classI_' in d:
                classI_folders.append(os.path.join(root, d))
    return classI_folders

def load_excel_files(folder):
    """Load all Excel and CSV files from the folder."""
    excel_data = {}
    species_data = []
    for file in os.listdir(folder):
        if file.endswith(('.xlsx', '.xls', '.csv')):
            path = os.path.join(folder, file)
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)

                # Load descriptions
                if "Description" in df.columns:
                    descs = df["Description"].dropna().tolist()
                    excel_data[file] = descs

                # Collect species names if present
                if "Scientific Name" in df.columns:
                    species = df["Scientific Name"].dropna().tolist()
                    species_data.extend(species)

            except Exception as e:
                print(f"Failed to read {path}: {e}")
    return excel_data, species_data

def compare_descriptions(all_descriptions, species_list, text_output_path, pdf_output_path):
    """Compare Description columns and summarize species."""
    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    try:
        description_map = defaultdict(set)
        file_hit_counts = {}

        for file, descriptions in all_descriptions.items():
            file_hit_counts[file] = len(descriptions)
            for desc in descriptions:
                description_map[desc].add(file)

        shared = {}
        unique = {}

        for desc, files in description_map.items():
            if len(files) > 1:
                shared[desc] = files
            else:
                unique[desc] = files

        print("\n📊 Hit count summary per file:")
        for file, count in sorted(file_hit_counts.items(), key=lambda x: -x[1]):
            print(f"{file}: {count} descriptions")

        file_summary = defaultdict(lambda: {'shared': 0, 'unique': 0})
        for desc, files in description_map.items():
            if len(files) > 1:
                for f in files:
                    file_summary[f]['shared'] += 1
            else:
                only_file = next(iter(files))
                file_summary[only_file]['unique'] += 1

        print("\n📈 Total hits (Shared + Unique) per file:")
        for f in sorted(file_summary.keys()):
            total_hits = file_summary[f]['shared'] + file_summary[f]['unique']
            print(f"{f}: {total_hits} total hits (Shared: {file_summary[f]['shared']}, Unique: {file_summary[f]['unique']})")

        print("\n✅ Descriptions in MULTIPLE files:")
        for desc, files in shared.items():
            print(f"\nDescription: {desc}")
            print(f"Found in: {', '.join(sorted(files))}")

        print("\n🔹 Descriptions UNIQUE to one file:")
        for desc, files in unique.items():
            print(f"\nDescription: {desc}")
            print(f"Only in: {next(iter(files))}")

        total_unique_hits = len(unique)
        print(f"\n🧮 Total number of UNIQUE hits across all files: {total_unique_hits}")

        # === Species Summary ===
        print("\n🧬 Species occurrence summary:")
        species_counter = Counter(species_list)
        for species, count in species_counter.most_common():
            print(f"{species}: {count} hits")

        # === Plotting shared vs unique hits ===
        files = sorted(file_summary.keys())
        shared_counts = [file_summary[f]['shared'] for f in files]
        unique_counts = [file_summary[f]['unique'] for f in files]

        def shorten_filename(fname):
            parts = fname.split('_')
            if len(parts) > 1:
                short = parts[1]
            else:
                short = fname.split('.')[0]
            return short.upper()

        short_labels = [shorten_filename(f) for f in files]

        plt.figure(figsize=(10, 6))
        plt.bar(short_labels, shared_counts, label='Shared', color='#4A90E2')
        plt.bar(short_labels, unique_counts, bottom=shared_counts, label='Unique', color='#E94F37')

        plt.title('Shared vs. Unique Description Hits per File', fontsize=14, weight='bold')
        plt.xlabel('Dataset', fontsize=12)
        plt.ylabel('Number of Foldseek hits', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.legend()
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.savefig(pdf_output_path)
        plt.close()

    finally:
        sys.stdout = sys_stdout
        with open(text_output_path, 'w') as f:
            f.write(buffer.getvalue())

def main():
    base_dir = os.getcwd()
    folders = find_classI_folders(base_dir)

    all_descriptions = {}
    all_species = []

    for folder in folders:
        print(f"\n📁 Scanning folder: {folder}")
        files_data, species_data = load_excel_files(folder)
        all_descriptions.update(files_data)
        all_species.extend(species_data)

    text_output_path = os.path.join(base_dir, "classI_foldseek_description_hits_summary.txt")
    pdf_output_path = os.path.join(base_dir, "classI_foldseek_description_hits_summary.pdf")

    compare_descriptions(all_descriptions, all_species, text_output_path, pdf_output_path)

    print(f"Text results saved to: {text_output_path}")
    print(f"Graph saved as PDF: {pdf_output_path}")

if __name__ == "__main__":
    main()
