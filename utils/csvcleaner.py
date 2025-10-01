import csv
import argparse

def clean_csv(input_file, output_file):
    columns = [3, 8, 9]

    with open(input_file, "r", newline="") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        for row in reader:
            if len(row) == 0 or row[0].lower() == "version":
                continue

            new_row = [row[i] if i < len(row) else "" for i in columns]
            writer.writerow(new_row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    clean_csv(args.input_file, args.output_file)
    print(f"Cleaned CSV saved to {args.output_file}")

if __name__ == "__main__":
    main()

