# rctevaluation

This repository provides simple utilities for evaluating randomized and observational studies without relying on heavy dependencies.

The `analysis_tools.py` module contains helpers for computing t-tests, difference-in-differences, and a lightweight synthetic control on small CSV datasets using only Python's standard library. A small demonstration dataset is provided in `example_data.csv`.

## Usage

```bash
python analysis_tools.py example_data.csv
```

This command loads the example dataset, computes the difference-in-differences estimate and performs a basic t-test between treatment and control groups for the post-treatment period. It can also construct a simple synthetic control for a treated region.

## AidData Scraper

The repository includes `aiddata_scraper.py`, a simple utility to download dataset files linked from a web page on AidData. It searches the page for CSV, ZIP, Excel, or JSON links and saves them to a chosen directory. Please review AidData's terms of service before running automated downloads.

```bash
python aiddata_scraper.py https://www.aiddata.org/ data
```
