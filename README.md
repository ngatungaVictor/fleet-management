# GPS Fleet Monitoring — EDA

A Python exploratory data analysis project on simulated GPS fleet tracking data set in **Dar es Salaam, Tanzania**.

Built as a portfolio mini-project by **Victor Thadei Ngatunga** (B.Sc. Mathematics & Statistics, University of Dar es Salaam).

---

## Files

| File | Description |
|---|---|
| `fleet_data.csv` | Simulated dataset — 1,000 GPS records across 5 vehicles |
| `fleet_analysis.py` | Main analysis script (Python) |
| `fleet_analysis.png` | Output visualisation (6 charts) |

---

## Dataset Columns

| Column | Description |
|---|---|
| `timestamp` | Date and time of GPS ping |
| `vehicle_id` | Unique vehicle identifier (TJL-001 … TJL-005) |
| `driver` | Driver name |
| `vehicle_type` | Delivery Van / Truck / Pickup |
| `latitude` | GPS latitude (Dar es Salaam region) |
| `longitude` | GPS longitude |
| `speed_kmh` | Speed in km/h (0 = stopped) |
| `fuel_level_pct` | Fuel level as percentage |
| `engine_status` | ON / OFF |
| `speeding_flag` | True if speed > 80 km/h |

---

## Analysis Covers

- Speed distribution per vehicle
- Speeding events per driver (threshold: 80 km/h)
- Fuel level trends over time
- Engine status breakdown
- GPS route traces on a coordinate map
- Average speed by vehicle type

---

## How to Run

```bash
pip install pandas numpy matplotlib seaborn
python fleet_analysis.py
```

Output: summary statistics printed to console + `fleet_analysis.png` saved locally.

---

## Tools
`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn`
