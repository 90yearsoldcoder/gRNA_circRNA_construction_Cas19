# Introduction
* This is a pipeline to constructing guideRNA(gRNA) for screening circRNA in CRISPR–Cas13 system
* The original paper/protocol is Li, S., Wu, H. & Chen, LL. Screening circular RNAs with functional potential using the RfxCas13d/BSJ-gRNA system. Nat Protoc 17, 2085–2107 (2022). https://doi.org/10.1038/s41596-022-00715-5

# Dependency
* bedtools
* python, python library: random, os, argparse, tqdm, pandas

# Usage
## 1.Prepare data
* circRNA coordinate and its host gene name
* Format: bed file, the first four columns are **required**
* Example bed file:

| |  |  |  | | |
|-------|-----------|-----------|--------|--------|--|
| chr10 | 103427642 | 103436193 | FBXW4  |  0     | + |
| chr10 | 103432671 | 103436193 | FBXW4  |0       |+ |
| chr10 | 105197771 | 105198565 | PDCD11 |0       |- |
| chr10 | 112723882 | 112745523 | SHOC2  |0       |- |

## 2.Run the pipeline
```
python gRNA_construct.py -r path/to/reference.fa -b path/to/circRNA.bed
```
optional parameters: (1) -f path to generated circRNA fasta file; (2) -o path to output.tsv file; (3) -d flag to delete fasta file;


# Example: use the paper data
* In the example, we will use the circRNA data in the original paper to build gRNA and then compare our gRNA with their gRNA library.
* [Original data](https://static-content.springer.com/esm/art%3A10.1038%2Fs41592-020-01011-4/MediaObjects/41592_2020_1011_MOESM3_ESM.xlsx) in the paper is already downloaded to ```example/41592_2020_1011_MOESM3_ESM.xlsx```
## 1. Step 0(optional):
* Convert the original data from xlsx to ```bed file``` and ```tsv file(for the further comparison)```
* python library **openpyxl** is **required**
```
cd example
python convert_xlsx2tsv.py
python extract_tsv2bed.py
```
* We remove the row 287 which is ```chr17_ctg5_hap1:616744-618122```, since we do not have enough information about this haplotype in reference

## 2. Step 1 run the command line:
You can check the bed file at ```example/circRNA.bed``` \
**Notice**: the first col in the ```example/circRNA.bed``` is just a number instead of chr+[number]. Because the original paper was using hg37 as reference. If you are now using any higher version(hg38+), the first col should be chr + [number], which is the same with the [Example bed file above](#1prepare-data)
```
(optional, if you do not have hg37 reference)
wget ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.primary_assembly.fa.gz
gunzip Homo_sapiens.GRCh37.dna.primary_assembly.fa.gz
```
```
python ../gRNA_construct.py -r Homo_sapiens.GRCh37.dna.primary_assembly.fa -b ./circRNA.bed
```

## 3. Step 2 compare the gRNA with paper's gRNA
