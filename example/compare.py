import csv

def compare(seq1, seq2):
    if len(seq1) != len(seq2):
        return 0
    else:
        length = len(seq1)
        count = 0
        for i in range(length):
            if seq1[i] == seq2[i]:
                count += 1
        return count / length

# Read the data from the first file
ref_dic = {}
with open('reference_data.tsv', 'r') as f:
    lines = f.readlines()
    for line in lines[3:]:
        line_sp = line.strip().split('\t')
        gene_name = line_sp[0] + "(" + line_sp[1] + ")"
        #print(gene_name)
        ref_dic[gene_name] = [item for item in line_sp[2:]]


gRNA_dic = {}
with open('gRNA.tsv', 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        line_sp = line.strip().split('\t')
        gene_name = "chr"+line_sp[0] + "(" + line_sp[1] + ")"
        #print(gene_name)
        gRNA_dic[gene_name] = [item for item in line_sp[2:]]


# Compare and save the results
with open('comparison_results.txt', 'w') as outfile:
    txt=""
    for key in ref_dic:
        if key in gRNA_dic:
            txt += key + "\t"
            for i in range(len(ref_dic[key])):
                p = compare(ref_dic[key][i], gRNA_dic[key][i])
                formatted_percentage = "{:.2f}%".format(p*100)  # Format the percentage
                txt += formatted_percentage + "\t"
                if p < 1:
                    print(ref_dic[key][i], gRNA_dic[key][i])
            txt += "\n"
    outfile.write(txt)