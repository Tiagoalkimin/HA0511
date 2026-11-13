"""Modelo de GPU: integrada e dedicadas (intermediária / alta)."""

GPU_PROFILES = {
    "integrada": {
        "nome": "Intel UHD Graphics 730 (integrada, memória compartilhada)",
        "idle_w": 2,
        "max_w": 20,
    },
    "dedicada_intermediaria": {
        "nome": "NVIDIA GeForce GTX 1660 SUPER (6 GB GDDR6)",
        "idle_w": 12,
        "max_w": 160,
    },
    "dedicada_alta": {
        "nome": "NVIDIA GeForce RTX 3080 (10 GB GDDR6X)",
        "idle_w": 18,
        "max_w": 320,
    },
}


class GPU:
    """Representa a GPU do computador simulado."""

    def __init__(self, tier: str):
        if tier not in GPU_PROFILES:
            raise ValueError(f"Tier de GPU inválido: {tier}")
        self.tier = tier
        self.profile = GPU_PROFILES[tier]
        self.nome = self.profile["nome"]

    def power_w(self, util_percent: float) -> float:
        util = max(0.0, min(100.0, util_percent)) / 100.0
        curva = util ** 1.1
        idle = self.profile["idle_w"]
        maxw = self.profile["max_w"]
        return round(idle + (maxw - idle) * curva, 1)

    def max_w(self) -> float:
        return self.profile["max_w"]
