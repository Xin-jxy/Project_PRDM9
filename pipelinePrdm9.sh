#!/bin/bash

#1ere etape : alignements read avec 32 alleles PRDM9
#Recupere les fichiers fasta : 32 alleles avec regions flanquante et fastq : reads 

#repertoire fasta et fatsq
alleleFasta=data/raw/Sequences_alleles_flanquees.fa
read1Fatsq=$1
read2Fatsq=$2

echo "##allele align"
bash ./alignementAllele.sh $alleleFasta $read1Fatsq $read2Fatsq


#Pour passer a la deuximeme partie on doit d'abord recreer un fichier fatsq read 1 et 2 
#à partir du fichier fastq générer dans la 1er partie
fichierFasqtTrier=data/alignementAllele.fastq
fichierRead1=data/read1.fastq
fichierRead2=data/read2.fastq

echo "##split read"
python3 ./separer_fichier.py $fichierFasqtTrier $fichierRead1 $fichierRead2


#2eme partie : alignement du genome entier et les 31 alleles restant avec les reads trié. 
#Recupere les fichiers fasta : genomes 31 alleles avec regions flanquante et fastq : reads tié 
#Considère que index genome et allele déjà fait donc netransmet pas de fichier fasta, le script utilise directement l'index du fichier BOTWIE_INDEX

read1alignementGenome=data/read1.fastq
read2alignementGenome=data/read2.fastq

echo "##sort paralogue"
bash ./testALigneParalogue.sh $read1alignementGenome $read2alignementGenome


#Pour passer a la troisième partie on doit d'abord recreer un fichier fatsq read 1 et 2 
#à partir du fichier fastq générer dans la 2eme partie
fichierFasqtTrierParalogue=data/alignGenome.fastq
fichierRead1Genome=data/read1Genome.fastq
fichierRead2Genome=data/read2Genome.fastq

echo "##split read"
python3 ./separer_fichier.py $fichierFasqtTrierParalogue $fichierRead2Genome $fichierRead1Genome

#Partie 3 : genotyage 
read1Genotypage=data/read1Genome.fastq
read2Genotypage=data/read2Genome.fastq

echo "##genotypings"
python3 ./Genotyping.py $read1Genotypage $read2Genotypage $alleleFasta 