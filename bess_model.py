class BESS:
    def __init__(self, E_rated, SOC_init=0.5, eta_chg=0.95, eta_dis=0.95, SOC_min=0.1, SOC_max=1.0):
        self.E_rated = E_rated  # Rated energy capacity in kWh
        self.SOC = SOC_init      # Initial state of charge (0 to 1)
        self.eta_chg = eta_chg  # Charging efficiency (fraction)
        self.eta_dis = eta_dis  # Discharging efficiency (fraction)
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max

    def update_SOC(self, P_batt, dt=1):
        """
        Update SOC based on requested battery power (P_batt in kW).
        Positive P_batt = discharging, Negative P_batt = charging.
        Returns:
          - new SOC value (0-1)
          - actual battery power used (may be limited to respect SOC constraints)
        """
        if P_batt < 0:  # Charging
            dSOC = (-P_batt * self.eta_chg * dt) / self.E_rated
        else:  # Discharging
            dSOC = (-P_batt / self.eta_dis * dt) / self.E_rated

        new_SOC = self.SOC + dSOC

        if new_SOC > self.SOC_max:
            # Limit charging power so SOC doesn't exceed max
            dSOC_allowed = self.SOC_max - self.SOC
            P_batt_actual = - (dSOC_allowed * self.E_rated) / (self.eta_chg * dt)
            self.SOC = self.SOC_max
        elif new_SOC < self.SOC_min:
            # Limit discharging power so SOC doesn't go below min
            dSOC_allowed = self.SOC_min - self.SOC
            P_batt_actual = - (dSOC_allowed * self.E_rated) * self.eta_dis / dt
            self.SOC = self.SOC_min
        else:
            P_batt_actual = P_batt
            self.SOC = new_SOC

        return self.SOC, P_batt_actual
