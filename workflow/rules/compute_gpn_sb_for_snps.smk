# get snp data
# get reference genome
# compute gpn and sb for snps


rule get_genome:
    output:
        fasta="results/get_genome/genome.fna",
    conda:
        "../envs/get_genome.yaml"
    message:
        """--- Downloading genome sequence."""
    params:
        ncbi_ftp=lookup(within=config, dpath="get_genome/ncbi_ftp"),
    log:
        "results/get_genome/genome.log",
    shell:
        "wget -O results/get_genome/genome.fna.gz {params.ncbi_ftp} > {log} 2>&1 && "
        "gunzip results/get_genome/genome.fna.gz >> {log} 2>&1"
