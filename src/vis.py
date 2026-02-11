#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess

if __name__ == "__main__":
    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python vis.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Read the DataFrame from the CSV file
    df = pd.read_csv(file_path)

    # Plot disease prevalence by age group
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    # Group data by Age and calculate the mean Disease_Status
    if 'Age' in df.columns and 'Disease_Status' in df.columns:
        age_disease = df.groupby('Age')['Disease_Status'].mean() * 100
        sns.barplot(x=age_disease.index, y=age_disease.values, palette="viridis")

        # Customize plot
        plt.title('Disease Prevalence by Age Group', fontsize=14, fontweight='bold')
        plt.xlabel('Age Group', fontsize=12)
        plt.ylabel('Percentage with Disease', fontsize=12)
        plt.ylim(0, 100)

        # Save the visualization as vis.png
        plt.savefig('service-result/vis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Visualization saved as 'service-result/vis.png'.")
    else:
        print("Required columns ('Age' and 'Disease_Status') are missing in the dataset.")

    # Run the next script (model.py)
    subprocess.run(["python3", "model.py", file_path])
