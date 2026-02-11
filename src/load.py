import sys
import pandas as pd
import subprocess

def process_data_frame(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Print some information about the DataFrame
    print("DataFrame shape:", df.shape)
    print("DataFrame columns:", df.columns)
    # Pass the DataFrame path to the next Python file for further processing
    subprocess.run(["python3", "dpre.py", file_path])

if __name__ == "__main__":
    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python load.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    process_data_frame(file_path)
