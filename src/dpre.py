#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from scipy.stats import zscore
from sklearn.preprocessing import MinMaxScaler
import sys
import subprocess

# Check for null values
def check_nulls(df):
    print("Null values in each column:")
    print(df.isnull().sum())

# Check for duplicate rows
def check_duplicates(df):
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    return df.drop_duplicates()

# Remove outliers using Z-score
def remove_outliers(df):
    z_scores = zscore(df.select_dtypes(include=['number']))
    df_cleaned = df[(z_scores < 3).all(axis=1)]
    print(f"Shape after removing outliers: {df_cleaned.shape}")
    return df_cleaned

# Normalize data using MinMaxScaler
def normalize_data(df):
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(df.select_dtypes(include=['number'])), columns=df.select_dtypes(include=['number']).columns)
    print("Data normalized (scaled between 0 and 1).")
    return df_normalized

# Bin the 'Age' column into intervals
def bin_age(df):
    bins = [18, 35, 50, 70]  # Age intervals
    labels = ['Young Adult', 'Middle Aged', 'Senior']  # Labels
    if 'Age' in df.columns:
        df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels)
        print("Age column binned into categories.")
    else:
        print("Age column not found in the dataset.")
    return df

# Save the cleaned and processed data to a CSV file
def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Processed data saved to {file_path}")

# Run the next script (eda.py)
def run_eda(file_path):
    subprocess.run(["python3", "eda.py", file_path])

if __name__ == "__main__":
    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python dpre.py <file_path>")
        sys.exit(1)
    
    # Read the input file
    file_path = sys.argv[1]
    df = pd.read_csv(file_path)
    
    # Perform data cleaning and processing
    check_nulls(df)
    df = check_duplicates(df)
    df = remove_outliers(df)
    df_normalized = normalize_data(df)
    df = bin_age(df)
    
    # Save the processed DataFrame to a new CSV file
    output_path = "res_dpre.csv"
    save_to_csv(df, output_path)
    
    # Run the next script (eda.py)
    run_eda(output_path)
