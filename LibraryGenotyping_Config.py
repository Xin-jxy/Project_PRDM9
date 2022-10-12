#!/usr/bin/env python3
#
# coding: utf-8
#


DISTANCE_ACCEPTEE = list(range(100, 500)) #Distance acceptable entre les positions de début du read et de son read pair
SCORE_SEUIL_READ = 120 #seuil de score considéré comme acceptable pour l'alignement d'un read
SCORE_SEUIL_PAIR_DE_READ = 260 #seuil de score considéré comme acceptable pour l'alignement de la pair de read
SEUIL_MISMATCH_TOLERE = 3 #nombre de mismatch acceptés dans l'alignement
COMBIEN_PRINT = 10 #nombre de genotypes à écrire dans le terminal
