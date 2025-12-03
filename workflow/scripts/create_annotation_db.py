import gffutils
from snakemake.script import snakemake


def create_annotation_db(gff_file, db_file):
    db = gffutils.create_db(gff_file, db_file, merge_strategy="create_unique")
    db.update(list(db.create_introns()))


create_annotation_db(snakemake.input[0], snakemake.output[0])
