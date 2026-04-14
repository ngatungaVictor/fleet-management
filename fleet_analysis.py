"""
GPS Fleet Monitoring — Exploratory Data Analysis
Author : Victor Thadei Ngatunga | 2023-04-10475
Dataset: Simulated fleet data, Dar es Salaam, Tanzania
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Styling ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#F8F9FA",
    "axes.grid":        True,
    "grid.color":       "#E0E0E0",
    "grid.linewidth":   0.6,
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})
COLORS = ["#1A3C6E", "#2E86AB", "#A23B72", "#F18F01", "#3BB273"]
PALETTE = dict(zip(["TJL-001","TJL-002","TJL-003","TJL-004","TJL-005"], COLORS))

# ── 1. Load data ─────────────────────────────────────────────────────────────
df = pd.read_csv("fleet_data.csv", parse_dates=["timestamp"])
print("=" * 55)
print("  GPS FLEET MONITORING — ANALYSIS REPORT")
print("=" * 55)
print(f"\nRecords loaded : {len(df):,}")
print(f"Vehicles       : {df['vehicle_id'].nunique()}")
print(f"Date range     : {df['timestamp'].min().date()} → {df['timestamp'].max().date()}")
print(f"Columns        : {', '.join(df.columns)}\n")

# ── 2. Summary statistics ────────────────────────────────────────────────────
print("── Summary Statistics ──────────────────────────────")
summary = df.groupby("vehicle_id").agg(
    Driver        = ("driver",       "first"),
    Type          = ("vehicle_type", "first"),
    Avg_Speed     = ("speed_kmh",    lambda x: round(x[x > 0].mean(), 1)),
    Max_Speed     = ("speed_kmh",    "max"),
    Speeding_Events = ("speeding_flag", "sum"),
    Avg_Fuel      = ("fuel_level_pct", lambda x: round(x.mean(), 1)),
    Min_Fuel      = ("fuel_level_pct", "min"),
).reset_index()
print(summary.to_string(index=False))

# ── 3. Figures ───────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12))
fig.suptitle(
    "GPS Fleet Monitoring Dashboard — Dar es Salaam",
    fontsize=16, fontweight="bold", color="#1A3C6E", y=0.98
)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── Plot 1: Speed distribution per vehicle ────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
moving = df[df["speed_kmh"] > 0]
for vid, color in PALETTE.items():
    data = moving[moving["vehicle_id"] == vid]["speed_kmh"]
    ax1.hist(data, bins=25, alpha=0.6, color=color, label=vid, edgecolor="white", linewidth=0.4)
ax1.axvline(80, color="red", linestyle="--", linewidth=1.2, label="Speed limit (80 km/h)")
ax1.set_title("Speed Distribution (moving records only)", fontweight="bold")
ax1.set_xlabel("Speed (km/h)")
ax1.set_ylabel("Frequency")
ax1.legend(fontsize=8, ncol=3)

# ── Plot 2: Speeding events per driver ────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
spd = df[df["speeding_flag"]].groupby("driver").size().sort_values(ascending=True)
bars = ax2.barh(spd.index, spd.values, color=COLORS[:len(spd)], edgecolor="white")
ax2.bar_label(bars, padding=3, fontsize=9)
ax2.set_title("Speeding Events\nper Driver", fontweight="bold")
ax2.set_xlabel("Count")
ax2.set_yticklabels([d.split()[0] for d in spd.index], fontsize=9)

# ── Plot 3: Fuel level over time ──────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, :2])
for vid, color in PALETTE.items():
    vdf = df[df["vehicle_id"] == vid].sort_values("timestamp")
    ax3.plot(vdf["timestamp"], vdf["fuel_level_pct"], color=color, linewidth=1.2, label=vid, alpha=0.85)
ax3.axhline(25, color="red", linestyle="--", linewidth=1, label="Low fuel (25%)")
ax3.set_title("Fuel Level Over Time", fontweight="bold")
ax3.set_xlabel("Timestamp")
ax3.set_ylabel("Fuel Level (%)")
ax3.legend(fontsize=8, ncol=3)
ax3.tick_params(axis="x", rotation=20, labelsize=8)

# ── Plot 4: Engine status pie ─────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
status_counts = df["engine_status"].value_counts()
ax4.pie(
    status_counts, labels=status_counts.index,
    colors=["#3BB273", "#E8E8E8"],
    autopct="%1.1f%%", startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    textprops={"fontsize": 10}
)
ax4.set_title("Engine Status\nDistribution", fontweight="bold")

# ── Plot 5: GPS scatter map ───────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :2])
for vid, color in PALETTE.items():
    vdf = df[df["vehicle_id"] == vid]
    ax5.scatter(vdf["longitude"], vdf["latitude"],
                c=color, s=4, alpha=0.4, label=vid)
ax5.set_title("Vehicle GPS Traces — Dar es Salaam", fontweight="bold")
ax5.set_xlabel("Longitude")
ax5.set_ylabel("Latitude")
ax5.legend(fontsize=8, markerscale=3, ncol=2)

# ── Plot 6: Avg speed by vehicle type ─────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 2])
type_speed = moving.groupby("vehicle_type")["speed_kmh"].mean().sort_values()
bars2 = ax6.barh(type_speed.index, type_speed.values,
                 color=["#1A3C6E", "#2E86AB", "#A23B72"], edgecolor="white")
ax6.bar_label(bars2, fmt="%.1f km/h", padding=3, fontsize=9)
ax6.set_title("Avg Speed by\nVehicle Type", fontweight="bold")
ax6.set_xlabel("Avg Speed (km/h)")

plt.savefig("fleet_analysis.png", dpi=150, bbox_inches="tight")
print("\nPlot saved → fleet_analysis.png")

# ── 4. Alerts summary ────────────────────────────────────────────────────────
print("\n── Alerts Summary ──────────────────────────────────")
total_speeding = df["speeding_flag"].sum()
low_fuel_events = (df["fuel_level_pct"] < 25).sum()
print(f"Speeding events (> 80 km/h) : {total_speeding}")
print(f"Low fuel records  (< 25%)   : {low_fuel_events}")
print(f"Vehicles with low fuel      : {df[df['fuel_level_pct']<25]['vehicle_id'].nunique()}")

worst = df[df["speeding_flag"]].groupby("driver")["speed_kmh"].max().idxmax()
print(f"Highest speed recorded by   : {worst} ({df[df['speeding_flag']].groupby('driver')['speed_kmh'].max().max()} km/h)")
print("\nAnalysis complete.")
