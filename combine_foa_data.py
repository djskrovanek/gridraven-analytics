import pandas as pd
import os

def combine_foa_data():
    """
    Combines CSV files into a single file.
    All files are merged on the Time column.
    """
    
    # Define the input file paths
    input_dir = "datasets/Summer 2025 analysis/FOAs"
    files = ["M14.csv", "M91.csv", "M80.csv", "M59.csv", "M44.csv", "M28.csv"]
    
    # Initialize with the first file
    print(f"Reading {files[0]}...")
    combined_df = pd.read_csv(os.path.join(input_dir, files[0]))
    
    # Merge with the remaining files
    for file in files[1:]:
        print(f"Reading {file}...")
        df = pd.read_csv(os.path.join(input_dir, file))
        
        # Merge on the Time column
        combined_df = pd.merge(combined_df, df, on="Time", how="outer")
    
    # Sort by Time to ensure chronological order
    combined_df['Time'] = pd.to_datetime(combined_df['Time'])
    combined_df = combined_df.sort_values('Time')
    
    # Save the combined data
    output_file = "HHN-HHO.csv"
    print(f"Saving combined data to {output_file}...")
    combined_df.to_csv(output_file, index=False)
    
    print(f"Successfully combined {len(files)} files into {output_file}")
    print(f"Total rows: {len(combined_df)}")
    print(f"Columns: {list(combined_df.columns)}")
    
    return combined_df

if __name__ == "__main__":
    # Run the combination
    result = combine_foa_data() 