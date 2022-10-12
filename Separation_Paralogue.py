#!/usr/bin/env python3
#
# coding: utf-8
#

import sys


class Separation_PRDM9_Paralogue:
    CHROMOSOME_LIST_ACCEPTED = ["chr5", "a", "b", "c", "d", "e", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9",
                                "L10",
                                "L11", "L12", "L13", "L14", "L15", "L16", "L17", "L18", "L19", "L20",
                                "L21", "L22", "L23", "L24", "L25", "L26", "L27"]

    def __init__(self, sam_file, new_sam_file):
        self.file = sam_file
        self.sorted_sam = new_sam_file
        self.dic_to_sort, self.head = self.sam_to_dic()

    def sam_to_dic(self):
        dictionnaire_a_read = {}
        head = []
        with open(self.file, "r") as file:
            for line in file:
                table = line.split("\t")
                if table[0][0] != "@":
                    if table[0] in dictionnaire_a_read.keys():
                        if table[9] in dictionnaire_a_read[table[0]].keys():
                            dictionnaire_a_read[table[0]][table[9]].append(line)
                        else:
                            dictionnaire_a_read[table[0]][table[9]] = [line]
                    else:
                        dictionnaire_a_read[table[0]] = {}
                        dictionnaire_a_read[table[0]][table[9]] = [line]
                else:
                    head.append(line)
        return dictionnaire_a_read, head

    def accepted_position(self, read):

        if read[2] == self.CHROMOSOME_LIST_ACCEPTED[0]:
            start = int(read[3])
            if start >= 23443586 and start <= 23528597:
                return True
            else:
                return False
        elif read[2] in self.CHROMOSOME_LIST_ACCEPTED[1:]:
            return True
        else:
            return False

    def sort_reads(self, dic_to_sort):
        dic_sorted = {}
        for key in dic_to_sort:
            dic_sorted[key] = {}
            for key2 in dic_to_sort[key]:
                list_of_best = self.which_best(dic_to_sort[key][key2])
                number_in_list = 0
                accepted = False
                while number_in_list < len(list_of_best) and accepted == False:
                    cut = dic_to_sort[key][key2][list_of_best[number_in_list]].split('\t')
                    accepted = self.accepted_position(cut)
                    if accepted:
                        dic_sorted[key][key2] = dic_to_sort[key][key2][list_of_best[number_in_list]]
                    number_in_list += 1
            if key in dic_sorted.keys():
                if len(dic_sorted[key]) < 2:
                    del dic_sorted[key]
        return dic_sorted

    def write_new_sam(self, dic_sorted, head):
        with open(self.sorted_sam, "w") as file:
            for line in head:
                file.write(line)
            for key in dic_sorted:
                for key2 in dic_sorted[key]:
                    for read in dic_sorted[key][key2]:
                        file.write(read)

    def best_score(self, cigar):
        dico_nombre = {"M": 0, "I": 0, "D": 0, "H": 0, "S": 0, "N": 0, "P": 0}
        nombre = ""
        for lettre in cigar:
            if lettre in ["M", "I", "D", "H", "S", "N", "P"]:
                dico_nombre[lettre] += int(nombre)
                nombre = ""
            else:
                nombre += lettre
        return dico_nombre["M"]

    def which_best(self, liste_reads):
        num_list = 0
        best_score = 0
        list_to_keep = []
        while num_list < len(liste_reads):
            cut = liste_reads[num_list].split('\t')
            score_read = self.best_score(cut[5])
            if score_read > best_score:
                best_score = score_read
                list_to_keep = [num_list]
            elif score_read == best_score:
                list_to_keep.append(num_list)
            num_list += 1
        return list_to_keep

    def run_all(self):
        dic_to_keep = self.sort_reads(self.dic_to_sort)
        self.write_new_sam(dic_to_keep, self.head)


if __name__ == '__main__':
    input_seq_file = sys.argv[1]
    output_seq_file = "data/alignNoParalogue.sam"
    boot = Separation_PRDM9_Paralogue(input_seq_file, output_seq_file)
    boot.run_all()
