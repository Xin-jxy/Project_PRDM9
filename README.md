##Project of identification of genotype of gene PRDM9 in divers human population  

In this project, we provide a process which could find new zinc finger of gene PRDM9 in another human population except European, Indian and west-African. The accomplished  of project is based on knowledge of sequences of 32 alleles identified by other scientists in this three populations. The sequence of human sequence is free to download at [1000 genomes project](https://www.internationalgenome.org/).

In this manual, you will receive informations about :

```
1. Steps concerned for the identification of PRDM9 
in different population.

2. The indication of genotype searching

3. Indication of utilisation of pipline

4. informations about bioinformatic tools and sequence format.

5. Imperfection and notice of project
```

**Notice**: all script are writed based on system Linux and for Python3, it won't work with system Windows, and some errors have been detcted with system macOS in the process of genotype searching as well. 

You may click [here](https://www.python.org/downloads/ ) to download Python3. 


****


###<u>How to identify PRDM9 in divers population</u>

* _**Align 32 alleles identified to reads of whole genome sequence desired**_

For start, the obtained of 32 alleles can map to reads of whole genome sequence that we choose randomly other than population of European, Indian and west-African at 1000 genomes project (*hereinafter called sequence desired*), this step allows the identification of gene PRDM9 and its sequences paralogical in sequence desired. We apply the mode alignment local, the requirement of alignment exact is the raison why we use alignment local instead of alignment global, and the consideration of our work efficiency, the paired-end of reads will be applied in this experience. We use Bowtie2 as tool to align read. After that, we use samtools for the output file of Bowtie2 to transfer his format SAM to FASTQ. 


* _**Identifcation of PRDM9 sequence at sequence desired without paralogy**_

We combine at first the sequence of reference genome [GRCh38](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/) with other 31 alleles but allele B in a same file, beacause of the contain of allele B in GRCh38. And then, we align this new file to sequence desired with Bowtie2. This step allows us to recognize the part of sequence paralogical possible(PRDM7 for instance) in sequence desired and then delete it, so that we could raise rate alignment for identification of new zinc finger of gene PRDM9 in sequence desired. 

* _**Align PRDM9 sequence to reads of sequence desired**_

We've obtained a PRDM9 sequence without paralogy from last step, therefore we can campare each 32 alleles to reads of sequence desired for obtaining the genotype corresponded and its scores, so we have to do 31*32/2=512 comparaison within both the sequence of homozygote and heterozygote. We choose the genotype with best score after the comparaison. With thoses genotypes, we could finally find new zinc finger in this population chosen, and in this systeme, we could discover perhaps new characters and differences entre-population based on analysation of gene sequence.

###<u> How to find the genotype ? </u>

This part of content is a part of a important process which the goal is to find the genotype in PRDM9 of a person and potentially to find alleles by discovering new zinc finger. The script concern are: Genotyping.py, LibraryGenotyping.py and LibraryGenotyping_Config.py with python3.

* _**Genotyping.py**_

This script servs to run all functions and modules of LibraryGenotyping.

it takes in input 3 arguments :
- a file of reads supposed from PRDM9 in fasta or fastq format
- a file of reads which are the pairs from the first file , also in fasta or fastq 
- a file containing all alleles of references of PRDM9 in fasta or fastq  

and write in the terminal a list of the 10 best genotypes founds and their score  

example:
```
./Genotyping.py read1.fq read2.fq alleles.fa

meilleurs score possible : 604

(' a', ' a', 604)
(' a', ' d', 604)
(' a', ' L3', 604)
(' a', ' L5', 604)
(' a', ' L8', 604)
(' a', ' L9', 604)
```

* _**LibraryGenotyping.py**_

This is a script containing all the functions and class for genotyping.

#####FastX-to-Dico

It's an object which role is to turn a fasta or fastq file into a dictionary.

#####Calcule_Score

This class serves to find the best scores by aligning the sequence of a read on the sequence of an allele

#####Alignement-Read-Allele

The role of this class is to find the genotype of a person from his reads  by calculating the score of alignment of each 
allele.

* _**LibraryGenotyping-Config.py**_

It is a script for the user to change variables without having to enter the script itself.

DISTANCE_ACCEPTEE : distance between the pair of read tolerated   
SCORE_SEUIL_READ : minimal score for the read to be added to be considered as accepted
SCORE_SEUIL_PAIR_DE_READ : minimal score for the pair to be added to the allele
SEUIL_MISMATCH_TOLERE : number of mismatch accepted for an alignment  
COMBIEN_PRINT : number of genotype to be printed between the best ones   

* by default: 

(for reads which length is 150)  
DISTANCE_ACCEPTEE : 100 - 500  
SCORE_SEUIL_READ : 120  
SEUIL_MISMATCH_TOLERE : 260  
SEUIL_MISMATCH_TOLERE : 3  
COMBIEN_PRINT : 20
****
###<u>Indication of pipeline</u>

####Indication of pipeline

Notice: All commands apply in the file floder "script"

**_The command line global of pipeline:_**

	sh pipelinePrdm9.sh <name_file_of_read1_allele> <name_file_of_read2_allele> 
****

####content of pipeline

1. * _Align 32 alleles identified to reads of whole genome sequence desired_

**alignementAllele.sh** is a script that we write for aligning 32 alleles identified to sequence desired. In this script, it contains utilization of alignment tool Bowtie2**[1]** and the format transformation tool samtools **[2]**, which helps us tansfer the file with format SAM to FASTQ for application of next step. **separer_fichier.py** is a script which we use to separate 2 reads after the apllication of Bowtie2. 


_The command line for align：_

	sh alignementAllele.sh <name_of_sequence_alleles_flanc> <name_file_of_read1_allele> <name_file_of_read2_allele> 

In this command, we fix the file >>Sequences_alleles_flanquees.fa in file floder "raw" which in file folder "data". After the application of this command, Bowtie2 reunite 2 reads in 1 file >>alignementAllele.fastq, which is stocked in "data".

_The command line for separate read1 and read2_

	python3 ./separer_fichier.py <name_file_of_align_allele_after_bowtie2> <new_file_read1> <new_file_read2>
	
After this command, it creates 2 new files of read1 and read2, which we apply in next step. Those 2 new files should be stocked in file floder "data".
	

2. * _Identifcation of PRDM9 sequence at sequence desired without paralogy_

**testALigneParalogue.sh** is a script which allows us to select only the sequence of read of gene PRDM9, without sequences paralogical. 

_The command line for the sort of reads with part paralogy_

	sh ./testALigneParalogue.sh <new_file_read1> <new_file_read2>

We use thoses 2 reads obtained from last step, and then after this command, it generates a new file >>alignGenome.fastq , stocked in "data".

_The command line for the sort of reads withut part paralogy：_

	python3 ./separer_fichier.py <name_of_file_fastq_without_paralogy> <name_of_file_read1> <name_of_file_read2>
	

3. * _Align PRDM9 sequence to reads of sequence desired_

**LibraryGenotyping_config.py** is a script that we determine the standard of selection of good genotype corresponded. **LibraryGenotyping.py** uses for accomplishing the selection of genotype and find new zinc finger. **Genotyping.py** is a pipeline for this process.

_The command line for score of genotype：_

	python Genotyping.py <name_of_file_read1> <name_of_file_read2> <name_of_sequence_alleles_flanc>
	
Therefore we obtain result of genotype in file floder "result" to analysis.

****
###<u>informations of tool and format</u>

####Bioinformatic tools
####[1] Bowtie2

1. <u>Introduction</u>


Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s of characters to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index (based on the Burrows-Wheeler Transform or BWT) to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 gigabytes of RAM. Bowtie 2 supports gapped, local, and paired-end alignment modes. Multiple processors can be used simultaneously to achieve greater alignment speed.

Bowtie 2 outputs alignments in SAM format, enabling interoperation with a large number of other tools (e.g. SAMtools, GATK) that use SAM. Bowtie 2 is distributed under the GPLv3 license, and it runs on the command line under Windows, Mac OS X and Linux.

2. <u>Option applied in our project</u>

*Alignment options*

**--local**:

In this mode, Bowtie 2 does not require that the entire read align from one end to the other. Rather, some characters may be omitted (“soft clipped”) from the ends in order to achieve the greatest possible alignment score. The match bonus --ma is used in this mode, and the best possible alignment score is equal to the match bonus (--ma) times the length of the read. Specifying --local and one of the presets (e.g. --local --very-fast) is equivalent to specifying the local version of the preset (--very-fast-local). This is mutually exclusive with --end-to-end. --end-to-end is the default mode.

*Main arguments*

**-x (bt2-idx)**:

The basename of the index for the reference genome. The basename is the name of any of the index files up to but not including the final .1.bt2 / .rev.1.bt2 / etc. bowtie2 looks for the specified index first in the current directory, then in the directory specified in the BOWTIE2_INDEXES environment variable.

**-1 (m1)**:

Comma-separated list of files containing mate 1s (filename usually includes _1), e.g. -1 flyA_1.fq,flyB_1.fq. Sequences specified with this option must correspond file-for-file and read-for-read with those specified in <m2>. Reads may be a mix of different lengths. If - is specified, bowtie2 will read the mate 1s from the “standard in” or “stdin” filehandle.

**-2 (m2)**:

Comma-separated list of files containing mate 2s (filename usually includes _2), e.g. -2 flyA_2.fq,flyB_2.fq. Sequences specified with this option must correspond file-for-file and read-for-read with those specified in <m1>. Reads may be a mix of different lengths. If - is specified, bowtie2 will read the mate 2s from the “standard in” or “stdin” filehandle.

**-S (sam)**:

File to write SAM alignments to. By default, alignments are written to the “standard out” or “stdout” filehandle (i.e. the console).

*Reporting options*

**-k** :

By default, bowtie2 searches for distinct, valid alignments for each read. When it finds a valid alignment, it continues looking for alignments that are nearly as good or better. The best alignment found is reported (randomly selected from among best if tied). Information about the best alignments is used to estimate mapping quality and to set SAM optional fields, such as AS:i and XS:i.

When -k is specified, however, bowtie2 behaves differently. Instead, it searches for at most <int> distinct, valid alignments for each read. The search terminates when it can’t find more distinct valid alignments, or when it finds <int>, whichever happens first. All alignments found are reported in descending order by alignment score. The alignment score for a paired-end alignment equals the sum of the alignment scores of the individual mates. Each reported read or pair alignment beyond the first has the SAM ‘secondary’ bit (which equals 256) set in its FLAGS field. For reads that have more than <int> distinct, valid alignments, bowtie2 does not guarantee that the <int> alignments reported are the best possible in terms of alignment score. -k is mutually exclusive with -a.

Note: Bowtie 2 is not designed with large values for -k in mind, and when aligning reads to long, repetitive genomes large -k can be very, very slow.

*Input options*

**-q**:

Reads (specified with (m1), (m2), (s)) are FASTQ files. FASTQ files usually have extension .fq or .fastq. FASTQ is the default format. See also: --solexa-quals and --int-quals.

3. The command line for index and alignment


			* constrction of index for alignment
		bowtie2-build $fichierFasta data/BOWTIE2_INDEX/index
		
			* alignment
		bowtie2 --local -x data/BOWTIE2_INDEX/index -1 $fichierRead1 -2 $fichierRead2 -S $fichierSam


You can get more informations about Bowtie2 [here](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml). 


####[2] Samtools

1. Introduction

SAM Tools provide various utilities for manipulating alignments in the SAM format, including sorting, merging, indexing and generating alignments in a per-position format.

2. The command line for transformation of format SAM

		samtools view $fichierSam | awk '{OFS="\t"; print ">"$1"\n"$10}' - > $fichierFastq

You can get more informations about samtools [here](http://samtools.sourceforge.net/).
****

####Sequence format 

* **FASTA** 

The format of file that we download our genome sequence data from 1000 genome is FASTA. 

FASTA format is a text-based format for representing either nucleotide sequences or amino acid (protein) sequences, in which nucleotides or amino acids are represented using single-letter codes. The format also allows for sequence names and comments to precede the sequences. The format originates from the FASTA software package, but has now become a near universal standard in the field of bioinformatics.

The description line (defline) or header/identifier line, which begins with '>', gives a name and/or a unique identifier for the sequence, and may also contain additional information. In a deprecated practice, the header line sometimes contained more than one header, separated by a ^A (Control-A) character. In the original Pearson FASTA format, one or more comments, distinguished by a semi-colon at the beginning of the line, may occur after the header.

You can get more informations [here](https://en.wikipedia.org/wiki/FASTA_format-)

* **SAM**

We obtain format SAM after the application of Bowtie2 tool in our project.

Sequence Alignment Map (SAM) is a text-based format originally for storing biological sequences aligned to a reference sequence developed by Heng Li and Bob Handsaker et al. It is widely used for storing data, such as nucleotide sequences, generated by next generation sequencing technologies, and the standard has been broadened to include unmapped sequences.

Clo  | Field | Type | Brief description
---- | ----- | ---- | -------------------
 1   |	QNAME | String| Query template NAME
 2	  | FLAG | Int	| bitwise FLAG
 3	  |RNAME|String|	References sequence NAME
 4|POS	   |Int	 |1- based leftmost mapping POSition
 5	  |MAPQ|	Int	 |MAPping Quality
 6	|CIGAR|	String|	CIGAR String
 7	|RNEXT	|String|	Ref. name of the mate/next read
8	|PNEXT	|Int	|Position of the mate/next read
9	|TLEN	|Int	|observed Template LENgth
10	|SEQ	|String|	segment SEQuence
11	|QUAL	|String|	ASCII of Phred-scaled base QUALity+33

You can get more informations from [here](https://en.wikipedia.org/wiki/SAM_(file_format))

* **FASTQ**

After the transformation of tool SamTools, we use format FASTQ for the need of sequence analysis.

FASTQ format is a text-based format for storing both a biological sequence (usually nucleotide sequence) and its corresponding quality scores. Both the sequence letter and quality score are each encoded with a single ASCII character for brevity.

A FASTQ file normally uses four lines per sequence.

Line 1 begins with a '@' character and is followed by a sequence identifier and an optional description (like a FASTA title line).

Line 2 is the raw sequence letters.

Line 3 begins with a '+' character and is optionally followed by the same sequence identifier (and any description) again.

Line 4 encodes the quality values for the sequence in Line 2, and must contain the same number of symbols as letters in the sequence.


****
###Imperfction and notice of project

* Due to limited time and level, we did not accomplish the step of k-mer, because the process of calcul and algorithm is more complexe, and allows get more specific and better result.  

* We aren't able to find sequence of zinc finger with results imcompelet and some difficults with analysis of heterozygote, which prevente us from figuring out the zone of zinc finger. 
