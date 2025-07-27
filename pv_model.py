def pv_output(irradiance, temp, Voc=37, Isc=8.21, FF=0.75, G_ref=1000, T_ref=25, alpha=0.005):
    P = Voc * Isc * FF * (irradiance / G_ref) * (1 - alpha * (temp - T_ref))
    return P

if __name__ == "__main__":
    print("PV Output Test:", pv_output(1000, 25))
