import random
import os
import argparse
import re
from tqdm import tqdm

# Generate a random RNA sequence of Length l
def generate_random_sequence(l: int):
    sequence = ""
    for i in range(l):
        sequence += random.choice("ACGT")
    return sequence

# Generate scrambled sequence
def generate_scrambled_sequence(sequence, length):
    if len(sequence) < length:
        raise ValueError("Length of sequence is less than the length of scrambled sequence")
    scrambled_sequence = generate_random_sequence(length//2)
    scrambled_sequence += sequence[0:(length-length//2)]
    return scrambled_sequence

'''
Generate a gRNA according to a given RNA sequence
Input: RNA sequence, Length of left arm, Length of right arm
'''
def generate_gRNA(sequence, left_arm, right_arm):
    if len(sequence) < left_arm + right_arm:
        raise ValueError("Length of sequence is less than the sum of left and right arms")
    # Generate sequence for the left arm
    left_arm_sequence = sequence[-left_arm:]
    # Generate sequence for the right arm
    right_arm_sequence = sequence[:right_arm]
    # Generate sequence for the gRNA
    gRNA_sequence = left_arm_sequence + right_arm_sequence
    return gRNA_sequence

# Generate a list of gRNAs according to a given RNA sequence
# Input: RNA sequence
# return: list of gRNAs: [scrambled sequence, 15+15nt, 10nt + 20nt, 20nt + 10nt, 14nt + 14nt, 13nt + 13nt]
def generate_gRNA_list(sequence):
    gRNA_list = []
    # Generate scrambled sequence
    gRNA_list.append(generate_scrambled_sequence(sequence, 30))
    # Generate 15+15nt
    gRNA_list.append(generate_gRNA(sequence, 15, 15))
    # Generate 10+20nt
    gRNA_list.append(generate_gRNA(sequence, 10, 20))
    # Generate 20+10nt
    gRNA_list.append(generate_gRNA(sequence, 20, 10))
    # Generate 14+14nt
    gRNA_list.append(generate_gRNA(sequence, 14, 14))
    # Generate 13+13nt
    gRNA_list.append(generate_gRNA(sequence, 13, 13))
    return gRNA_list

def reverse_bed_file(bed_path, reversed_bed):
    with open(bed_path, "r") as f, open(reversed_bed, "w") as out:
        for line in f:
            parts = line.strip().split()
            if len(parts) > 5:
                # Assuming strand info is in the 6th column
                strand = parts[5]
                if strand == "+":
                    parts[5] = "-"
                elif strand == "-":
                    parts[5] = "+"
            out.write("\t".join(parts) + "\n")


# Using bedtools getfasta to generate fasta file for gRNA
# Input: path to bed file, path to fasta file, path to output file
# help info: bedtools getfasta -fi reference.fa  -bed test.bed -fo circRNAs.fa -s -split
def generate_fasta_file(bed_path, fasta_path, fasta_file_path):
    print("Get RNA sequence(fasta) from bed file: ", end=" ")
    os.system("bedtools getfasta -fi " + fasta_path + " -bed " + bed_path + " -fo " + fasta_file_path + " -s -split")
    print("Done")


# read in fasta file and bed file to generate gRNA, and save to output file
# Input: path to fasta file, path to bed file, path to output file
# output file format: col1: chr:st-ed, col2: gRNA_list[0], col3: gRNA_list[1], col4: gRNA_list[2], col5: gRNA_list[3], col6: gRNA_list[4], col7: gRNA_list[5]
def generate_gRNA_file(fasta_file_path, bed_path, output_file_path):
    # read in fasta file
    fasta_file = open(fasta_file_path, "r")
    fasta_lines = fasta_file.readlines()
    fasta_file.close()
    # read in bed file
    bed_file = open(bed_path, "r")
    bed_lines = bed_file.readlines()
    bed_file.close()
    # generate gRNA list
    RNA_gRNA_dic = {}
    for i in tqdm(range(len(fasta_lines)), desc="Processing fasta file"):
        if fasta_lines[i].startswith(">"):
            continue
        bed_info = bed_lines[i//2].strip().split("\t")
        gene_info = bed_info[0] + ":" + bed_info[1] + "-" + bed_info[2] + "(" + bed_info[3] + ")"
        RNA_gRNA_dic[gene_info] = generate_gRNA_list(fasta_lines[i].strip())
    # write to output file
    output_file = open(output_file_path, "w")
    output_file.write("gene_location\tgene\tPaired_control\tgRNA_15+15nt\tgRNA_10+20nt\tgRNA_20+10nt\tgRNA_14+14nt\tgRNA_13+13nt\n")
    for key in RNA_gRNA_dic:
        # Regular expression to find text within brackets
        match = re.search(r'\((.*?)\)', key)
        # Extract and print the gene name if a match is found
        if match:
            gene_name = match.group(1)
            #print("Gene name:", gene_name)
        else:
            print("No gene name found in the " + key)
            continue
        output_file.write(key.split("(")[0] + "\t" + gene_name + "\t" + RNA_gRNA_dic[key][0] + "\t" + RNA_gRNA_dic[key][1] + "\t" + RNA_gRNA_dic[key][2] + "\t" + RNA_gRNA_dic[key][3] + "\t" + RNA_gRNA_dic[key][4] + "\t" + RNA_gRNA_dic[key][5] + "\n")
    
    output_file.close()


# parse parameters
parser = argparse.ArgumentParser(description="Generate gRNA for circRNA")
parser.add_argument("-r", "--reference", help="Path to reference fasta file", required=True)
parser.add_argument("-b", "--bed", help="Path to circRNA bed file", required=True)
# parse output fast file, default: circRNA.fa
parser.add_argument("-f", "--fasta", help="Path to output fasta file", required=False, default="circRNA.fa")
# parse output file, default: gRNA.tsv
parser.add_argument("-o", "--output", help="Path to output file", required=False, default="gRNA.tsv")
# remove fasta file after generating gRNA
parser.add_argument("-d", "--delete", help="Delete fasta file after generating gRNA", required=False, default=False)
args = parser.parse_args()

# Treverse strand info in bed file. Since the gRNA is reversed RNA. file: "reversed.bed"
reverse_bed_file(args.bed, "reversed.bed")
# generate fasta file
generate_fasta_file("reversed.bed", args.reference, args.fasta)
# generate gRNA file
generate_gRNA_file(args.fasta, args.bed, args.output)
if args.delete:
    os.system("rm " + args.fasta)
