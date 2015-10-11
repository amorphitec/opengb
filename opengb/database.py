from peewee import *
from tornado.options import options

import opengb.config


DB = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = DB


class PrintJob(BaseModel):
    start = DateTimeField()
    end = DateTimeField()


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
    ], safe=True)
