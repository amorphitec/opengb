Installation
============

*Note: Instructions are for Debian-based distros. Official packages will be available when OpenGB enters beta.*

Python 3.4
^^^^^^^^^^

OpenGB requires Python 3.4 or greater. 

_Note: Debian Wheezy only supports Python 3.2. If you are using a Beaglebone Black you should upgrade to Debian Jessie before installing OpenGB._

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

*Note: OpenGB will be available from* `PyPI`_ *when OpenGB enters beta.*

::

    pip install -e git+git://github.com/re-3D/opengb@master#egg=opengb

Create database directory
^^^^^^^^^^^^^^^^^^^^^^^^^

*Note: this will happen automatically when OpenGB is distributed as a package.*

::

    sudo mkdir /var/opengb
    sudo chown <your_user>:<your_group> /var/opengb

Deploy config file
^^^^^^^^^^^^^^^^^^

*Note: this will happen automatically when openGB is distributed as a package.*

::

    sudo mkdir /etc/opengb
    sudo chown <your_user>:<your_group> /etc/opengb
    sudo cp ~/virtualenvs/opengb/src/opengb/opengb/etc/opengb.conf /etc/opengb/

Once deployed, edit this file to set the appropriate parameters for your system.

Add user to dialout
^^^^^^^^^^^^^^^^^^^

Your user must be a member of the group :code:`dialout` for serial port access:

::

    sudo adduser <your_user> dialout

Start
^^^^^

Switch to the virtualenv and start opengb:

::

    source ~/virtualenvs/opengb/bin/activate
    opengb

Navigate to http://localhost:8000 and the OpenGB interface should appear.

.. _PyPI: https://pypi.python.org/ 
