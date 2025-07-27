BESS‑PV Integration on IEEE 9-bus System
Authors: Radhika Priyadarshini et al.
Language: Python 3.x
Goal: Evaluate integration of photovoltaic generation and battery energy storage into the IEEE-9 bus system under different scenarios, including frequency support using droop control.

🔧 Repository Structure
graphql
Copy
Edit
BESS_PV_integration_IEEE9/
├── ieee9_case.py        # Defines the IEEE‑9 bus network
├── pv_model.py          # PV generation behavior and MPPT control
├── bess_model.py        # BESS model and charge/discharge control
├── simulation.py        # Runs time‑series simulation and events
├── plots.py             # Visualization of results
├── utils.py             # Helper functions (logging, interpolation)
├── parameters.py        # Configuration parameters
└── main.py              # Command line entry point
⚙️ Installation & Requirements
bash
Copy
Edit
git clone <repo_url>
cd BESS_PV_integration_IEEE9
pip install -r requirements.txt
Typical dependencies:

numpy, pandas, matplotlib

pandapower or pypower (if used for load flow)

pyyaml or jsonschema (if configurations are structured)

🏃 Usage
To run a base scenario:

bash
Copy
Edit
python main.py --scenario baseline --duration 3600
Other options:

--scenario fault to simulate a line or generator trip

--plot to generate results charts

🧱 Models & Controls
IEEE‑9 Network (ieee9_case.py)
Defines buses, generator inertia, reactances, load distribution, and initial power flow — based on the classic standard IEEE test case.

PV Model (pv_model.py)
Generates PV output time-series, with or without irradiance profiles. Often includes:

Maximum power point tracking (MPPT)

Curtailment logic when generation exceeds capacity

BESS Controller (bess_model.py)
Implements state of charge (SoC) tracking and control strategies:

Droop‑based frequency control (inertia emulation, charging/discharging)

Peak‑shaving or time‑of‑use scheduling

Simulation Engine (simulation.py)
Combines dynamic events:

Load disturbance or fault injection

PV generation variability

Tracks system frequency, voltages, flows, BESS SoC over time

📊 Output & Visualization
plots.py typically produces:

Bus voltage and system frequency vs time

BESS SoC and power dispatch

PV power profile and curtailed power

Line flows and voltage profile across network
