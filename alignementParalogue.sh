#!/bin/bash

#Download fastq files from 1000 Genomes
#ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/
#Take 6 genomes of individus with differents origins and coverage


##Creation of the necessary folders
cd ~/projet_PRDM9/script/data/
mkdir BOWTIE_INDEXES/
mkdir BOWTIE_INDEXES/index/


##Creation of index

bowtie2-build hg38_alleles.fa data/BOWTIE2_INDEXES/index/index

##Alignment with bowtie2

#Options 

#-k <int>:
#By default, bowtie2 searches for separate and valid alignments for each reading. When he finds a valid alignment, he continues to look for alignments that are almost as good or better. The best alignment found is indicated (randomly chosen from the best if tied). Information on the best alignments is used to estimate the quality of the mapping and to define SAM optional fields, such as AS:i and XS:i.
#When -k is specified, however, bowtie2 behaves differently. Instead, it searches for separate and valid alignments for each reading as much as possible <int>. The search ends when it is not possible to find more distinct valid alignments, or when it finds <int>, whichever comes first. All alignments found are reported in descending order by alignment score. 
#The alignment score of a two-ended alignment is equal to the sum of the alignment scores of each partner. Each reading or pair alignment reported beyond the first has the'secondary' SAM bit (which is equal to 256) enabled in its FLAGS field. For readings that have more than <int> separate and valid alignments, bowtie2 does not guarantee that the reported <int> alignments are the best possible in terms of alignment score. -k is mutually exclusive with -a.
#Note: Bowtie 2 is not designed with large values for -k in mind, and when aligning reads to long repetitive genomes large -k can be very, very slow.

#-q:
#The readings (specified with <m1>, <m2>, <m2>, <m2>, <s>) are FASTQ files. FASTQ files usually have the extension.fq or.fastq. FASTQ is the default format.

#-s:
#File to write SAM alignments to. By default, alignments are written to the'standard out' or'stdout' file (i.e. the console).

#-x <bt2-idx>
#The basic name of the index of the reference genome. The base name is the name of any of the index files up to but not including the final .1.bt2 / .rev.1.bt2 / etc. 
#bowtie2 searches for the specified index first in the current directory, then in the directory specified in the BOWTIE2_INDEXES environment variable.
#
#-1 <m1>
#List of files separated by commas containing mats 1s (the filename usually contains _1), for example -1 flyA_1.fq,flyB_1.fq. 
#The sequences specified with this option must match the file-for-file and read-for-read sequences with those specified in <m2>. 
#The readings can be a mixture of different lengths. If - is specified, bowtie2 will read the mat 1s in the'standard in' or'stdin' file.

#-2 <m2>
##Comma-separated list of files containing the mate 2s files (the filename usually contains _2), for example -2 flyA_2.fq,flyB_2.fq. 
#The sequences specified with this option must match the file-for-file and read-for-read sequences with those specified in <m1>. 
#The readings can be a mixture of different lengths. If - is specified, bowtie2 will read the mat 2s in the 'standard in' or 'stdin' file.


bowtie2 -x data/BOWTIE_INDEXES/index/index -q -k11 -1 data/raw/READ_1.fq -2 data/raw/READ_2.fq -S align.sam



##Conversion of sam file to fastq
# /!\ The reads must be sorted beforehand

samtools view align_trie.sam | awk '{OFS="\t"; print ">"$1"\n"$10}' - > align.fastq


