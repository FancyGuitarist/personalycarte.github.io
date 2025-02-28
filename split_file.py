import pandas as pd

# quick function to split a file in 3 parts
def split_file(input_file, output_path):
    df = pd.read_csv(input_file, delimiter=",", header=None, encoding='utf-8')
    
    total_lines = len(df)
    part_size = total_lines // 3
    
    parts = [df.iloc[:part_size], df.iloc[part_size:2*part_size], df.iloc[2*part_size:]]
    
    for i, part in enumerate(parts, start=1):
        output_file = output_path + f"_{i}.txt"
        part.to_csv(output_file, index=False, header=False, encoding='utf-8')
        print(f"Fichier {output_file} créé avec {len(part)} lignes.")

# quick function to take three files and merge them into one
def merge_files(input_files, output_file): # not tested yet !!
    df = pd.concat([pd.read_csv(f, delimiter=",", header=None, encoding='utf-8') for f in input_files])
    df.to_csv(output_file, index=False, header=False, encoding='utf-8')
    print(f"Fichier {output_file} créé avec {len(df)} lignes.")


# Exemple d'utilisation
if __name__ == "__main__":
    split_file("Data\RTC\googletransit\stop_times.txt", "Data\RTC\googletransit\stop_times")