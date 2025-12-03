localrules:
    download_ncbi_dataset,
    unpack_ncbi_dataset,


rule download_ncbi_dataset:
    output:
        "resources/download_ncbi_dataset/{accession}.zip",
    conda:
        "../envs/download_ncbi_dataset.yaml"
    message:
        """--- Downloading NCBI dataset for {wildcards.accession}."""
    shell:
        "datasets download genome accession {wildcards.accession} --include genome,gff3 --filename {output}"


rule unpack_ncbi_dataset:
    input:
        "resources/download_ncbi_dataset/{accession}.zip",
    output:
        "resources/unpack_ncbi_dataset/{accession}/genome.fna",
        "resources/unpack_ncbi_dataset/{accession}/annotation.gff",
    params:
        data_path="/tmp/ncbi_dataset/data",
    shell:
        "unzip {input} -d /tmp"
        " && genome_path=$(cat {params.data_path}/dataset_catalog.json | jq -r '.assemblies[1].files | .[] | select(.fileType==\"GENOMIC_NUCLEOTIDE_FASTA\").filePath')"
        " && annotation_path=$(cat {params.data_path}/dataset_catalog.json | jq -r '.assemblies[1].files | .[] | select(.fileType==\"GFF3\").filePath')"
        " && mv {params.data_path}/$genome_path {output[0]}"
        " && mv {params.data_path}/$annotation_path {output[1]}"
