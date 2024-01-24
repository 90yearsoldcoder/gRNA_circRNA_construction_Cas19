import pandas as pd

# Load your data (change this to the correct file and sheet name)
file_path = 'reference_data.tsv'
df = pd.read_csv(file_path, sep='\t', skiprows=1)


# Extract the relevant columns
locations = df['CircRNA genomic location\n(Chr:Start-End)']
genes = df['CircRNA host gene symbol']


# Parse the genomic locations and split them into chromosome, start, and end
chr_start_end = locations.str.extract(r'(chr[0-9XY]+):(\d+)-(\d+)')
chr_start_end.columns = ['chrom', 'start', 'end']

# Remove 'chr' prefix from the chromosome column
chr_start_end['chrom'] = chr_start_end['chrom'].str.replace('chr', '')

# Combine with gene names
bed_data = pd.concat([chr_start_end, genes], axis=1)

# Save to BED file
output_file = 'circRNA.bed'
bed_data.to_csv(output_file, sep='\t', header=False, index=False)

print(f'BED file saved as {output_file}')
''''''