import csv
import glob

def join_csv_files(file_paths, output_path):
    # Open the first file to get headers
    with open(file_paths[0], newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

    with open(output_path, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(headers)

        for file_path in file_paths:
            with open(file_path, newline='', encoding='utf-8') as in_file:
                reader = csv.reader(in_file)
                next(reader)  # Skip header
                for row in reader:
                    writer.writerow(row)

if __name__ == "__main__":
    # Example: join all CSV files in the current directory
    csv_files = glob.glob("input/*.csv")
    join_csv_files(csv_files, "joined_output.csv")