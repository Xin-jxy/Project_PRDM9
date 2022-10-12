#!/usr/bin/env python3
#
# coding: utf-8
#

import sys
import LibraryGenotyping as LG


if __name__ == '__main__':
    seq1 = sys.argv[1]
    dictionnaire_read1 = LG.FastX_To_Dico(seq1).run_fastx()
    seq2 = sys.argv[2]
    dictionnaire_read_pair = LG.FastX_To_Dico(seq2).run_fastx()
    seq3 = sys.argv[3]
    dictionnaire_allele = LG.FastX_To_Dico(seq3).run_fastx()
    boot = LG.Alignement_Read_Allele(dictionnaire_read1, dictionnaire_read_pair, dictionnaire_allele)
    meilleur_genotype = boot._choix_du_genotype()
    boot.ecrire_le_genotype(meilleur_genotype)