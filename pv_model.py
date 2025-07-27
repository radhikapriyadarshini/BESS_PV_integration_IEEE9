import numpy as np

def pv_output(irradiance, temp, Voc_ref=37, Isc_ref=8.21, FF=0.75,
              G_ref=1000, T_ref=25, beta_Voc=-0.003, alpha_Isc=0.0005):
    """
    Estimate PV power output under given irradiance and temperature.

    Returns:
    - P (float): Estimated PV output power (kW)
    """
    irradiance = np.array(irradiance, dtype=float)
    temp = np.array(temp, dtype=float)

    Voc = Voc_ref * (1 + beta_Voc * (temp - T_ref))
    Isc = Isc_ref * (irradiance / G_ref) * (1 + alpha_Isc * (temp - T_ref))
    P = Voc * Isc * FF

    return P / 1000  # kW

if __name__ == "__main__":
    print("PV Output @ STC:", pv_output(1000, 25))
    print("PV Output @ Low Irradiance:", pv_output(200, 25))
    print("PV Output @ High Temp:", pv_output(1000, 45))
