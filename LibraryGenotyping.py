#!/usr/bin/env python3
#
# coding: utf-8
#

import copy
import LibraryGenotyping_Config as conf






class FastX_To_Dico:
    """
    Est une classe permettant la conversion de fichier au format fasta ou fastq en dictionnaire
    entré:
         fichier(chr) = nom du fichier
    """

    def __init__(self, fichier):
        self.fichier = fichier
        self._dicosequences = {}

    def fasta(self):
        """
        converti un fichier au format Fasta en un dictionnaire où le nom des séquences sont les clés
        """
        nom = ""
        with open(self.fichier, 'r') as f:
            for index in f:
                index = index.strip()
                if index != "":
                    if index[0] == '>':
                        nom = index[1:]
                        self._dicosequences[nom] = ""
                    else:
                        self._dicosequences[nom] += index

    def fastq(self):
        """
        converti un fichier au format Fasta en un dictionnaire où le nom des séquences sont les clés
        """
        index = 0
        with open(self.fichier, 'r') as f:
            for line in f:
                line = line.strip()
                if index % 4 == 0:
                    nom = line[1: -2]
                    self._dicosequences[nom] = ""
                elif index % 4 == 1:
                    self._dicosequences[nom] = line
                index += 1

    def run_fastx(self):
        """
        permet de lancer les fonction de la classe suivant le suffixe du fichier d'entré
        retour:
              self._dicoseqence(dic) = un dictionnaire rempli où la clé est le nom de la séquence et la valeur la séquence
        """
        if self.fichier[-2:] == "fa":
            self.fasta()
        else:
            self.fastq()
        return self._dicosequences

#    def _get_sequences(self):
#       return self._dicosequences
#    sequences = property(fget=_get_sequences, doc="Dictionnaire de séquences")



class Calcule_Score:
    """
    Est une classe permetant le calcule des scores d'alignement entre un read et un allèle suivant leur position
    entrés:
          sequence_read(chr) = séquence du read à aligner
          sequence_allele(chr) = séquence du allèle à aligner
    """
    def __init__(self, sequence_read, sequence_allele):
        self.read = sequence_read
        self.allele = sequence_allele
        self.taille_read = len(sequence_read)
        self.taille_allele = len(sequence_allele)

    def score_alignement(self, base_read, base_allele):
        """
        Permet d'aligner 2 bases entre elles et de ressortir un tuple du score associé à cet alignement et s'il y a mismatch ou non
        entrés:
              base_read(chr) = base du read à comparer
              base_allele(chr) = base de l'allèle à comparer
        retour:
              (tuple) :
                   tuple[0](int) = s'il y a mismatch ou pas
                   tuple[1](int) = score de l'alignement entre les deux bases
        """
        if base_read == base_allele:
            return (0,1)
        else:
            return (1,- 10)

    def _alignement_sequence(self):
        """
        aligne un read contre l'allèle à toutes les positions possibles et ressort une liste de tuple des positions et scores
        plausibles pour l'alignement du read.
        retour:
              liste_tuple(list) = liste de tuples des alignements dis acceptables contenant le score de l'alignement(int) et sa
              position de départ(int)
        """
        liste_tuple = []
        for depart_lecture_allele in range(0, self.taille_allele - self.taille_read + 1):
            position_base = 0
            nombre_de_mismatch = 0
            score_total = 0
            while position_base < self.taille_read and nombre_de_mismatch < conf.SEUIL_MISMATCH_TOLERE:
                mismatch, score = self.score_alignement(self.read[position_base], self.allele[position_base + depart_lecture_allele])
                nombre_de_mismatch += mismatch
                score_total += score
                position_base += 1
            if score_total > conf.SCORE_SEUIL_READ:
                liste_tuple.append((score_total, depart_lecture_allele))
        return liste_tuple


class Alignement_Read_Allele:
    """
    Classe ayant pour but d'aligner l'ensemble des reads gardés précedemment contre les allèles de PRDM9 et écrire les 10
    génotypes avec le meilleurs score dans le terminal.
    entrés:
        dictionnaire_reads(dic) = dictionnaire où les clés sont les noms des reads et les valeurs leurs séquences
        dictionnaire_reads_paire(dic) = dictionnaire des reads pairés au précédent.
        dictionnaire_alleles(dic) = dictionnaire où les clés sont les noms des allèles et les valeurs leurs séquences
    """
    def __init__(self, dictionnaire_reads, dictionnaire_reads_paires, dictionnaire_alleles):
        self.alleles = dictionnaire_alleles
        self.reads = dictionnaire_reads
        self.reads_pairs = dictionnaire_reads_paires
        self.nombre_read = len(dictionnaire_reads)*2

    def _aligner(self):
        """
        Aligne la pair de read contre les différents allèles de PRDM9 pour donner un score d'alignement à un allèle
        sorti:
            score_des_alleles(dic) = a comme clé un allèle et en valeur son score d'alignement contre tous les reads
        """
        score_des_alleles = {}
        reads_non_aligne = list(self.reads.keys())
        reads_non_aligne_pair = list(self.reads_pairs.keys())
        for allele in self.alleles:
            score_des_alleles[allele] = 0
            for read in self.reads:
                calcule = Calcule_Score(self.reads[read], self.alleles[allele])
                calcule_pair = Calcule_Score(self.reads_pairs[read], self.alleles[allele])
                liste_de_score = calcule._alignement_sequence()
                liste_de_score_pair = calcule_pair._alignement_sequence()
                if liste_de_score != []:
                    if read in reads_non_aligne:
                        reads_non_aligne.remove(read)
                if liste_de_score_pair != []:
                    if read in reads_non_aligne_pair:
                        reads_non_aligne_pair.remove(read)
                if liste_de_score != [] and liste_de_score_pair != []:
                    selection = Selecion_Read_Pair(liste_de_score, liste_de_score_pair)
                    best_score = selection.run_selection()
                    score_des_alleles[allele] += best_score
        return score_des_alleles



    def _choix_du_genotype(self):
        """
        Donne le score de chaque diploïdes et les classe de manière décroissante
        retour:
              liste_meilleur_genotype(list) = la liste de tous les génotypes avec en tuple les deux allèles(chr) et le
              score(int)
        """
        score_des_alleles = self._aligner()
        liste_meilleur_genotype = []
        for allele1 in score_des_alleles:
            for allele2 in score_des_alleles:
                score_diploide = score_des_alleles[allele1] + score_des_alleles[allele2]
                liste_meilleur_genotype.append((allele1, allele2, score_diploide))
        liste_meilleur_genotype = sorted(liste_meilleur_genotype, reverse=True, key=lambda tup: tup[2])
        return liste_meilleur_genotype

    def ecrire_le_genotype(self, meilleurs_genotypes):
        """
        Ecrit la liste des 10 meilleurs génotypes et leur score sur le terminal
        entré:
            meilleurs_genotypes(list) = liste de tuple trié de manière décroissante suivant le score et contenant les deux
            allèles ainsi que le score du génotype.

        """
        print("meilleur score possible = {} \n".format(self.nombre_read*151*2))
        for i in range(0, 2*conf.COMBIEN_PRINT):
            print(meilleurs_genotypes[i])





class Selecion_Read_Pair:
    """
    Cette classe a pour rôle de vérifier si les pairs de reads après alignage sont compatibles avec la réalité biologique
    entrés:
          tuple_read1(list) = liste de tous les reads acceptés après alignements, contient son score et sa position
          tuple_read2(list) = liste de tous les reads acceptés après alignements, contient son score et sa position du read pair
    """
    def __init__(self, liste_tuple_read1, liste_tuple_read2):
        self.liste_tuple_read1 = liste_tuple_read1
        self.liste_tuple_read2 = liste_tuple_read2


    def selection_read_position(self, tuple_read1, tuple_read2):
        """
        Vérifie si deux positions plausibles d'un read et de son read pair sont compatibles
        entrés:
               tuple_read1(tup) = tuple contenant le score et la position du read
               tuple_read2(tup = tuple contenant le score et la position du second read
        retour:
               (bool) = booléen indiquant si les positions sont acceptables
        """
        distance = abs(tuple_read1[1] - tuple_read2[1])
        accepte = conf.DISTANCE_ACCEPTEE
        if distance in accepte:
            return True
        else:
            return False

    def premiere_selection(self):
        """
        Fait un premier tri dans les reads que l'on aura trouvé après alignement
        sorti:
            liste_reads_paires_acceptes(list) = liste des pairs de reads acceptés contient deux tuples ayant la position
            et le score du read.
        """
        liste_reads_paires_acceptes = []
        for tuple1 in self.liste_tuple_read1:
            for tuple2 in self.liste_tuple_read2:
                if self.selection_read_position(tuple1, tuple2):
                    liste_reads_paires_acceptes.append((tuple1, tuple2))
        return liste_reads_paires_acceptes

    def selection_meilleurs_couple_read(self, liste_de_pair_de_reads):
        """
        Choisi la pair de read ayant le meilleurs score
        sorti
            meilleur_score(int) = meilleurs score qu'a la pair de read
        """
        meilleur_score = 0
        for pair_de_tuple in liste_de_pair_de_reads:
            score_pair = pair_de_tuple[0][0] + pair_de_tuple[1][0]
            if score_pair > meilleur_score and score_pair > conf.SCORE_SEUIL_PAIR_DE_READ:
                meilleur_score = score_pair
        return meilleur_score

    def run_selection(self):
        """
        Lance tout le système de selection de la pair de reads pour en sortir leur meilleur score
        sorti:
            meilleur_score(int) = meilleur score de la pair de read
        """
        liste_acceptee = self.premiere_selection()
        meilleur_score = self.selection_meilleurs_couple_read(liste_acceptee)
        return meilleur_score


def reverse_complement(dictionnaire_read_a_inverser):
    dic_convert = {"A" : "T", "C" : "G", "G": "C", "T": "A"}
    dic_complement = {}
    for read in dictionnaire_read_a_inverser:
        dic_complement[read] = ""
        for base in dictionnaire_read_a_inverser[read]:
            dic_complement[read] = dic_convert[base.upper()] + dic_complement[read]
    return dic_complement








class Recherche_De_Nouveau_Doigt:
    """
    non fini
    """
    def __init__(self, reads_non_lie):
        self.liste_reads = reads_non_lie




if __name__ == '__main__':
    seq3 = "Sequencesallelesflanquees.fa"
    instance = FastX_To_Dico(seq3)
    dictionnaire_allele =instance.run_fastx()
    for i in range(0,1):
        seq1 = conf.SEQUENCES_TEST[i]
        seq2 = conf.SEQUENCES_TEST[i+1]
        dictionnaire_read = FastX_To_Dico(seq1).run_fastx()
        dictionnaire_pair = FastX_To_Dico(seq2).run_fastx()
        boot = Alignement_Read_Allele(dictionnaire_read, dictionnaire_pair, dictionnaire_allele)
        run = boot._choix_du_genotype()
        print(run)