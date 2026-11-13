import unittest
from models.computer import Computer, COMPUTER_PRESETS
from core.simulator import Track

class HardwareTests(unittest.TestCase):
    def test_clock_respects_each_cpu_and_ignores_gpu_load(self):
        for key in COMPUTER_PRESETS:
            cpu = Computer(key).cpu.profile
            track = Track(Computer(key))
            track.modo = "laboratorio"
            self.assertEqual(track.clock_ghz, cpu['base_ghz'])
            track.tick((0, 0), (100, 100), 0)
            self.assertEqual(track.clock_ghz, cpu['base_ghz'])
            track.tick((100, 100), (0, 0), 0)
            self.assertEqual(track.clock_ghz, cpu['boost_ghz'])
            for _ in range(100):
                track.tick((100, 100), (100, 100), 2)
                self.assertLessEqual(track.clock_ghz, cpu['boost_ghz'])
