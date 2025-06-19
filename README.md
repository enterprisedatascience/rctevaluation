## Aid Effectiveness – Synthetic Control Pipeline (Vietnam example)

This repository automates a full synthetic–control study that estimates the impact of foreign aid on a country's GDP.
The default configuration replicates the Vietnam 1994 aid‑shock example from our ChatGPT session, but **any** country
and treatment year can be analysed by changing a single YAML file.

### Quick start
```bash
# clone and enter
git clone <your‑repo‑url>.git
cd vietnam-aid-synth

conda env create -n aid_synth -f environment.yml   # OR: pip install -r requirements.txt
conda activate aid_synth

python src/run_pipeline.py              # <- produces output/Vietnam_Aid_Study.pdf
```

See **docs/usage.md** for detailed instructions and troubleshooting.
