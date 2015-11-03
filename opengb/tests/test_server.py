"""
Opengb server unit tests.
"""

from multiprocessing import Queue
import json

from peewee import *
from playhouse.test_utils import test_database

from opengb.tests import OpengbTestCase
from opengb import server
from opengb.database import Counter


class TestSetTemp(OpengbTestCase): 

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

class TestMoveHead(OpengbTestCase): 

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(to_printer=self.to_printer)

    def test_pass_move_head_method_to_printer(self):
        """Valid x,y,z values result in a 'move_head' message on the to_printer queue."""
        mh = self.message_handler.move_head(x=0.02, y=-4, z=2)
        self.assertEqual(json.loads(self.to_printer.get())["method"], "move_head")

    def test_valid_xyz_passed_to_printer(self):
        """Valid x,y,z values are added as a message on the to_printer queue."""
        mh = self.message_handler.move_head(x=0.02, y=-4, z=2)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "move_head",
            "params": {"x": 0.02, "y": -4, "z": 2}})

    def test_move_head_x_defaults_to_zero(self):
        """Unspecified x is passed to_the printer as 0."""
        mh = self.message_handler.move_head(y=-4, z=2)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["x"], 0)
    
class TestHomeHead(OpengbTestCase): 

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(to_printer=self.to_printer)

    def test_pass_home_head_method_to_printer(self):
        """Valid x,y,z values result in a 'home_head' message on the to_printer queue."""
        mh = self.message_handler.home_head(x=True, y=True, z=False)
        self.assertEqual(json.loads(self.to_printer.get())["method"], "home_head")

    def test_valid_xyz_passed_to_printer(self):
        """Valid x,y,z values are added as a message on the to_printer queue."""
        mh = self.message_handler.home_head(x=True, y=True, z=False)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "home_head",
            "params": {"x": True, "y": True, "z": False}})

    def test_home_head_x_defaults_to_True(self):
        """Unspecified x is passed to_the printer as True."""
        mh = self.message_handler.home_head(y=True, z=False)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["x"], True)
    
class TestGetCounters(OpengbTestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.test_counters = {
            'printer_up_mins_session':  15,
            'printer_up_mins':          777,
            'printer_print_mins':       101,
            'bed_up_mins':              777,
            'nozzle_1_up_mins':         777,
            'nozzle_2_up_mins':         777,
            'motor_x1_up_mins':         777,
            'motor_x2_up_mins':         777,
            'motor_y1_up_mins':         777,
            'motor_y2_up_mins':         93,
            'motor_z1_up_mins':         777,
            'motor_z2_up_mins':         777,
            'filament_up_mins':         777,
        }
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(to_printer=self.to_printer)

    def test_get_counters_returns_correct_values(self):
        """Correct counter values are returned from the database."""
        with test_database(self.db, [Counter], create_tables=True):
            for k, v in self.test_counters.items():
                Counter.create(name=k, count=v)
            mh = self.message_handler.get_counters()
            self.assertDictEqual(mh['counters'], self.test_counters)
