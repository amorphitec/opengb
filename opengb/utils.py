"""
OpenGB utils.

Various utilities and helper functions used by OpenGB.
"""
import os

from tornado.options import options
import psutil

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

    :param gcode: A string contianing gcode commands separated by newlines.
    :rtype gcode: :class:`str`
    :param remove_comments: Remove lines representing comments.
    :rtype remove_comments: :class:`bool`
    :returns: Individual gcode commands.
    :rtype: :class:`iter` of :class:`str`
    """
    gcode_list = [g.strip() for g in gcode.split('\n') if g != '']
    if remove_comments:
        return [g.split(';', 1)[0] for g in gcode_list
                if not g.startswith(';')]
    return gcode_list

def get_filesystem_utilization():
    """
    Get current filesystem utilization.

    :returns: Filesystem names mapped to utilization metrics.
    :rtype: :class:`dict of :class:`dict`
    :raises: `IOError` on all errors.
    """
    all_fs_utilization = {}
    try:
        for each in psutil.disk_partitions():
            utilization = psutil.disk_usage(each.mountpoint)
            all_fs_utilization[each.mountpoint] = {
                'total_bytes':      utilization.total,
                'utilized_bytes':   utilization.used,
                'utilized_percent': utilization.percent,
                'free_bytes':       utilization.free,
            }
    except psutil.Error as err:
        raise IOError(err.args[0])    
    return all_fs_utilization
