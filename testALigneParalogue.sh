#!/bin/bash


##Creation of the necessary folders

#cd ~/projet_PRDM9/script/data/
#mkdir -m BOWTIE2_INDEXES/

fichierRead1=$1
fichierRead2=$2

echo "$1"
echo "$2"


##Creation of index

#bowtie2-build data/raw/hg38_alleles.fa data/BOWTIE2_INDEXES/index_genom

#alignement
echo "##Alignement genome"
bowtie2 -x data/BOWTIE2_INDEX/index_genome/index -q -k10 -1 $fichierRead1 -2 $fichierRead2 -S data/align.sam

echo "##separation paralogue"
python3 ./Separation_Paralogue.py data/align.sam

echo "##Fichier fatsq"
samtools view data/alignNoParalogue.sam | awk {'OFS="\t"; print "@"$1"\n"$10"\n+\n"$11}' - > data/alignGenome.fastq
