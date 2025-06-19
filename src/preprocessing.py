"""Turn raw CSV into balanced panel matrices for SCM."""

import argparse
import pathlib
import pandas as pd
import yaml

def preprocess(cfg_path: str) -> None:
    cfg = yaml.safe_load(open(cfg_path))

    df = pd.read_csv("data_raw/wdi_panel.csv")
    df = df[(df.year >= cfg["start_year"]) & (df.year <= cfg["end_year"])]

    gdp = df.pivot(index="year", columns="country", values="gdp_pc")

    # drop countries with any missing data
    gdp = gdp.dropna(axis=1, how="any")
    donors = [c for c in cfg["donors"] if c in gdp.columns]

    pathlib.Path("data_processed").mkdir(exist_ok=True)
    gdp.to_pickle("data_processed/gdp.pkl")
    pd.Series(donors).to_csv("data_processed/donors.csv", index=False, header=False)
    print("✅  GDP matrix + donor list ready → data_processed/")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config/vnm.yml")
    args = p.parse_args()
    preprocess(args.config)
