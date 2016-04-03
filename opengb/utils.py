"""
OpenGB utils.

Various utilities and helper functions used by OpenGB.
"""
import os

from tornado.options import options

import opengb.database as OGD


def load_gcode_file(id):
    """
    Load gcode file with given `id`

    :param id: ID of the gcode file to load.
    :type id: :class:`int`
    :returns: Gcode loaded from file.
    :rtype: :class:`str`
    :raises: `IOError` if file cannot be loaded.
    """
    destination = os.path.join(options.gcode_dir, str(id))
    if not os.path.isfile(destination):
        raise IOError('No gcode file found at {0}'.format(destination))
    with open(destination, "r") as gcode_file_in:
        try:
            gcode = gcode_file_in.read()
        except IOError:
            raise
    return gcode


def delete_gcode_file(id):
    """
    Delete gcode file with given `id`.

    :param id: ID of the gcode file to delete.
    :type id: :class:`int`
    :raises: `IOError` if file cannot be loaded.
    """
    destination = os.path.join(options.gcode_dir, str(id))
    try:
        os.remove(destination)
    except (OSError, FileNotFoundError):
        raise IOError('Unable to delete gcode file at '
                      '{0}'.format(destination)) from None
    try:
        gcode_instance = OGD.GCodeFile.get(OGD.GCodeFile.id == id)
        gcode_instance.delete_instance()
    except OGD.GCodeFile.DoesNotExist:
        raise IOError('No gcode entry in database with id '
                      '{0}'.format(id)) from None


def prepare_gcode(gcode, remove_comments=True):
    """
    Prepare a :class:`str` containing gcode commands for execution by
    converting it to a :class:`iter` of :class:`str` representing individual
    commands.

    Optionally remove comments.

    :param remove_comments: Remove lines representing comments.
    :type remove_comments: :class:`bool`
    """
    gcode_list = [g.strip() for g in gcode.split('\n') if g != '']
    if remove_comments:
        return [g.split(';', 1)[0] for g in gcode_list
                if not g.startswith(';')]
    return gcode_list
