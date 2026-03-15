import pandas as pd
import numpy as np
import calplot
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
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

# Load Excel
df = pd.read_excel("./mrt_disruptions_2025_refined.xlsx")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Hours"] = pd.to_numeric(df["Hours"], errors="coerce").fillna(0)

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

    fig, ax = calplot.calplot(
        values_line,
        cmap=cmap,
        vmin=1,
        vmax=len(lines),
        suptitle="MRT Disruptions by Line",
        colorbar=False
    )

    legend_handles = [
        mpatches.Patch(color=LINE_COLORS[line], label=line)
        for line in lines
    ]

    for a in ax:
        for label in a.get_xticklabels():
            label.set_fontsize(20)

    # for a in ax:
    #     for label in a.texts:
    #         if label.get_text() in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
    #             label.set_fontsize(20)

    ax[0].legend(
        handles=legend_handles,
        title="MRT Line",
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        frameon=False,
        fontsize=18,          # labels
        title_fontsize=20     # title
    )
    
    plt.show()

def part2():
    values_hours = pd.Series(
        df["Hours"].values,
        index=df["Date"]
    )

    fig, ax = calplot.calplot(
        values_hours,
        cmap=strong_cmap,
        suptitle="MRT Disruption Severity (Hours)",
        colorbar=True
    )

    for a in ax:
        for label in a.get_xticklabels():
            label.set_fontsize(20)
    for a in ax:
        for label in a.texts:
            if label.get_text() in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                label.set_fontsize(20)
                
    plt.show()


part1()
#part2()
