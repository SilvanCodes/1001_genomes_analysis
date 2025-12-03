from helpers import parse_dna_substitution
from Bio import SeqIO
import pandas as pd
from gffutils import FeatureDB
from snakemake.script import snakemake


def get_substitution_dna_window(variant, gene_sequence, gene_annotation):
    in_gene_position = variant["position"] - gene_annotation.start

    ref, _alt = parse_dna_substitution(variant["amino acid change"])

    assert ref == gene_sequence[in_gene_position].upper()

    # fails for positions close to start or end of gene
    return str(gene_sequence[in_gene_position - 256 : in_gene_position + 256].seq)


def add_sequence_window(
    snp_effect_path, reference_fasta_path, annotation_db_path, output_path
):
    annotation = FeatureDB(annotation_db_path)
    genome = SeqIO.to_dict(SeqIO.parse(reference_fasta_path, "fasta"))

    gene_annotation_id = f"gene-{snakemake.wildcards[0].split('.')[0]}"
    gene_annotation = annotation[gene_annotation_id]

    # compensate for 1-based indexing in gff
    gene_sequence = genome[gene_annotation.seqid][
        gene_annotation.start - 1 : gene_annotation.end
    ]

    df = pd.read_csv(snp_effect_path)

    # move data cleaning into seperate rule
    df = df.dropna(subset=["amino acid change"])
    df = df[~df["amino acid change"].str.contains("ins", na=False)]
    df = df[~df["amino acid change"].str.contains("del", na=False)]

    df["sequence_window"] = df.apply(
        lambda x: get_substitution_dna_window(x, gene_sequence, gene_annotation), axis=1
    )

    df.to_csv(output_path, index=False)


add_sequence_window(
    snakemake.input[2], snakemake.input[0], snakemake.input[1], snakemake.output[0]
)
