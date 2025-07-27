from pv_model import pv_output
from bess_model import BESS
from control import ems_control
from ieee9_mod import modified_ieee9
import matplotlib.pyplot as plt
import pandas as pd

print(">>> Script started")

# Initialize hourly profiles
irradiance_profile = [800 + 200 * i / 24 for i in range(24)]  # Dummy increasing profile
temp_profile = [25 + 5 * i / 24 for i in range(24)]
load_profile = [180 + 20 * ((i % 24) / 24) for i in range(24)]  # Rises slightly over the day



# Init models
bess = BESS(E_rated=100)  # 100 kWh battery
soc_log = []
power_log = []
voltage_log = []
line_loading_log = []

try:
    print("=== Hourly Load Profile ===")
    for hour, load in enumerate(load_profile):
        print(f"Hour {hour:2d}: {load:.2f} kW")
    for hour, (G, T) in enumerate(zip(irradiance_profile, temp_profile)):
        # Calculate PV output
        P_pv = pv_output(G, T)

        # Get BESS control action
        P_load = load_profile[hour]
        P_bess = ems_control(P_pv, P_load, bess.SOC)


        # Update battery SOC
        SOC = bess.update_SOC(P_bess)

        # Net output to grid
        total_P = P_pv + P_bess  # in kW

        # Logging
        soc_log.append(SOC)
        power_log.append(total_P)

        # Inject into IEEE 9-bus system and run power flow
        net = modified_ieee9(P_dg=total_P / 1000,  # Convert to MW
                             bus_id=5,
                             run_powerflow=True,
                             verbose=False)

        voltage = net.res_bus.vm_pu.at[5]
        voltage_log.append(voltage)

        loading = net.res_line.loading_percent.max()
        line_loading_log.append(loading)

        print(f"[Hour {hour}] PV: {P_pv:.2f} kW, BESS: {P_bess:.2f} kW, SOC: {SOC:.2f}, Bus5 V: {voltage:.3f} pu, Max Line Loading: {loading:.1f}%")

except Exception as e:
    print(f"Simulation error: {e}")

# === Plotting ===
try:
    hours = list(range(24))

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(hours, soc_log, label='SOC', color='blue')
    plt.ylabel('State of Charge')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(hours, power_log, label='Total Power Output (kW)', color='orange')
    plt.ylabel('Power Output')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(hours, voltage_log, label='Bus 5 Voltage (pu)', color='green')
    plt.ylabel('Voltage at Bus 5 (pu)')
    plt.xlabel('Hour')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
    
except Exception as e:
    print(f"Plotting error: {e}")

print(">>> Script finished")
