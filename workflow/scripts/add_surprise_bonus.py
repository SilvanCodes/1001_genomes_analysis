import numpy as np
import pandas as pd
from snakemake.script import snakemake


def add_surprise_bonus(input_path, output_path):
    df = pd.read_csv(input_path)
    # Entropy H in base-4
    df["H"] = -(
        df[["p_a", "p_c", "p_g", "p_t"]]
        .pipe(lambda p: p * (np.log2(p) / 2))
        .sum(axis=1)
    )

    # Surprisal I in base-4
    df["I"] = -(np.log2(df["p_alt"]) / 2)
    df["surprise bonus"] = df["H"] - df["I"]

    df.to_csv(output_path, index=False)


add_surprise_bonus(snakemake.input[0], snakemake.output[0])
