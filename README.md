<div align="center">

# 🛡️ ROADSAFE

### Smart Road Accident Data Intelligence & Visualization System

**A modern, interactive analytics dashboard for exploring road safety trends across India.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)
![Status](https://img.shields.io/badge/Status-Project%20Demo-22C55E)

**[Features](#-features) · [Dashboard Preview](#-dashboard-preview) · [Getting Started](#-getting-started) · [Data Sources](#-data-sources--limitations)**

</div>

---

## ✨ Overview

**ROADSAFE** transforms historical Indian road accident data into an interactive, visual dashboard. It helps users explore changes over time, compare states and road categories, examine collision patterns, and understand reported road-user fatalities.

The interface features a dark navy theme, gradient highlights, KPI cards, and interactive charts. ROADSAFE is an **exploratory analytics project**, not a live crash-monitoring or accident-prediction service.

## 📸 Dashboard Preview

> Add your own full-page ROADSAFE screenshot to `assets/dashboard.png` to display it here.

<!-- Remove the HTML comment below after adding assets/dashboard.png.
![ROADSAFE Premium Dashboard](assets/dashboard.png)
-->

## 🚀 Features

| Module | What it shows |
|---|---|
| 📊 Executive overview | Summary KPI cards for the selected reporting year |
| 📈 Accident trajectory | National accident and fatality trends |
| 🗓️ Monthly intelligence | Monthly patterns and year-by-month heatmap |
| 🛣️ Road categories | National Highways, State Highways, and Other Roads |
| 🗺️ State comparison | State-wise accident and fatality comparisons (charts) |
| 👥 Road-user analysis | Fatalities by road-user category |
| 💥 Collision analysis | Accident distribution by collision type |
| 🪖 Safety devices | Reported helmet and seat-belt non-use outcomes |
| 🔀 Junction analysis | Accident statistics by junction type for 2019 |
| 🚦 Historical context | Historical vehicle and road safety indicators |
| 💡 Automated findings | Data-driven highlights for selected years |
| 📥 Data explorer | Browse tables and download CSV files |

### Design highlights

- Premium dark navy interface with cyan and violet accents
- Responsive sidebar controls and a gradient hero section
- Interactive Plotly area, bar, donut, treemap, and heatmap charts
- Separate handling of national and state-level datasets

## 🧰 Tech Stack

- **Python** — application language
- **Streamlit** — interactive web interface
- **Pandas** — data processing and filtering
- **Plotly** — interactive data visualizations
- **CSV** — local datasets

## 📁 Project Structure

```text
ROADSAFE/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
│   └── .gitkeep
└── data/
    ├── road_accidents.csv
    ├── state_fatalities.csv
    ├── monthly_accidents.csv
    ├── road_types.csv
    ├── road_user_fatalities.csv
    ├── collision_types.csv
    ├── safety_device_totals.csv
    ├── junction_types_2019.csv
    ├── historical_vehicle_context.csv
    └── DATA_DICTIONARY.csv
```

## ⚙️ Getting Started

### Prerequisites

Install [Python 3.10+](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads).

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ROADSAFE.git
cd ROADSAFE
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## 📚 Data Sources & Limitations

The dashboard uses cleaned historical datasets derived from supplied CSV files and tables in the **Ministry of Road Transport and Highways (MoRTH), _Road Accidents in India 2023_** report.

| Dataset | Coverage |
|---|---|
| State-wise accidents | 2016–2019 |
| State-wise fatalities | 2019–2023 |
| Monthly accident trends | 2019–2023 |
| Road categories | 2021–2023 |
| Road-user fatalities | 2022–2023 |
| Collision types | 2022–2023 |
| Safety-device outcomes | 2023 |
| Junction statistics | 2019 |
| Historical vehicle context | 2012–2023 |

**Interpretation notes:**

- The data is historical, not live.
- National statistics are not filtered by state selections.
- Different datasets cover different years and units; their totals should not be combined indiscriminately.
- State-level accident counts and state-level fatality counts have different time coverage.
- The published 2021 monthly accident values sum to **412,632**, while the reported annual total is **412,432**; the original monthly entries are retained.
- Counts do not represent population-normalized risk or establish the causes of accidents.

See [`data/DATA_DICTIONARY.csv`](data/DATA_DICTIONARY.csv) for column definitions.

## 🧭 Roadmap

- [x] Premium Streamlit dashboard
- [x] Interactive filtering and visualizations
- [x] Multi-dataset analysis
- [x] CSV export
- [ ] Verified geographic India choropleth map
- [ ] Deployment and public demo link
- [ ] Additional data validation and tests

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome. Open an issue or submit a pull request.

## 📄 Acknowledgements

Historical road safety data: **Ministry of Road Transport and Highways (MoRTH), Government of India**. This project is an independent educational visualization and is not an official government service.

---

<div align="center">

**ROADSAFE — Turning road safety data into actionable understanding.**

Made with Python · Streamlit · Plotly

</div>
