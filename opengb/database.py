from peewee import *


DB = SqliteDatabase(None)

COUNTERS = [
    'printer_up_mins_session',
    'printer_up_mins',
    'printer_print_mins',
    'bed_up_mins',
    'nozzle_1_up_mins',
    'nozzle_2_up_mins',
    'motor_x1_up_mins',
    'motor_x2_up_mins',
    'motor_y1_up_mins',
    'motor_y2_up_mins',
    'motor_z1_up_mins',
    'motor_z2_up_mins',
]


class BaseModel(Model):
    class Meta:
        database = DB


class PrintJob(BaseModel):
    start = DateTimeField()
    end = DateTimeField()


class GCodeFile(BaseModel):
    name = CharField()
    size = IntegerField()
    print_material = CharField()
    print_quality = CharField()
    print_extruders = CharField()
    print_time_sec = IntegerField()
    print_filament_mm = IntegerField()
    print_material_gm = IntegerField()
    thumbnail_png_base64 = CharField()


class Counter(BaseModel):
    name = CharField()
    count = IntegerField()


def initialize(path):
    """
    Initialize the database.

    :param path: Path to the sqlite database file.
    :type path: :class:`str`
    :raises: :class:`peewee.OperationalError` if database file cannot be
        created.
    """
    # Connect to database
    DB.init(path)
    try:
        DB.connect()
    except OperationalError:
        # TODO: handle this, though it shouldn't happen if we ensure path
        # exists and is writeable upstream.
        raise

    # Create database tables if not already present.
    DB.create_tables([
        PrintJob,
        GCodeFile,
        Counter,
    ], safe=True)

    # Create counters if not already present.
    existing_counters = [c.name for c in Counter.select()]
    for counter in COUNTERS:
        if counter not in existing_counters:
            Counter.create(name=counter, count=0)

    # Reset session counters.
    query = Counter.update(count=0).where(Counter.name.endswith('_session'))
    query.execute()
