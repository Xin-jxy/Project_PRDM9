#!/bin/bash

"""
Script permettant de faire l'alignement des read du sequencage d'un genome avec les 32 allèles de PRDM9

Trois paramètres doivent être passé 
1.Le fichier fasta = sequence(s) que l'on veut comparer au reads
2.Le fichier de read1 fastq
3.Le fichier de read2 fastq

Dans ce script il y à la création d'un index à partie du fichier fasta
Index est placer dans le dossier BOWTIE2_INDEX qui se trouve dans ce chemin /script/data/BOWTIE2_INDEX.
Le dossier BOWTIE2_INDEX doit exister au préalable

un fichier .sam est creer et placer dans le dossier data du dossier script (alignementAllele.sam).

Le fichier .sam est trié, si une ligne de read à un alignement (match de nucléotides) < 100 il n'est pas gardé.

Par la suite un fichier fastq (alignementAllele.fq) est créer à partir du fichier.sam, celui-ci est aussi
dans le répertoir data.

Après cette alignement il devrait rester les read qui ont pu s'aligner au différent alleles. 
On grade tout ceux qui ont au moins un match pour ne pas perdre de postentiel nouveaux alleles.
Portentiellement des alleles ou paralogues. 

Par la suite un fichier fastq (alignementAllele.fq) est créer à partir du fichier.sam, celui-ci est aussi
dans le répertoir data
"""

#Recupère paramètre 
fichierFasta=$1
fichierRead1=$2
fichierRead2=$3

fichierSam="data/alignementAllele.sam"
fichierFastq="data/alignementAllele.fastq"

#etape d'indexation / pas compris pourquoi doit le faire 
bowtie2-build $fichierFasta data/BOWTIE2_INDEX/index_allele

#etape d'aligenement
bowtie2 --local --no-mixed -x data/BOWTIE2_INDEX/index_allele -1 $fichierRead1 -2 $fichierRead2 -S $fichierSam

#Boucles sur le fichier .sam pour garder seulement la ligne qui a un M > 100
cat $fichierSam | while  read ligne ; do 
i=$(($i+1))
    #Commence seulement après entete
    premierCaractere=$(echo $ligne | cut -c1)
    if [ $premierCaractere != "@" ] ; then 
        #recupère le code cigare sur la ligne 
        codeCigar=$( echo $ligne | awk '{ print $6 }')
        match=0
        #Décompose le code cigare : 10M2I3M ==> 10M 2I 3M
        out=($(grep -Eo '[0-9]+[IMD]+'  <<< $codeCigar ))
        if [ 0 -eq $? ] ; then
        #Veut connaitre le nombre des composant du code cigare
        taille=$(echo ${#out[@]})
            #boucle sur chaqu'un des composant
            for (( var=0; var<$taille; var++ )) ; do
                #si le composant est un match 'M' le recupère
                out2=($(echo "${out[var]}" | grep -q "M" ))
                #si on est bien sur un match récupère son nombre
                if [ 0 -eq $? ] ; then 
                    nombreMatch=$(grep -Eo '[0-9]+' <<< ${out[var]})
                    let "match=$match+$nombreMatch"
                fi
            done
        fi
        #si aucun match vu match == 0 on suprime la sequence
        if [ $match == 0 ];then 
            #Supression de la ligne
            sed -i "${i}d" $fichierSam
            #Comme surpime la ligne met a jour index des ligne aussi
            i=$(($i-1))
        fi
    fi
done

#etape pour convertir de sam à fastq
samtools view $fichierSam | awk '{OFS="\t"; print "@"$1"\n"$10"\n+\n"$11}' - > $fichierFastq

