from .cpu import CPU
from .gpu import GPU


class Computer:
    """Perfil intermediário usado no cenário da demonstração."""

    def __init__(self):
        self.cpu = CPU()
        self.gpu = GPU()
        self.extras_w = 25 + 6 + 3 + 6
        self.thermal_reference_c = 84
        self.thermal_tau_s = 40

    def max_power_w(self):
        return self.cpu.MAX_W + self.gpu.MAX_W + self.extras_w
