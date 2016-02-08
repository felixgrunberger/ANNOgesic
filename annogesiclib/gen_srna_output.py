import os
import sys
import csv
from copy import deepcopy
from annogesiclib.gff3 import Gff3Parser


def import_data(row, type_):
    if type_ == "gff":
        if len(row) == 15:
            return {"strain": row[0], "name": row[1], "start": int(row[2]),
                    "end": int(row[3]), "strand": row[4], "conds": row[5],
                    "detect": row[6], "tss_pro": row[7], "end_pro": row[8],
                    "avg": float(row[9]), "high": float(row[10]),
                    "low": float(row[11]), "track": row[12],
                    "overlap_CDS": row[13], "overlap_percent": row[14]}
        else:
            return {"strain": row[0], "name": row[1], "start": int(row[2]),
                    "end": int(row[3]), "strand": row[4], "conds": row[5],
                    "detect": row[6], "tss_pro": row[7], "end_pro": row[8],
                    "avg": float(row[9]), "high": float(row[10]),
                    "low": float(row[11]), "overlap_CDS": row[13],
                    "overlap_percent": row[14]}
    elif type_ == "nr":
        if len(row) == 8:
            return {"strain": row[0], "name": row[1], "strand": row[2],
                    "start": int(row[3]), "end": int(row[4]),
                    "hits": "|".join(row[5:8])}
        elif len(row) == 6:
            return {"strain": row[0], "name": row[1], "strand": row[2],
                    "start": int(row[3]), "end": int(row[4]), "hits": row[5]}
    elif type_ == "sRNA":
        if len(row) == 7:
            return {"strain": row[0], "name": row[1], "strand": row[2],
                    "start": int(row[3]), "end": int(row[4]),
                    "hits": "|".join(row[5:])}
        elif len(row) == 6:
            return {"strain": row[0], "name": row[1], "strand": row[2],
                    "start": int(row[3]), "end": int(row[4]), "hits": row[5]}

def merge_info(blasts):
    first = True
    finals = []
    if len(blasts) != 0:
        for blast in blasts:
            if first:
                repeat = 0
                first = False
                pre_blast = deepcopy(blast)
            else:
                if (pre_blast["strain"] == blast["strain"]) and (
                    pre_blast["strand"] == blast["strand"]) and (
                    pre_blast["start"] == blast["start"]) and (
                    pre_blast["end"] == blast["end"]):
                    if (repeat < 2):
                        pre_blast["hits"] = ";".join([pre_blast["hits"], blast["hits"]])
                        repeat += 1
                else:
                    repeat = 0
                    finals.append(pre_blast)
                    pre_blast = blast.copy()
        finals.append(pre_blast)
    return finals

def compare_srna_table(srna_tables, srna, final, min_len, max_len):
    for table in srna_tables:
        tsss = []
        pros = []
        cands = []
        if (table["strain"] == srna.seq_id) and (
            table["strand"] == srna.strand) and (
            table["start"] == srna.start) and (
            table["end"] == srna.end):
            final = dict(final, **table)
            start_datas = table["tss_pro"].split(";")
            end_datas = table["end_pro"].split(";")
            tsss.append(table["start"])
            pros.append(table["end"])
            for data in start_datas:
                if "TSS" in data:
                    if table["start"] != int(data.split(":")[1][:-2]):
                        tsss.append(int(data.split(":")[1][:-2]))
                elif "Cleavage" in data:
                    if table["end"] != int(data.split(":")[1][:-2]):
                        pros.append(int(data.split(":")[1][:-2]))
            for data in end_datas:
                if "Cleavage" in data:
                    if table["end"] != int(data.split(":")[1][:-2]):
                        pros.append(int(data.split(":")[1][:-2]))
            for tss in tsss:
                for pro in pros:
                    if ((pro - tss) >= min_len) and (
                        (pro - tss) <= max_len):
                        cands.append("-".join([str(tss), str(pro)]))
            final["candidates"] = ";".join(cands)
            if ("tex" in table["conds"]) and (
                "frag" in table["conds"]):
                final["type"] = "TEX+/-;Fragmented"
            elif ("tex" in table["conds"]):
                final["type"] = "TEX+/-"
            elif ("frag" in table["conds"]):
                final["type"] = "Fragmented"
    return final

def compare_blast(blasts, srna, final, hit):
    for blast in blasts:
        if (srna.seq_id == blast["strain"]) and (
            srna.strand == blast["strand"]) and (
            srna.start == blast["start"]) and (
            srna.end == blast["end"]):
            final[hit] = blast["hits"]
    return final

def check_keys(ref_key, final_key, srna, final):
    if ref_key in srna.attributes.keys():
        final[final_key] = srna.attributes[ref_key]
    else:
        if (final_key == "nr_hit_num") or (
            final_key == "sRNA_hit_num"):
            final[final_key] = "0"
        else:
            final[final_key] = "NA"

def compare(srnas, srna_tables, nr_blasts, srna_blasts, min_len, max_len):
    finals = []
    for srna in srnas:
        final = {}
        check_keys("2d_energy", "energy", srna, final)
        check_keys("nr_hit", "nr_hit_num", srna, final)
        check_keys("sRNA_hit", "sRNA_hit_num", srna, final)
        check_keys("sORF", "sORF", srna, final)
        check_keys("end_pro", "end_pro", srna, final)
        if srna.attributes["sRNA_type"] == "intergenic":
            final["utr"] = "Intergenic"
        elif srna.attributes["sRNA_type"] == "in_CDS":
            final["utr"] = "in_CDS"
        else:
            if "&" in srna.attributes["sRNA_type"]:
                final["utr"] = "5'UTR_derived;3'UTR_derived"
            elif srna.attributes["sRNA_type"] == "5utr":
                final["utr"] = "5'UTR_derived"
            elif srna.attributes["sRNA_type"] == "3utr":
                final["utr"] = "3'UTR_derived"
            elif srna.attributes["sRNA_type"] == "interCDS":
                final["utr"] = "interCDS"
        final = compare_srna_table(srna_tables, srna, final, min_len, max_len)
        final = compare_blast(nr_blasts, srna, final, "nr_hit")
        final = compare_blast(srna_blasts, srna, final, "sRNA_hit")
        finals.append(final)
    return finals

def print_file(finals, out):
    rank = 1
    for final in finals:
        if "nr_hit" not in final.keys():
            final["nr_hit"] = "NA"
        if "sRNA_hit" not in final.keys():
            final["sRNA_hit"] = "NA"
        if "with_term" not in final.keys():
            final["with_term"] = "NA"
        out.write("\t".join([str(rank),
                  final["strain"], final["name"], str(final["start"]),
                  str(final["end"]), final["strand"], final["tss_pro"],
                  final["end_pro"], final["candidates"], final["type"],
                  str(final["avg"]), str(final["high"]), str(final["low"]),
                  final["track"], final["energy"], final["utr"], final["sORF"],
                  final["nr_hit_num"], final["sRNA_hit_num"],
                  final["nr_hit"], final["sRNA_hit"], final["overlap_CDS"],
                  str(final["overlap_percent"]), final["with_term"]]) + "\n")
        rank += 1

def read_table(srna_table_file, nr_blast, srna_blast_file):
    srna_tables = []
    nr_blasts = []
    srna_blasts = []
    f_h = open(srna_table_file, "r")
    for row in csv.reader(f_h, delimiter='\t'):
        srna_tables.append(import_data(row, "gff"))
    f_h.close()
    if os.path.exists(nr_blast):
        f_h = open(nr_blast, "r")
        for row in csv.reader(f_h, delimiter='\t'):
            nr_blasts.append(import_data(row, "nr"))
        f_h.close()
    if os.path.exists(srna_blast_file):
        f_h = open(srna_blast_file, "r")
        for row in csv.reader(f_h, delimiter='\t'):
            srna_blasts.append(import_data(row, "sRNA"))
        f_h.close()
    return srna_tables, nr_blasts, srna_blasts

def read_gff(srna_gff):
    srnas = []
    for entry in Gff3Parser().entries(open(srna_gff)):
        srnas.append(entry)
    srnas = sorted(srnas, key=lambda k: (k.seq_id, k.start))
    return srnas

def gen_srna_table(srna_gff, srna_table_file, nr_blast, srna_blast_file,
                   max_len, min_len, out_file):
    srnas = read_gff(srna_gff)
    srna_tables, nr_blasts, srna_blasts = read_table(srna_table_file,
                                          nr_blast, srna_blast_file)
    out = open(out_file, "w")
    out.write("\t".join(["rank", "strain", "name", "start", "end", "strand",
                         "start_with_TSS/Cleavage_site", "end_with_cleavage",
                         "candidates", "lib_type", "best_avg_coverage",
                         "best_highest_coverage", "best_lower_coverage",
                         "track/coverage", "normalized_secondary_energy_change(by_length)",
                         "UTR_derived/Intergenic", "confliction_of_sORF",
                         "nr_hit_number", "sRNA_hit_number",
                         "nr_hit_top3|ID|e-value", "sRNA_hit|e-value",
                         "overlap_CDS", "overlap_percent", "end_with_terminator"]) + "\n")
    nr_blasts = merge_info(nr_blasts)
    srna_blasts = merge_info(srna_blasts)
    finals = compare(srnas, srna_tables, nr_blasts,
                     srna_blasts, min_len, max_len)
    sort_finals = sorted(finals, key=lambda x: (x["avg"]), reverse=True)
    print_file(sort_finals, out)

def print_best(detect, out, srna):
    no_print = False
    for value in detect.values():
        if not value:
            no_print = True
    if not no_print:
        out.write(srna.info + "\n")

def gen_best_srna(srna_file, all_srna_hit, energy, hit_nr_num,
                  compare_sorf, out_file, best_term):
    srnas = read_gff(srna_file)
    out = open(out_file, "w")
    out.write("##gff-version 3\n")
    for srna in srnas:
        detect = {"energy": False, "TSS": False, "nr_hit": False,
                  "sRNA_hit": False, "sORF": False, "term": False}
        if "2d_energy" in srna.attributes.keys():
            if float(srna.attributes["2d_energy"]) < energy:
                detect["energy"] = True
        else:
            detect["energy"] = True
        if "with_TSS" in srna.attributes.keys():
            if srna.attributes["with_TSS"] != "NA":
                detect["TSS"] = True
            elif (srna.attributes["sRNA_type"] != "intergenic") and (
                  srna.attributes["sRNA_type"] != "in_CDS"):
                if (("3utr" in srna.attributes["sRNA_type"]) or (
                     "interCDS" in srna.attributes["sRNA_type"])) and (
                     srna.attributes["start_cleavage"] != "NA"):
                    detect["TSS"] = True
        else:
            detect["TSS"] = True
        if "nr_hit" in srna.attributes.keys():
            if (srna.attributes["nr_hit"] == "NA") or (
                int(srna.attributes["nr_hit"]) <= hit_nr_num):
                detect["nr_hit"] = True
        else:
            detect["nr_hit"] = True
        if (compare_sorf):
            if ("sORF" in srna.attributes.keys()):
                if srna.attributes["sORF"] == "NA":
                    detect["sORF"] = True
        else:
            detect["sORF"] = True
        if ("sRNA_hit" in srna.attributes.keys()) and (all_srna_hit):
            if (srna.attributes["sRNA_hit"] != "NA"):
                for key in detect.keys():
                    detect[key] = True
            else:
                count = 0
                for value in detect.values():
                    if value:
                        count += 1
                if count == 4:
                    detect["sRNA_hit"] = True
        else:
            detect["sRNA_hit"] = True
        if best_term:
            if ("with_term" in srna.attributes.keys()):
                if srna.attributes["with_term"] != "NA":
                    detect["term"] = True
                elif ("end_cleavage" in srna.attributes.keys()):
                    if srna.attributes["end_cleavage"] != "NA":
                        detect["term"] = True
        else:
            detect["term"] = True
        print_best(detect, out, srna)
    out.close()
