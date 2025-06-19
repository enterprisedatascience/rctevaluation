"""Fit SCM, export synthetic series & weights."""

import argparse
import pathlib
import yaml
import numpy as np
import pandas as pd
from SyntheticControlMethods import Synth

def run_scm(cfg_path: str) -> None:
    cfg = yaml.safe_load(open(cfg_path))

    gdp = pd.read_pickle("data_processed/gdp.pkl")
    donors = pd.read_csv("data_processed/donors.csv", header=None)[0].tolist()

    df_long = (
        gdp.reset_index()
        .melt(id_vars="year", var_name="country", value_name="gdp_pc")
    )

    model = Synth(
        df_long,
        outcome="gdp_pc",
        unit="country",
        time="year",
        i0=cfg["treat_year"],
        treated_unit=cfg["treat_country"],
        donors=donors,
    )
    model.fit()

    synth = model.predict()
    pathlib.Path("output").mkdir(exist_ok=True)
    synth.to_csv("output/synth_gdp.csv")
    pd.Series(model.get_weights()).to_csv("output/donor_weights.csv")

    # gap series (VN actual – synthetic)
    gap = gdp[cfg["treat_country"]].loc[cfg["treat_year"]:] - synth
    gap.to_csv("output/gap.csv")
    print("🎯  Synthetic series, weights, gap → output/")

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--config", default="config/vnm.yml")
    run_scm(a.parse_args().config)
