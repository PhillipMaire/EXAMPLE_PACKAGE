#!/usr/bin/env python3
import os
import subprocess

# Absolute path to your notebook-style .py
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/does equipment affect rask_V2.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/modeling/subdaily_modeling_deep_dive.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/profit_margin_by_equip_historical_V6.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/comparing_pred_with_actual.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/get_data/flown_flight_plan_match_with_predictions.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/ATR_deep_dive.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/flight_aligned_plots.py"
# PY_PATH = "/Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/metrics/ATR_deep_dive_v10.py"

# /Users/phillipmaire/Documents/GitHub/azul-plf/notebooks/modeling/subdaily/example_lgbm_v4.ipynb

def init_jupytext():
    base, _ = os.path.splitext(PY_PATH)
    ipynb_path = base + ".ipynb"

    # Read existing .py
    with open(PY_PATH, "r") as f:
        lines = f.readlines()

    # 1) Remove old auto-sync block if present
    auto_start = auto_end = None
    for i, l in enumerate(lines):
        if l.strip() == "# %% AUTO SYNC":
            auto_start = i
        if l.strip() == "##########END_AUTO_ADD##########":
            auto_end = i
            break
    if auto_start is not None and auto_end is not None:
        del lines[auto_start:auto_end+1]

    # 2) Find end of Jupytext header (2nd "# ---")
    delim = [i for i, l in enumerate(lines) if l.strip() == "# ---"]
    insert_at = delim[1] + 1 if len(delim) >= 2 else 0

    # 3) Build new auto-sync block
    auto_block = [
        "# %% AUTO SYNC\n",
        "import subprocess\n",
        f"subprocess.run(['jupytext', '--sync', '{PY_PATH}'], check=True)\n",
        "\n",
        f"# To sync Python from notebook edits: jupytext --sync '{ipynb_path}'\n",
        "\n",
        "##########END_AUTO_ADD##########\n",
        "\n"
    ]

    # 4) Insert it just after the header
    new_lines = lines[:insert_at] + auto_block + lines[insert_at:]

    # 5) Write back .py
    with open(PY_PATH, "w") as f:
        f.writelines(new_lines)

    # 6) Update or create the paired notebook
    subprocess.run(["jupytext", "--to", "ipynb", PY_PATH], check=True)
    # 7) Ensure two-way pairing
    subprocess.run([
        "jupytext", "--set-formats",
        "ipynb,py:percent",
        ipynb_path
    ], check=True)

if __name__ == "__main__":
    init_jupytext()
