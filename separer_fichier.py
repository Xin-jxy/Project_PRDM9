#!/usr/bin/env python
#
#coding: utf-8
#
import sys

def separation(nomFichierASeparer, nomFichierRead, nomFichierPair):
    with open(nomFichierRead, "w") as fichier_read:
        with open(nomFichierPair, "w") as fichier_pair:
            with open(nomFichierASeparer, "r") as fichier_separe:
                compteur = 0
                quel_fichier = 0
                for ligne in fichier_separe:
                    if compteur % 4 == 0:
                        quel_fichier += 1
                    if quel_fichier % 2 == 0:
                        fichier_pair.write(ligne)
                    else:
                        fichier_read.write(ligne)
                    compteur+=1

if __name__=='__main__':
    nomFichierASeparer=sys.argv[1]
    nomFichierRead=sys.argv[2]
    nomFichierPair=sys.argv[3]
    separation(nomFichierASeparer,nomFichierRead,nomFichierPair)
