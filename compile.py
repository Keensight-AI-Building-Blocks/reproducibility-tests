import os
import csv
import yaml

# Directory containing the metadata files
metadata_dir = '/home/ameen/work/internship/reproducibility-tests/output'

# Output CSV file
output_csv = '/home/ameen/work/internship/reproducibility-tests/metadata.csv'

# Collect all metadata files
metadata_files = []
for root, dirs, files in os.walk(metadata_dir):
    for file in files:
        if file.endswith('.yaml'):
            metadata_files.append(os.path.join(root, file))

# Open the CSV file for writing
with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header
    header_written = False
    
    for metadata_file in metadata_files:
        with open(metadata_file, 'r') as f:
            metadata = yaml.safe_load(f)
            
            if not header_written:
                # Write the header row
                writer.writerow(metadata.keys())
                header_written = True
            
            # Write the metadata values
            writer.writerow(metadata.values())
