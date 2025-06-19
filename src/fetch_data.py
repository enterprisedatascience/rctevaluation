"""Download GDP & ODA series from the World Bank API and cache as CSV."""

import argparse
import pathlib
import yaml
import pandas as pd
import wbgapi as wb

INDICATORS = {
    "NY.GDP.PCAP.KD": "gdp_pc",     # GDP per capita (constant 2015 USD)
    "DT.ODA.ODAT.KD": "oda_const"   # Net ODA received (constant USD)
}

def fetch(cfg_path: str) -> None:
    cfg = yaml.safe_load(open(cfg_path))
    all_countries = cfg["donors"] + [cfg["treat_country"]]

    panel = (
        wb.data.DataFrame(INDICATORS, all_countries,
                          time=range(cfg["start_year"], cfg["end_year"] + 1))
        .reset_index()
        .rename(columns={"economy": "country", "time": "year"})
    )

    out = pathlib.Path("data_raw/wdi_panel.csv")
    out.parent.mkdir(exist_ok=True)
    panel.to_csv(out, index=False)
    print(f"✅  Saved World‑Bank panel → {out.relative_to(pathlib.Path().resolve())}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/vnm.yml")
    args = parser.parse_args()
    fetch(args.config)
