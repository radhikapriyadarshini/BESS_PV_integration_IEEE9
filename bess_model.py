class BESS:
    def __init__(self, E_rated, SOC_init=0.5, eta=0.95):
        self.E_rated = E_rated
        self.SOC = SOC_init
        self.eta = eta

    def update_SOC(self, P_batt, dt=1):
        dSOC = (-self.eta * P_batt * dt) / self.E_rated
        self.SOC += dSOC
        self.SOC = max(0.0, min(1.0, self.SOC))
        return self.SOC
