from Bio.SeqUtils import seq1
import re


def parse_aa_substitution(HGVS_string):
    prot_match = re.match(r"p\.([A-Z]{1}[a-z]{2})\d+([A-Z]{1}[a-z]{2})", HGVS_string)
    reference, alternative = prot_match.groups()
    return seq1(reference), seq1(alternative)


def parse_dna_substitution(HGVS_string):
    dna_match = re.search(r"c\..*([ATCG])>([ATCG])$", HGVS_string)
    reference, alternative = dna_match.groups()
    return reference, alternative


def get_start_end_from_seq(seq):
    range = seq.id.split("|")[2]
    _chrom, range = range.split(":")
    start, end = range.split("-")
    return int(start), int(end)


# parse_dna_substitution("p.Leu16Val/c.46T>G")

# parse_aa_substitution("p.Leu16Val/c.46T>G")
