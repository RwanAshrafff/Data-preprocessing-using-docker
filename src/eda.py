#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import numpy as np
import subprocess
import os

# Ensure the service-result directory exists
if not os.path.exists("service-result"):
    os.makedirs("service-result")

def generate_summary_statistics(df):
    summary_stats = df.describe()
    with open("service-result/summary_statistics.txt", "w") as f:
        f.write("Summary Statistics:\n")
        f.write(str(summary_stats))
    print("Summary statistics saved to 'service-result/summary_statistics.txt'.")

def detect_outliers(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    z_scores = df[numeric_cols].apply(lambda x: (x - x.mean()) / x.std())
    z_score_threshold = 3
    outliers = (z_scores > z_score_threshold) | (z_scores < -z_score_threshold)
    with open("service-result/outliers_z_score.txt", "w") as f:
        f.write("Outliers Detected using Z-Score (Threshold = {}):\n\n".format(z_score_threshold))
        for col in outliers.columns:
            f.write("Column: {}\n".format(col))
            for idx in outliers.index:
                is_outlier = outliers.loc[idx, col]
                if is_outlier:
                    f.write("    - Row {}: Z-Score = {:.2f}\n".format(idx, z_scores.loc[idx, col]))
    print("Outliers detected and saved to 'service-result/outliers_z_score.txt'.")

def analyze_correlation(df):
    # Exclude non-numeric columns from correlation calculation
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    positive_corr = {}
    negative_corr = {}
    for col in corr_matrix.columns:
        for idx, corr in corr_matrix[col].items():
            if col != idx:
                if corr > 0:
                    positive_corr.setdefault(col, []).append((idx, corr))
                elif corr < 0:
                    negative_corr.setdefault(col, []).append((idx, corr))
    with open("service-result/correlation_analysis.txt", "w") as f:
        f.write("Correlation Analysis:\n\n")
        f.write("Positively Correlated Variables:\n")
        for col, correlations in positive_corr.items():
            f.write("    - {}: {}\n".format(col, ", ".join(["{} ({:.2f})".format(var, corr) for var, corr in correlations])))
        f.write("\nNegatively Correlated Variables:\n")
        for col, correlations in negative_corr.items():
            f.write("    - {}: {}\n".format(col, ", ".join(["{} ({:.2f})".format(var, corr) for var, corr in correlations])))

    print("Correlation analysis saved to 'service-result/correlation_analysis.txt'.")

def generate_insights(df):
    # Insight 1: Distribution of Disease Status
    disease_dist = df['Disease_Status'].value_counts(normalize=True) * 100
    insight1 = f"Distribution of Disease Status:\n{disease_dist.to_string()}"
    with open('service-result/eda-in-1.txt', 'w') as f:
        f.write(insight1)
    print("Insight 1 saved to 'service-result/eda-in-1.txt'.")

    # Insight 2: Average BMI by Age Group and Disease Status
    avg_bmi = df.groupby(['Age', 'Disease_Status'])['BMI'].mean().unstack()
    insight2 = f"Average BMI by Age Group and Disease Status:\n{avg_bmi.to_string()}"
    with open('service-result/eda-in-2.txt', 'w') as f:
        f.write(insight2)
    print("Insight 2 saved to 'service-result/eda-in-2.txt'.")

    # Insight 3: Percentage of Smokers by Disease Status
    smoking_dist = df.groupby('Disease_Status')['Smoking_Status'].mean() * 100
    with open('service-result/eda-in-3.txt', 'w') as f:
        f.write("Percentage of Smokers by Disease Status:\n\n")
        f.write(f"0 (No Disease): {smoking_dist[0]:.2f}%\n")
        f.write(f"1 (Has Disease): {smoking_dist[1]:.2f}%\n")
    print("Insight 3 saved to 'service-result/eda-in-3.txt'.")

if __name__ == "__main__":
    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python eda.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    df = pd.read_csv(file_path)

    # Print dataset shape and data types
    print("Dataset shape:", df.shape)
    print("\nData types:")
    print(df.dtypes)

    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Perform EDA tasks
    generate_summary_statistics(df)
    detect_outliers(df)
    analyze_correlation(df)
    generate_insights(df)

    # Run the next script (vis.py)
    subprocess.run(["python3", "vis.py", file_path])
