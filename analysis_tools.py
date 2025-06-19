import csv
import math
from statistics import mean, variance
from typing import List, Dict, Tuple


def _compute_weights(target: float, candidates: List[float]) -> List[float]:
    """Return non-negative weights that sum to 1 favoring values close to the target."""
    diffs = [abs(target - c) + 1e-6 for c in candidates]
    inv = [1.0 / d for d in diffs]
    total = sum(inv)
    return [w / total for w in inv]


def load_dataset(path: str) -> List[Dict[str, float]]:
    """Load a CSV dataset into a list of dictionaries."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            converted = {
                "region": row["region"],
                "time": float(row["time"]),
                "treatment": float(row["treatment"]),
                "outcome": float(row["outcome"]),
            }
            data.append(converted)
    return data


def mean_difference(sample1: List[float], sample2: List[float]) -> float:
    """Return the difference in sample means."""
    return mean(sample1) - mean(sample2)


def normal_cdf(x: float) -> float:
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def independent_ttest(sample1: List[float], sample2: List[float]) -> Tuple[float, float]:
    """Compute a two-sided t-test with normal approximation for the p-value."""
    n1 = len(sample1)
    n2 = len(sample2)
    var1 = variance(sample1)
    var2 = variance(sample2)
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    se = math.sqrt(pooled_var * (1 / n1 + 1 / n2))
    t_stat = (mean(sample1) - mean(sample2)) / se
    p_value = 2 * (1 - normal_cdf(abs(t_stat)))
    return t_stat, p_value


def difference_in_differences(data: List[Dict[str, float]], pre: float = 0.0, post: float = 1.0) -> float:
    """Compute a simple difference-in-differences estimate."""
    pre_treat = [d["outcome"] for d in data if d["treatment"] == 1 and d["time"] == pre]
    post_treat = [d["outcome"] for d in data if d["treatment"] == 1 and d["time"] == post]
    pre_control = [d["outcome"] for d in data if d["treatment"] == 0 and d["time"] == pre]
    post_control = [d["outcome"] for d in data if d["treatment"] == 0 and d["time"] == post]

    diff_treat = mean(post_treat) - mean(pre_treat)
    diff_control = mean(post_control) - mean(pre_control)
    return diff_treat - diff_control


def synthetic_control(
    data: List[Dict[str, float]],
    treated_region: str,
    pre: float = 0.0,
    post: float = 1.0,
) -> Dict[str, float]:
    """Compute a very simple synthetic control estimate for a single treated region."""
    pre_outcomes = {d["region"]: d["outcome"] for d in data if d["time"] == pre}
    post_outcomes = {d["region"]: d["outcome"] for d in data if d["time"] == post}

    treated_pre = pre_outcomes[treated_region]
    treated_post = post_outcomes[treated_region]

    control_regions = [r for r in pre_outcomes.keys() if r != treated_region]
    control_pre = [pre_outcomes[r] for r in control_regions]
    control_post = [post_outcomes[r] for r in control_regions]

    weights = _compute_weights(treated_pre, control_pre)

    synth_pre = sum(w * x for w, x in zip(weights, control_pre))
    synth_post = sum(w * x for w, x in zip(weights, control_post))

    effect = (treated_post - synth_post) - (treated_pre - synth_pre)

    return {
        "weights": dict(zip(control_regions, weights)),
        "effect": effect,
        "synthetic_pre": synth_pre,
        "synthetic_post": synth_post,
    }


def run_analysis(path: str) -> None:
    data = load_dataset(path)
    did_effect = difference_in_differences(data)
    post_treat = [d["outcome"] for d in data if d["treatment"] == 1 and d["time"] == 1]
    post_control = [d["outcome"] for d in data if d["treatment"] == 0 and d["time"] == 1]
    t_stat, p_value = independent_ttest(post_treat, post_control)
    print(f"Difference-in-differences effect: {did_effect:.2f}")
    print(f"Post-period t-test: t={t_stat:.3f}, p≈{p_value:.3f}")

    treated_regions = sorted({d["region"] for d in data if d["treatment"] == 1 and d["time"] == 1})
    if treated_regions:
        sc = synthetic_control(data, treated_regions[0])
        print(
            f"Synthetic control effect for {treated_regions[0]}: {sc['effect']:.2f}"
        )
        print(f"Synthetic control weights: {sc['weights']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python analysis_tools.py <dataset.csv>")
    else:
        run_analysis(sys.argv[1])
