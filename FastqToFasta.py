#python3
#
#coding: utf-8
#

import sys

def FastqToFasta(fichier_fastq, fichier_fasta):
    with open(fichier_fasta, "w") as fichier_sorti:
        with open(fichier_fastq, "r") as fichier_entree:
            ligne = fichier_entree.readline()
            while ligne != "":
                ligne = ligne.strip()
                if ligne[0] == "@":
                    fichier_sorti.write(">{} \n".format(ligne[1:]))
                    ligne = fichier_entree.readline()
                    index = 1
                    ligne = ligne.strip()
                    for lettre in ligne:
                        fichier_sorti.write("{}".format(lettre))
                        if (index % 70) == 0:
                            fichier_sorti.write("\n")
                        index += 1
                    ligne = fichier_entree.readline()
                    ligne = fichier_entree.readline()
                else:
                    ligne = fichier_entree.readline()
                    ligne = ligne.strip()


if __name__ == '__main__':
    fichier_fastq = sys.argv[1]
    fichier_fasta = sys.argv[2]
    FastqToFasta(fichier_fastq,fichier_fasta)