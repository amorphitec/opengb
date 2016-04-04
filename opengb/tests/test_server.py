"""
Opengb server unit tests.

TODO:
    
    * Add print-related API method tests
    * Add retract/unretract tests
    * Add extrude override tests
    * Add speed override tests
    * Add fan speed tests
    * Add filament swap tests
"""

import os
from multiprocessing import Queue
import json
import tempfile
import shutil
from mock import patch

from peewee import SqliteDatabase
from playhouse.test_utils import test_database

from opengb.tests import OpengbTestCase
from opengb import server
from opengb.database import Counter, GCodeFile
from opengb.printer import State


GCODE = """
    M107
    M190 S115 ; set bed temperature
    M104 S205 ; set temperature
    G28 ; home all axes
    G1 Z5 F5000 ; lift nozzle

    M109 S205 ; wait for temperature to be reached
    G21 ; set units to millimeters
    G90 ; use absolute coordinates
    M82 ; use absolute distances for extrusion
    G92 E0
    G1 Z0.500 F7800.000
    G1 E-2.00000 F2400.00000
    G92 E0
    G1 X75.666 Y76.670 F7800.000
    G1 E2.00000 F2400.00000
    G1 X77.428 Y75.130 E2.14774 F1800.000
    G1 X79.603 Y74.269 E2.29548
    G1 X81.016 Y74.123 E2.38516
    G1 X118.984 Y74.123 E4.78272
    G1 X121.290 Y74.520 E4.93046
"""


class TestSetTemp(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_set_temps_method_to_printer(self):
        """Valid temps result in 'set_temp' message on the to_printer queue."""
        self.message_handler.set_temp(bed=100, nozzle1=200, nozzle2=200)
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "set_temp")

    def test_valid_set_temps_passed_to_printer(self):
        """Valid temps are added as a message on the to_printer queue."""
        self.message_handler.set_temp(bed=100, nozzle1=200, nozzle2=200)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "set_temp",
            "params": {"bed": 100, "nozzle2": 200, "nozzle1": 200}})

    def test_set_bed_temp_defaults_to_none(self):
        """Unspecified bed_temperature is passed to_the printer as None."""
        self.message_handler.set_temp(nozzle1=200, nozzle2=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["bed"], None)

    def test_set_nozzle1_temp_defaults_to_none(self):
        """Unspecified nozzle1_temperature is passed to_the printer as None."""
        self.message_handler.set_temp(bed=100, nozzle2=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["nozzle1"], None)

    def test_set_nozzle2_temp_defaults_to_none(self):
        """Unspecified nozzle2_temperature is passed to_the printer as None."""
        self.message_handler.set_temp(bed=100, nozzle1=200)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["nozzle2"], None)


class TestMoveHeadRelative(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_move_head_relative_method_to_printer(self):
        """Valid x,y,z vals result in 'move_head_relative' msg on to_printer
        queue."""
        self.message_handler.move_head_relative(x=0.02, y=-4, z=2)
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "move_head_relative")

    def test_valid_xyz_passed_to_printer(self):
        """Valid x,y,z vals are added as msg on to_printer queue."""
        self.message_handler.move_head_relative(x=0.02, y=-4, z=2)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "move_head_relative",
            "params": {"x": 0.02, "y": -4, "z": 2}})

    def test_move_head_relative_x_defaults_to_zero(self):
        """Unspecified x is passed to_the printer as 0."""
        self.message_handler.move_head_relative(y=-4, z=2)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["x"], 0)

    def test_move_head_relative_y_defaults_to_zero(self):
        """Unspecified y is passed to_the printer as 0."""
        self.message_handler.move_head_relative(x=0.02, z=2)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["y"], 0)

    def test_move_head_relative_z_defaults_to_zero(self):
        """Unspecified z is passed to_the printer as 0."""
        self.message_handler.move_head_relative(x=0.02, y=-4)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["z"], 0)


class TestMoveHeadAbsolute(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_move_head_absolute_method_to_printer(self):
        """Valid x,y,z vals result in 'move_head_absolute' msg on to_printer
        queue."""
        self.message_handler.move_head_absolute(x=105, y=80, z=20)
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "move_head_absolute")

    def test_valid_xyz_passed_to_printer(self):
        """Valid x,y,z vals are added as msg on to_printer queue."""
        self.message_handler.move_head_absolute(x=105, y=80, z=20)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "move_head_absolute",
            "params": {"x": 105, "y": 80, "z": 20}})

    def test_move_head_absolute_x_defaults_to_zero(self):
        """Unspecified x is passed to_the printer as 0."""
        self.message_handler.move_head_absolute(y=80, z=20)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["x"], 0)

    def test_move_head_absolute_y_defaults_to_zero(self):
        """Unspecified y is passed to_the printer as 0."""
        self.message_handler.move_head_absolute(x=105, z=20)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["y"], 0)

    def test_move_head_absolute_z_defaults_to_zero(self):
        """Unspecified z is passed to_the printer as 0."""
        self.message_handler.move_head_absolute(x=105, y=80)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["z"], 0)


class TestHomeHead(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_home_head_method_to_printer(self):
        """Valid x,y,z vals result in 'home_head' msg on to_printer queue."""
        self.message_handler.home_head(x=True, y=True, z=False)
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "home_head")

    def test_valid_xyz_passed_to_printer(self):
        """Valid x,y,z vals are added as a msg on to_printer queue."""
        self.message_handler.home_head(x=True, y=True, z=False)
        self.assertDictEqual(json.loads(self.to_printer.get()), {
            "method": "home_head",
            "params": {"x": True, "y": True, "z": False}})

    def test_home_head_x_defaults_to_True(self):
        """Unspecified x is passed to_the printer as True."""
        self.message_handler.home_head(y=True, z=False)
        self.assertEqual(
            json.loads(self.to_printer.get())["params"]["x"], True)


class TestEnableSteppers(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_enable_steppers_method_to_printer(self):
        """Enable steppers adds 'enable_steppers' msg to to_printer queue."""
        self.message_handler.enable_steppers()
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "enable_steppers")


class TestDisableSteppers(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_disable_steppers_method_to_printer(self):
        """Disable steppers adds 'disable_steppers' msg to to_printer queue."""
        self.message_handler.disable_steppers()
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "disable_steppers")


class TestEmergencyStop(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_pass_emergency_stop_method_to_printer(self):
        """Emergency stop adds 'emergency_stop' msg to to_printer queue."""
        self.message_handler.emergency_stop()
        self.assertEqual(json.loads(self.to_printer.get())["method"],
                         "emergency_stop")


class TestPutGCodeFile(OpengbTestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)
        self.gcode = GCODE

    def test_gcode_file_in_fs(self):
        """Uploaded gcode file is saved correctly to the filesystem."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            gcode_dir = tempfile.mkdtemp()
            with patch.object(server.options.mockable(), 'gcode_dir',
                              gcode_dir):
                r = self.message_handler.put_gcode_file(self.gcode,
                                                           'test_name')
            with open(os.path.join(gcode_dir, str(r['id'])), 'r') as g:
                self.assertEqual(self.gcode, g.read())
        shutil.rmtree(gcode_dir)

    def test_gcode_file_size_in_db(self):
        """Uploaded gcode file size is correct in the database."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            gcode_dir = tempfile.mkdtemp()
            with patch.object(server.options.mockable(), 'gcode_dir',
                              gcode_dir):
                r = self.message_handler.put_gcode_file(self.gcode,
                                                           'test_name')
        self.assertEqual(r['size'], len(self.gcode))

    def test_gcode_file_name_in_db(self):
        """Uploaded gcode file name is correct in the database."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            gcode_dir = tempfile.mkdtemp()
            with patch.object(server.options.mockable(), 'gcode_dir',
                              gcode_dir):
                r = self.message_handler.put_gcode_file(self.gcode,
                                                           'test_name')
        self.assertEqual(r['name'], 'test_name')

    def test_gcode_file_metadata_in_db(self):
        """Uploaded gcode file metadata is correct in the database."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            gcode_dir = tempfile.mkdtemp()
            with patch.object(server.options.mockable(), 'gcode_dir',
                              gcode_dir):
                r = self.message_handler.put_gcode_file(self.gcode,
                    'test_name', print_material='PLA', print_quality='High',
                    print_extruders='Both', print_time_sec=56743,
                    print_filament_mm=9876, print_material_gm=40,
                    thumbnail_png_base64='mock base64 data')
        self.assertEqual(r['print_material'], 'PLA')
        self.assertEqual(r['print_quality'], 'High')
        self.assertEqual(r['print_extruders'], 'Both')
        self.assertEqual(r['print_time_sec'], 56743)
        self.assertEqual(r['print_filament_mm'], 9876)
        self.assertEqual(r['print_material_gm'], 40)
        self.assertEqual(r['thumbnail_png_base64'], 'mock base64 data')

class TestGetGCodeFile(OpengbTestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)
        self.gcode = GCODE

    def test_gcode_file_returned(self):
        """Gcode file with given id is returned."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            g = GCodeFile.create(name='test_file', size='777',
                                 print_material='PLA', print_quality='High',
                                 print_extruders='Both', print_time_sec=56743,
                                 print_filament_mm=9876, print_material_gm=40,
                                 thumbnail_png_base64='mock base64 data')
            r = self.message_handler.get_gcode_file(g.id)
            self.assertEqual(r['name'], g.name)

    def test_gcode_file_content_returned(self):
        """Content of gcode file with given id is returned."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            g = GCodeFile.create(name='test_file', size='777',
                                 print_material='PLA', print_quality='High',
                                 print_extruders='Both', print_time_sec=56743,
                                 print_filament_mm=9876, print_material_gm=40,
                                 thumbnail_png_base64='mock base64 data')
            gcode_dir = tempfile.mkdtemp()
            with open(os.path.join(gcode_dir, str(g.id)), 'wb') as p:
                p.write(self.gcode.encode())
            with patch.object(server.options.mockable(), 'gcode_dir',
                              gcode_dir):
                r = self.message_handler.get_gcode_file(g.id, content=True)
            self.assertEqual(r['content'], self.gcode)
        shutil.rmtree(gcode_dir)


class TestGetGCodeFiles(OpengbTestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_all_gcode_files_returned(self):
        """All gcode files are returned."""
        with test_database(self.db, [GCodeFile], create_tables=True):
            GCodeFile.create(name='test_file_1', size=777,
                             print_material='PLA', print_quality='High',
                             print_extruders='Both', print_time_sec=56743,
                             print_filament_mm=9876, print_material_gm=40,
                             thumbnail_png_base64='xyz123')
            GCodeFile.create(name='test_file_2', size=888,
                             print_material='PLA', print_quality='Low',
                             print_extruders='Left', print_time_sec=12523,
                             print_filament_mm=3376, print_material_gm=22,
                             thumbnail_png_base64='abc456')
            GCodeFile.create(name='test_file_3', size=999,
                             print_material='ABS', print_quality='Medium',
                             print_extruders='Right', print_time_sec=87893,
                             print_filament_mm=10239, print_material_gm=76,
                             thumbnail_png_base64='qrs789')
            r = self.message_handler.get_gcode_files()
        self.assertListEqual(r['gcode_files'], [
            {
                'name':                 'test_file_1',
                'size':                 777,
                'id':                   1,
                'print_material':       'PLA',
                'print_quality':        'High',
                'print_extruders':      'Both',
                'print_time_sec':       56743,
                'print_filament_mm':    9876,
                'print_material_gm':    40,
                'thumbnail_png_base64': 'xyz123',
            },
            {
                'name': 'test_file_2',
                'size': 888,
                'id':   2,
                'print_material':       'PLA',
                'print_quality':        'Low',
                'print_extruders':      'Left',
                'print_time_sec':       12523,
                'print_filament_mm':    3376,
                'print_material_gm':    22,
                'thumbnail_png_base64': 'abc456',
            },
            {
                'name': 'test_file_3',
                'size': 999,
                'id':   3,
                'print_material':       'ABS',
                'print_quality':        'Medium',
                'print_extruders':      'Right',
                'print_time_sec':       87893,
                'print_filament_mm':    10239,
                'print_material_gm':    76,
                'thumbnail_png_base64': 'qrs789',
            },
        ])


class TestDeleteGCodeFile(OpengbTestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)
        self.gcode = GCODE

    def test_gcode_file_deleted_from_fs(self):
        # TODO: implement this
        pass

    def test_gcode_file_deleted_from_db(self):
        # TODO: implement this
        pass


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
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)

    def test_get_counters_returns_correct_values(self):
        """Correct counter values are returned from the database."""
        with test_database(self.db, [Counter], create_tables=True):
            for k, v in self.test_counters.items():
                Counter.create(name=k, count=v)
            mh = self.message_handler.get_counters()
            self.assertDictEqual(mh['counters'], self.test_counters)


class TestGetStatus(OpengbTestCase):

    def setUp(self):
        self.to_printer = Queue()
        self.message_handler = server.MessageHandler(
            to_printer=self.to_printer)
        self.test_status = {
            'state':    State.READY,
            'temp':     {
                'bed':      99,
                'nozzle1':  230,
                'nozzle2':  229,
            },
            'position': {
                'x':        11.9,
                'y':        56.0,
                'z':        46.0,
            },
            'progress': {
                'current':  2386,
                'total':    9945,
            },
        }

    @patch('opengb.server.PRINTER')
    def test_get_status_returns_correct_values(self, m_printer_status):
        """Correct status values are returned."""
        m_printer_status = self.test_status
        mh = self.message_handler.get_status
