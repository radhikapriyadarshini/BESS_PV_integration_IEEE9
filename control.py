def ems_control(P_pv, P_load, SOC, SOC_min=0.2, SOC_max=0.9, max_power=10):
    """
    Enhanced EMS control: only allow charge/discharge within SOC limits.
    """
    if P_pv > P_load and SOC < SOC_max:
        return -max_power  # Charging
    elif P_pv < P_load and SOC > SOC_min:
        return max_power   # Discharging
    else:
        return 0.0  # Idle
