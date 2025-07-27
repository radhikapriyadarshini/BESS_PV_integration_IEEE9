def ems_control(P_pv, P_load, SOC, SOC_min=0.2, SOC_max=0.9, max_power=10.0, margin=0.05):
    """
    EMS control strategy: adjusts BESS power to follow net load while respecting SOC bounds.

    Parameters:
    - P_pv: PV power (kW)
    - P_load: Load demand (kW)
    - SOC: Current state of charge (0 to 1)
    - SOC_min / SOC_max: SOC limits
    - max_power: Max charge/discharge power (kW)
    - margin: SOC buffer zone (for soft limits)

    Returns:
    - P_batt: Desired BESS power (kW)
    """
    net_power = P_pv - P_load  # Surplus if > 0

    if net_power > 0 and SOC < (SOC_max - margin):
        # Charge proportionally to surplus
        return -min(net_power, max_power)

    elif net_power < 0 and SOC > (SOC_min + margin):
        # Discharge proportionally to deficit
        return min(-net_power, max_power)

    return 0.0  # No action needed
