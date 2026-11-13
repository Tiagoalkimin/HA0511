import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def button(app, label):
    return next(b for b in app.button if b.label == label)


class InterfaceTests(unittest.TestCase):
    def test_clicks_persistence_tariff_reset_and_legacy(self):
        app = AppTest.from_file(APP).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Computador desta simulação' in m.value for m in app.markdown))
        self.assertTrue(any('EnergySim' in m.value for m in app.markdown))
        self.assertTrue(button(app, '2. Simular otimização').disabled)
        initial = app.session_state['quick_demo'].snapshot()['power']['total_w']
        button(app, '1. Mostrar consumo extra').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Algo está gastando' in m.value for m in app.markdown))
        self.assertNotEqual(initial, app.session_state['quick_demo'].snapshot()['power']['total_w'])
        button(app, '2. Simular otimização').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(initial, app.session_state['quick_demo'].snapshot()['power']['total_w'])
        self.assertTrue(any('19,44' in m.value for m in app.markdown))
        app.run()
        self.assertTrue(any('19,44' in m.value for m in app.markdown))
        app.number_input(key='demo_tariff').set_value(1.8).run()
        self.assertTrue(any('38,88' in m.value for m in app.markdown))
        button(app, 'Recomeçar').click().run()
        self.assertEqual(app.session_state['quick_demo'].stage, 'normal')
        self.assertIsNone(app.session_state['quick_demo'].comparison())
        button(app, 'Explorar o modo completo').click().run()
        self.assertEqual(app.session_state['screen'], 'intro_problema')
        self.assertEqual(len(app.exception), 0)
        button(app, 'Voltar à demonstração rápida').click().run()
        self.assertEqual(app.session_state['screen'], 'demo')
        self.assertEqual(len(app.exception), 0)
