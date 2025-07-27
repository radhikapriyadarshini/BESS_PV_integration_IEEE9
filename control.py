def bess_control(SOC, SOC_min=0.2, SOC_max=0.9):
    if SOC < SOC_min:
        return 1.0  # charge
    elif SOC > SOC_max:
        return -1.0  # discharge
    else:
        return 0.0  # idle
