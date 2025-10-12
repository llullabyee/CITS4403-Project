## CITS4403 Project

---
### Description
This project aims to model the impact that random node failures and targeted node attacks have on an internet backbone topology, utilising the Barabasi-Albert and Holme-Kim models to simulate this.

---

### Members
| UWA ID   | Name          | Github User   |
|----------|---------------|---------------|
| 23101312 | Mos Hassanein | llullabyee    |
| 23132836 | Ann  Roy      | developing-ar |

---

### Directory structure

```
.
├── data
├── figures
│   ├── models
│   └── visuals
├── notebooks
├── results
├── src
│   └── __pycache__
└── utils
    └── __pycache__
```

### Dataset
[Internet Topology Zoo](https://github.com/sk2/topologyzoo/)


---

### Setup
1. Clone this repository:
```bash
git clone https://github.com/llullabyee/CITS4403-Project.git
cd CITS4403-Project
```

2. Create a Python 3 virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the requirements in `requirements.txt`:
```bash
pip3 install -r requirements.txt
```

---

### Simulation Instructions
Run the following command:
```bash
python3 -m src.model_simulation.py
```

This will create graphs, found in the `figures/models` directory, as well as CSVs containing the data of the simulation, found in the `results` directory.

---

### Data Visualisation Instructions

Run the following command:

```bash
python3 -m src.data_visualisation.py
```

This will create graphs, found in the `figures/visuals` directory.