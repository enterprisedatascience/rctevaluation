import os
import sys
from typing import Optional

from analysis_tools import (
    load_dataset,
    difference_in_differences,
    synthetic_control,
)

try:
    from aiddata_scraper import scrape_datasets
except Exception:  # requests might not be installed
    scrape_datasets = None


def plan_research_design(dataset_path: str, output_dir: str) -> Optional[str]:
    """Create a simple research design summary and return a treated region."""
    data = load_dataset(dataset_path)
    treated_regions = sorted({d["region"] for d in data if d["treatment"] == 1})
    if not treated_regions:
        treated_region = None
    else:
        treated_region = treated_regions[0]

    design_text = (
        "This automated study uses a synthetic control approach to estimate the "
        "effect of treatment in a panel dataset. The unit of analysis is 'region' "
        "and observations are available for a pre-treatment and post-treatment "
        "period. The first treated region in the dataset will be compared with a "
        "weighted combination of control regions."
    )
    with open(os.path.join(output_dir, "research_design.txt"), "w") as f:
        f.write(design_text)
    return treated_region


def run_synthetic_control(dataset_path: str, treated_region: str, output_dir: str) -> None:
    data = load_dataset(dataset_path)
    did_effect = difference_in_differences(data)
    sc = synthetic_control(data, treated_region)

    results_path = os.path.join(output_dir, "results.txt")
    with open(results_path, "w") as f:
        f.write(f"Difference-in-differences effect: {did_effect:.2f}\n")
        f.write(
            f"Synthetic control effect for {treated_region}: {sc['effect']:.2f}\n"
        )
        f.write(f"Synthetic control weights: {sc['weights']}\n")


def generate_report(output_dir: str) -> str:
    design_file = os.path.join(output_dir, "research_design.txt")
    results_file = os.path.join(output_dir, "results.txt")
    report_path = os.path.join(output_dir, "study_report.txt")
    with open(report_path, "w") as out, open(design_file) as d, open(results_file) as r:
        out.write("=== Research Design ===\n")
        out.write(d.read())
        out.write("\n\n=== Results ===\n")
        out.write(r.read())
        out.write("\nThis report was generated automatically.\n")
    return report_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python pipeline.py <dataset.csv> <output_dir> [start_url]")
        sys.exit(1)
    dataset_path = sys.argv[1]
    output_dir = sys.argv[2]
    start_url = sys.argv[3] if len(sys.argv) > 3 else None

    os.makedirs(output_dir, exist_ok=True)

    if start_url:
        if scrape_datasets is None:
            print("aiddata_scraper dependency missing; skipping download step.")
        else:
            scrape_datasets(start_url, output_dir)

    treated_region = plan_research_design(dataset_path, output_dir)
    if treated_region is None:
        print("No treated region found in the dataset.")
        sys.exit(1)

    run_synthetic_control(dataset_path, treated_region, output_dir)
    report_path = generate_report(output_dir)
    print(f"Study published to {report_path}")


if __name__ == "__main__":
    main()
