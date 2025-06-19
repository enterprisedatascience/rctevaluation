"""One‑stop orchestration script."""

import argparse
import subprocess

CMD = [
    ["python", "src/fetch_data.py"],
    ["python", "src/preprocessing.py"],
    ["python", "src/synthetic_control.py"],
    ["papermill", "notebooks/report_template.ipynb", "output/report_filled.ipynb"],
    [
        "jupyter", "nbconvert", "--to", "pdf",
        "--output", "Vietnam_Aid_Study.pdf", "output/report_filled.ipynb",
    ],
]


def main(cfg: str) -> None:
    env_arg = ["--config", cfg]
    for c in CMD[:3]:  # first three accept --config
        subprocess.check_call(c + env_arg)
    for c in CMD[3:]:  # papermill & nbconvert take no custom arg here
        subprocess.check_call(c)
    print("\n🏁  Pipeline complete – find PDF in output/\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config/vnm.yml")
    args = p.parse_args()
    main(args.config)
