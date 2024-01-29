'''
a temp script to guess the strand info from comparison result
Since the original form did not provide strand info.
Add this to .gitignore
'''

comp_path = "./comparison_results.txt"
bed_ori_path = "./circRNA_ori.bed"
bed_path = "./circRNA.bed"

strand_info = []
with open(comp_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line_sp = line.split('\t')
        p = (line_sp[2][:-1])
        if float(p) < 100:
            strand_info.append('-')
        else:
            strand_info.append('+')

txt = ""
with open(bed_ori_path, 'r') as f:
    lines = f.readlines()
    i = -1
    for line in lines:
        i += 1
        txt += line.strip()
        txt += "\t" "0" + "\t" + strand_info[i] + "\n"

with open(bed_path, 'w') as f:
    f.write(txt)