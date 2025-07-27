from pv_model import pv_output
from bess_model import BESS
from control import bess_control
from ieee9_mod import modified_ieee9
import matplotlib.pyplot as plt

print(">>> Script started")

# Initialize profiles
irradiance_profile = [800 + 200 * i / 24 for i in range(24)]  # dummy increasing profile
temp_profile = [25 + 5 * i / 24 for i in range(24)]

# Init models
bess = BESS(E_rated=100)  # 100 kWh battery
soc_log = []
power_log = []

try:
    for hour, (G, T) in enumerate(zip(irradiance_profile, temp_profile)):
        P_pv = pv_output(G, T)
        ctrl = bess_control(bess.SOC)
        P_bess = -10 * ctrl  # Assume charging/discharging at 10kW
        SOC = bess.update_SOC(P_bess)
        total_P = P_pv + P_bess

        soc_log.append(SOC)
        power_log.append(total_P)

        print(f"[Hour {hour}] PV: {P_pv:.2f} kW, BESS: {P_bess:.2f} kW, SOC: {SOC:.2f}")

except Exception as e:
    print(f"Error in loop: {e}")

# Integrate into IEEE 9-bus
try:
    net = modified_ieee9(P_dg=power_log[-1])
    print(f">>> Integrated BESS+PV with IEEE 9-Bus: Injecting {power_log[-1]:.2f} kW at Bus 5")
except Exception as e:
    print(f"Integration error: {e}")

# Plot
try:
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(soc_log, label='SOC')
    plt.ylabel('State of Charge')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(power_log, label='Power (kW)', color='orange')
    plt.ylabel('Power Output')
    plt.xlabel('Hour')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"Plotting error: {e}")

print(">>> Script finished")
