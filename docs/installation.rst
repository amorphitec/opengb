Installation
============

Python 3.4
^^^^^^^^^^

OpenGB requires Python 3.4 or greater. 

Install Python3.4:

::

    sudo apt-get install python3.4

Virtualenv
^^^^^^^^^^

Install Virtualenv: 

::

    sudo apt-get install python-virtualenv

Create a new Python 3.4 virtualenv:

::    

    mkdir ~/virtualenvs
    virtualenv -p python3.4 ~/virtualenvs/opengb

Switch to the new virtualenv:

::

    source ~/virtualenvs/opengb/bin/activate

Install package
^^^^^^^^^^^^^^^

To install OpenGB from scratch:

::

    pip install opengb

Update package
^^^^^^^^^^^^^^

To update OpenGB from a previous version:

::

    pip install -U opengb

Create data directories
^^^^^^^^^^^^^^^^^^^^^^^

::

    sudo mkdir /var/opengb
    sudo mkdir /var/opengb/db
    sudo mkdir /var/opengb/gcode
    sudo chown -R <your_user>:<your_group> /var/opengb

Create log directory
^^^^^^^^^^^^^^^^^^^^

::

    sudo mkdir /var/log/opengb
    sudo chown <your_user>:<your_group> /var/log/opengb

Deploy config file
^^^^^^^^^^^^^^^^^^

Once deployed edit the config file to set the appropriate parameters for your system.

::

    sudo mkdir /etc/opengb
    sudo chown <your_user>:<your_group> /etc/opengb
    sudo cp ~/virtualenvs/opengb/lib/python3.4/site-packages/opengb/etc/opengb.conf /etc/opengb/

Start
^^^^^

Switch to the virtualenv and start opengb:

::

    source ~/virtualenvs/opengb/bin/activate
    opengb

Navigate to http://localhost:8000 and the OpenGB interface should appear.

.. _PyPI: https://pypi.python.org/ 
