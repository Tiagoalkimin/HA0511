class GPU:
    IDLE_W = 12
    MAX_W = 160

    def power_w(self, util_percent: float) -> float:
        util = max(0.0, min(100.0, util_percent)) / 100.0
        curva = util ** 1.1
        idle = self.IDLE_W
        maxw = self.MAX_W
        return round(idle + (maxw - idle) * curva, 1)
