class BESS:
    def __init__(self, E_rated, SOC_init=0.5, eta_chg=0.95, eta_dis=0.95, SOC_min=0.1, SOC_max=1.0):
        self.E_rated = E_rated  # Rated energy in kWh
        self.SOC = SOC_init     # Initial state of charge
        self.eta_chg = eta_chg  # Charging efficiency
        self.eta_dis = eta_dis  # Discharging efficiency
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max

    def update_SOC(self, P_batt, dt=1):
        """
        Updates SOC based on charging/discharging power.
        P_batt > 0 → Discharging
        P_batt < 0 → Charging
        """
        if P_batt < 0:  # Charging
            dSOC = (-P_batt * self.eta_chg * dt) / self.E_rated
        else:  # Discharging
            dSOC = (-P_batt / self.eta_dis * dt) / self.E_rated

        new_SOC = self.SOC + dSOC

        # Clamp SOC within limits
        if new_SOC > self.SOC_max:
            self.SOC = self.SOC_max
        elif new_SOC < self.SOC_min:
            self.SOC = self.SOC_min
        else:
            self.SOC = new_SOC

        return self.SOC
