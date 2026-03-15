import pandas as pd
import numpy as np
import calplot
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, PowerNorm
from matplotlib import cm
import matplotlib.patches as mpatches

LINE_COLORS = {
    "NSL": "#d32f2f",
    "EWL": "#2e7d32",
    "DTL": "#1565c0",
    "CCL": "#ffc422",
    "NEL": "#6a1b9a",
    "TEL": "#9a5a1bec",
    "LRT": "#6f6f6f",
    "Mixed": "#000000"
}

lines = list(LINE_COLORS.keys())


base_cmap = cm.get_cmap("YlOrRd")
colors = base_cmap(np.linspace(0.25, 1.0, 256))  # skip first 25%

strong_cmap = LinearSegmentedColormap.from_list(
    "YlOrRd_stronger",
    colors
)

norm = PowerNorm(gamma=0.5, vmin=0.5, vmax=8)

# Load Excel
df = pd.read_excel("./mrt_disruptions_2025_refined.xlsx")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Hours"] = pd.to_numeric(df["Hours"], errors="coerce").fillna(0)

def stretch(x):
    if x <= 1:
        return x * 1.8       # exaggerate low values
    elif x <= 2:
        return x * 1.2
    else:
        return x



def part1():
    df["Line"] = df["Line"].astype(str).str.strip()

    lines = list(LINE_COLORS.keys())

    # Encode lines starting from 1 (NOT 0)
    line_codes = {line: i + 1 for i, line in enumerate(lines)}
    df["LineCode"] = df["Line"].map(line_codes)

    assert df["LineCode"].notna().all(), "Unmapped MRT lines detected"

    cmap = ListedColormap([LINE_COLORS[line] for line in lines])

    values_line = pd.Series(
        df["LineCode"].values,
        index=df["Date"]
    )

    calplot.calplot(
        values_line,
        cmap=cmap,
        vmin=1,
        vmax=len(lines),
        suptitle="MRT Disruptions by Line",
        colorbar=False
    )

    plt.show()

def part2(): 
    values_hours = pd.Series( df["Hours"].values, index=df["Date"] ) 
    scaled = (values_hours - 0.4) / (8 - 0.5)
    values_stretched = values_hours.apply(stretch)

    calplot.calplot(
    values_stretched,
    cmap=strong_cmap,
    suptitle="MRT Disruption Severity (Hours)",
    colorbar=True,
    )

    plt.show()

part2()