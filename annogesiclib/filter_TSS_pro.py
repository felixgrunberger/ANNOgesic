import os
import math
from annogesiclib.gff3 import Gff3Parser
from annogesiclib.helper import Helper

def read_gff(input_file):
    datas = []
    gff_parser = Gff3Parser()
    f_h = open(input_file, "r")
    for entry in gff_parser.entries(f_h):
        datas.append(entry)
    datas = sorted(datas, key=lambda k: (k.seq_id, k.start))   
    return datas

def compare_tss_pro(tars, refs, out, cluster):
    for tar in tars:
        for ref in refs:
            if (tar.seq_id == ref.seq_id) and (
                tar.strand == ref.strand):
                if math.fabs(tar.start - ref.start) <= cluster:
                    break
                elif (ref.start - tar.start) > cluster:
                    out.write(tar.info + "\n")
                    break

def filter_tss_pro(tss_file, pro_file, feature, cluster):
    tsss = read_gff(tss_file)
    pros = read_gff(pro_file)
    out = open("tmp_filter", "w")
    out.write("##gff-version 3\n")
    if feature.lower() == "tss":
        compare_tss_pro(pros, tsss, out, cluster)
        os.remove(pro_file)
        os.rename("tmp_filter", pro_file)
    elif feature.lower() == "processing_site":
        compare_tss_pro(tsss, pros, out, cluster)
        os.remove(tss_file)
        os.rename("tmp_filter", tss_file)