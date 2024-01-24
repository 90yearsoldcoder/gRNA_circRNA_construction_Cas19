import pandas as pd

# Read the Excel file
excel_file = '41592_2020_1011_MOESM3_ESM.xlsx'
df = pd.read_excel(excel_file, sheet_name="b, gRNA sequences")

# Convert and save as a TSV file
tsv_file = 'reference_data.tsv'
df.to_csv(tsv_file, sep='\t', index=False)
