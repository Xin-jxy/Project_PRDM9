#!/usr/bin/env python3
#
# coding: utf-8
#

import sys

REGION_5 = """
AATTCAGATTTGCTCACACATCTTCTCTTTAACCACATTTGTGGATCTCCAGCCTGAGTG
CTCTTAATAGATCCTTTTCCCCTCTTAGGAAATCACTAAGGACAATCTCACCTAAGTCAT
CAAGAGTGTTATTTCTCAATAGAATAAAATAGCTGAAGGTCTCATGTCAGCAAAAGTGCC
CAGGGACCAGGGAGGGAGGATGTGGCAGAGGGTGATCAGGGAAGGCTTTATAGGACTTGG
AAAATACCTGCAGTGTGGGGAAAAGGTCACTGCAGTTCCATCTATGTAAGGAATGACACT
GCCCTGATGCTGGTTGAGGTTACCTAGTCTGGCAGATATGTAGAAAAGGACCAAGATGTG
GGATTTCTGGATTTTTTAAGATGTAGTGAATAAAAGTGGAATGGAAAAATGGACTGTAAA
GGTCCATCCAGCACTTGGTGGGAAAGAGCTTGCATTGTTAACATATGAAGAATGATTGTT
TCTTCATTTGATCTTCATACCTTCATATGTGGTAAGGCCTGAACAAAACATCTACCCTGA
CCAAAAACTTCCTCTTTCAGAACCAAAGCCAGAGATCCATCCATGTCCCTCATGCTGTCT
GGCCTTTTCAAGTCAGAAATTTCTCAGTCAACATGTAGAACGCAATCACTCCTCTCAGAA
CTTCCCAGGACCATCTGCAAGAAAACTCCTCCAACCAGAGAATCCCTGCCCAGGGGATCA
GAATCAGGAGCAGCAATATCCAGATCCACACAGCCGTAATGACAAAACCAAAGGTCAAGA
GATCAAAGAAAGGTCCAAACTCTTGAATAAAAGGACATGGCAGAGGGAGATTTCAAGGGC
CTTTTCTAGCCCACCCAAAGGACAAATGGGGAGCTGTAGAGTGGGAAAAAGAATAATGGA
AGAAGAGTCCAGAACAGGCCAGAAAGTGAATCCAGGGAACACAGGCAAATTATTTGTGGG
GGTAGGAATCTCAAGAATTGCAAAAGTCAAGTATGGAGAG
"""

REGION_3 = """
GATGAGTAAGTCATTAGTAATAAAACCTCATCTCAATAGCCACAAAAAGACAAATGTGGT
CACCACACACTTGCACACCCCAGCTGTGAGGTGGCTTCAGCGGAAGTCTGCTGACCCCTT
ATATTCCCCGAGAGTATAAAGAGATCGGAAATAACTGATTAAACAAATCCGCCACTTTCA
TGACTAGAGATGAGGAAGAACAAGGGATAGTTCTGTAAGTGTTCGGGGGACATCAGCATG
TGTGGTTCTTTCCCGCACTGATCCCCTCCATTTTTTGTTTGTTTTTTTGCCTCCTGTTCT
AATAAATTTTGTCTCCATACAAATCTGAACCCCAAGTGTGTACCTCATTCTTCCCTTATC
ACTGAAGGCAAGAAGAGTCCAGAAGGGCCACAGAGAACTCATGTGTTCAGCTCAAGACTC
CACAGGAATTCAACCCCCAGAAAGACATAAACTTGGAGTCCGTCTGGTTTAATTATTGGA
GAATCGATTCCCAAGTCCAGGAAGAGAAATGTAAGATTCTAGAAAGTCGCAGCAGGAAAG
GGAGTTCCCTGGTCTCCTGGGAAGTGTGGCTTCTTCTCCTAATGGACACCTCTCCTCTGC
TGCCATACTCTCCCTTGGCTCCCCAGTCTCCTCTCCTGATCTCCTCCAATCTCTGTAGCC
CAAGATGTGAAAGCCAGACAAGAACACGCGTGTGTGTATATATGTGTTCGGGTGTGGGGG
TATGTGCCCTCCGTGTAGGTAACTGTGTGAGTGTGGGGGGTTTCAAGGGTGTGTTAGGAA
CAACGCTCAAAATCCTAAGGAAACTGAACACTCGAACGAAGGATTCTTAGCAAAGCAATT
TTACTTCTGTGCAGAGGGGTGCCTCCTTGGCCGGTCGCCATGAGAGCACACCTGAACAAA
GAGGCAGGAGAGCCTTTATTCCTGACACAAGTCCTGCCCCTGTACCTTTTTCCACTGGCT
GGGGTCGGGTCGTACAATCTAAACTAATCCCAGTTGGCTA
"""


class Fasta:
    """
    Lecture de fichiers au format FASTA

    Exemple d'utilisation:
       f = Fasta("fichier.fasta")
       for k,v in iteritems(f.sequences):
           print("{}: {}".format(k, v))
    """

    def __init__(self, fichier):
        nom = ""
        self._dicosequences = {}

        with open(fichier, 'r') as f:
            index = f.readline()
            index = index.strip()
            while index != "":

                if index[0] == '>':
                    nom = index[1:].strip()
                    self._dicosequences[nom] = ""
                else:
                    self._dicosequences[nom] += index.strip()
                index = f.readline()



    def _get_sequences(self):
        return self._dicosequences
    sequences = property(fget=_get_sequences, doc="Dictionnaire de séquences")

class Ajout_Region_Flanquantes:
    def __init__(self, dictionnaire_alleles):
        self.dictionnaire_des_alleles = dictionnaire_alleles

    def ajout_des_region(self):
        region5 = REGION_5.replace('\n', "")
        region3 = REGION_3.replace('\n', "")
        for allele in self.dictionnaire_des_alleles:
            self.dictionnaire_des_alleles[allele] = region5 + self.dictionnaire_des_alleles[allele] + region3

    def ecrire_fichier_avec_region(self):
        self.ajout_des_region()
        with open("Sequences_alleles_flanquees.fa", 'w') as fichier:
            for allele in self.dictionnaire_des_alleles:
                fichier.write("\n > {} \n".format(allele))
                index = 1
                for cara in self.dictionnaire_des_alleles[allele]:
                    if (index % 70) == 0:
                        fichier.write("{}\n".format(cara))
                    else:
                        fichier.write(cara)
                    index += 1



if __name__ == '__main__':
    seq1 = sys.argv[1]
    run = Fasta(seq1)
    dico_allele = run._dicosequences
    boot_class = Ajout_Region_Flanquantes(dico_allele)
    ecrire = boot_class.ecrire_fichier_avec_region()

