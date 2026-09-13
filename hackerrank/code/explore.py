import os
import csv
import glob

DATASET_DIR = "dataset"

def summarize_csv(file_path):
    print(f"=== {os.path.basename(file_path)} ===")
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("Empty file")
            return
        rows = list(reader)
        print(f"Row count: {len(rows)}")
        print(f"Columns ({len(header)}): {header}")
        
        # Check nulls/blanks per column
        blanks = [0] * len(header)
        for r in rows:
            for i, val in enumerate(r):
                if val.strip() == "":
                    blanks[i] += 1
        for col, b in zip(header, blanks):
            if b > 0:
                print(f"  Column '{col}' has {b} blank values")
        
        # Sample first 2 rows
        if rows:
            print("Sample row 1:", dict(zip(header, rows[0])))
            if len(rows) > 1:
                print("Sample row 2:", dict(zip(header, rows[1])))
    print()

def main():
    files = sorted(glob.glob(os.path.join(DATASET_DIR, "*.csv")))
    for f in files:
        summarize_csv(f)

if __name__ == "__main__":
    main()
