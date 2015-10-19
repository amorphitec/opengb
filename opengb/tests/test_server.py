"""
Opengb server unit tests.
"""

from multiprocessing import Queue
import json

from opengb.tests import OpengbTestCase
from opengb import server

class TestMessageHandler(OpengbTestCase): 

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(to_printer=self.to_printer)

    def test_pass_set_temps_method_to_printer(self):
        """Valid set temperatures result in a 'set_temp' message on the to_printer queue."""
        mh = self.message_handler.set_temp(bed=100, nozzle1=200, nozzle2=200)
        self.assertEqual(json.loads(self.to_printer.get())["method"], "set_temp")

    def test_valid_set_temps_passed_to_printer(self):
        """Valid set temperatures are added as a message on the to_printer queue."""
        mh = self.message_handler.set_temp(bed=100, nozzle1=200, nozzle2=200)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "set_temp",
            "params": {"bed": 100, "nozzle2": 200, "nozzle1": 200}})

    def test_set_bed_temp_defaults_to_none(self):
        """Unspecified bed_temperature is passed to_the printer as None."""
        mh = self.message_handler.set_temp(nozzle1=200, nozzle2=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["bed"], None)
    
    def test_set_nozzle1_temp_defaults_to_none(self):
        """Unspecified nozzle1_temperature is passed to_the printer as None."""
        mh = self.message_handler.set_temp(bed=100, nozzle2=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["nozzle1"], None)

    def test_set_nozzle2_temp_defaults_to_none(self):
        """Unspecified nozzle2_temperature is passed to_the printer as None."""
        mh = self.message_handler.set_temp(bed=100, nozzle1=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["nozzle2"], None)
