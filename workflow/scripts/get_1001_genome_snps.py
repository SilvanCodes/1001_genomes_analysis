from snakemake.script import snakemake
import requests
import pandas as pd


def get_1001_genome_snps(base_url, gene_id, output_path):
    url = f"{base_url};gid={gene_id}"
    snp_effects_response = requests.get(url)

    df = pd.DataFrame(
        snp_effects_response.json()["data"],
        columns=[
            "chromosome",
            "position",
            "accession id",
            "type",
            "effect impact",
            "functional class",
            "codon change",
            "amino acid change",
            "amino acid length",
            "gene name",
            "transcript biotype",
            "gene coding",
            "transcript id",
            "exon rank",
        ],
    )

    df.to_csv(output_path[0], index=False)

    df = df.drop_duplicates(subset=["amino acid change"])

    df.to_csv(output_path[1], index=False)


get_1001_genome_snps(
    snakemake.params.base_url, snakemake.wildcards.gene_id, snakemake.output
)
