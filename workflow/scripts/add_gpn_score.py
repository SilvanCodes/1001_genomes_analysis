from helpers import parse_dna_substitution
import pandas as pd

import gpn.model
import gpn.pipelines
from transformers import pipeline


def get_gpn_score(variant):
    ref, alt = parse_dna_substitution(variant["amino acid change"])

    return variant[f"gpn_{alt.lower()}"]


def add_gpn_score(df):
    gpn_pipeline = pipeline("gpn")

    gpn_scores = pd.concat(
        gpn_pipeline(df["sequence_window"], start=256, end=257, batch_size=8),
        ignore_index=True,
    )

    df = pd.concat([df, gpn_scores], axis=1)

    df["gpn_score"] = df.apply(lambda x: get_gpn_score(x), axis=1)
    return df
