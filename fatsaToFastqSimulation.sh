#!/bin/bash


#Script pour simuler donnée test
echo $1
#On recupère le fichier transmis en fasta 1ere argument 
fichierFasta=$1


#Par defaut les fichier fatsq seront créer dans un dossier fastq de data
fichierFastqRead1=data/raw/FASTQ/read1.fq
fichierFastqRead2=data/raw/FASTQ/read2.fq

gcc -g -O2 -Wall -o wgsim wgsim.c -lz -lm


#on appelle wgsim 
if [ $# -eq 1 ];then
    ./wgsim -1151 -2151 -d500 -r0 -e0 -N100 -R0 -X0 "a.fa" $fichierFastqRead1 $fichierFastqRead2

elif [ $# -eq 3 ];then
    ./wgsim -1151 -2151 -d500 -r0 -e0 -N100 -R0 -X0 $fichierFasta $2 $3
else
    echo 'Pas de fichier à traiter'
fi

