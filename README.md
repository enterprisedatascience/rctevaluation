# rctevaluation

This repository provides simple utilities for evaluating randomized and observational studies without relying on heavy dependencies.

The `analysis_tools.py` module contains helpers for computing t-tests and difference-in-differences on small CSV datasets using only Python's standard library. A small demonstration dataset is provided in `example_data.csv`.

## Usage

```bash
python analysis_tools.py example_data.csv
```

This command loads the example dataset, computes the difference-in-differences estimate and performs a basic t-test between treatment and control groups for the post-treatment period.
```
