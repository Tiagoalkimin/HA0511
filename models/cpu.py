class CPU:
    IDLE_W = 9
    MAX_W = 95

    def power_w(self, util_percent: float) -> float:
        """Potência (W) consumida pela CPU para um dado percentual de uso."""
        util = max(0.0, min(100.0, util_percent)) / 100.0
        # Curva levemente não-linear: cargas altas custam proporcionalmente mais
        # (boost de clock e tensão), representando o comportamento real de CPUs.
        curva = util ** 1.15
        idle = self.IDLE_W
        maxw = self.MAX_W
        return round(idle + (maxw - idle) * curva, 1)
