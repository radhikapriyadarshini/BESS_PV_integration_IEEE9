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
load_profile = [180 + 100 * ((i - 12)**2) / 144 for i in range(24)]  # Parabolic load profile

# Initialize BESS model
bess = BESS(E_rated=100)  # 100 kWh battery

# Prepare logs
soc_log = []
power_log = []
voltage_log = []
line_loading_log = []

try:
    current_hour = pd.Timestamp.now().hour

    for hour, (G, T, load) in enumerate(zip(irradiance_profile, temp_profile, load_profile)):
        P_pv = pv_output(G, T) * 1000  # MW to kW

        P_bess_desired = ems_control(P_pv, load, bess.SOC)
        SOC, P_bess_actual = bess.update_SOC(P_bess_desired)

        total_P = P_pv + P_bess_actual

        soc_log.append(SOC)
        power_log.append(total_P)

        net = modified_ieee9(P_dg=total_P / 1000, bus_id=5, run_powerflow=True, verbose=False)

        voltage = net.res_bus.vm_pu.at[5]
        voltage_log.append(voltage)

        loading = net.res_line.loading_percent.max()
        line_loading_log.append(loading)

        highlight = "<<< CURRENT HOUR" if hour == current_hour else ""
        print(f"[Hour {hour:02d}] PV: {P_pv:.2f} kW, BESS Desired: {P_bess_desired:.2f} kW, "
              f"BESS Actual: {P_bess_actual:.2f} kW, SOC: {SOC:.2f}, "
              f"Bus5 V: {voltage:.3f} pu, Max Line Loading: {loading:.1f}% {highlight}")

except Exception as e:
    print(f"Simulation error: {e}")

# === Plotting ===
try:
    # Safe check in case simulation stopped early
    min_len = min(len(soc_log), len(power_log), len(voltage_log))
    hours = list(range(min_len))

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(hours, soc_log[:min_len], label='SOC', color='blue')
    plt.ylabel('State of Charge')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(hours, power_log[:min_len], label='Total Power Output (kW)', color='orange')
    plt.ylabel('Power Output (kW)')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(hours, voltage_log[:min_len], label='Bus 5 Voltage (pu)', color='green')
    plt.ylabel('Voltage (pu)')
    plt.xlabel('Hour')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Plotting error: {e}")

print(">>> Script finished")
