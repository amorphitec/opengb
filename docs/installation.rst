Installation
============

OpenGB is a Python application for Linux.

Using apt
^^^^^^^^^

If using Debian or derivates (Ubuntu, Raspbian etc) OpenGB is best installed via a package from the official apt repository.

Add OpenGB Repo
---------------

::

    echo "deb http://dl.bintray.com/amorphic/opengb jessie main" | sudo tee /etc/apt/sources.list.d/opengb.list

Install OpenGB
--------------

::

    sudo apt-get update
    sudo apt-get install opengb

Upgrade OpenGB
--------------

::

    sudo apt-get update
    sudo apt-get upgrade opengb

Post-Install
------------

The OpenGB apt package will offer to perform a number of post-installation steps depending on your platform and requirements:

::

    $ sudo apt-get install opengb

    ...

    Unpacking opengb (0.21.0) ...
    Setting up opengb (0.21.0) ...
    Creating opengb user
    Creating data directories in /var/opengb
    Creating log directory in /var/log/opengb
    Creating default config in /etc/opengb
    Creating service in /etc/init.d/opengb
    To setup the OpenGB graphical interface on this host run 'opengb-interface-setup'

Graphical Interface
-------------------

After installing OpenGB you may run `opengb-interface-setup` to set up the local machine as a graphical frontend to OpenGB. This will present options to:

* Change hostname to ``opengb``.
* Install the **Iceweasel** browser.
* Start the browser on boot.
* Install a Fullscreen browser extension.
* Disable screen blanking
* Disable mouse pointer

These steps are useful for configuring platforms such as the recommended Raspberry Pi + Touchscreen.

Using pip
^^^^^^^^^

OpenGB may be installed from scratch using pip. However this requires additional setup which is not neccessary when installing via apt.

Python 3.4
----------

OpenGB requires Python 3.4 or greater. 

Install Python3.4:

::

    sudo apt-get install python3.4

Virtualenv
----------

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
---------------

::

    pip install opengb

Update package
--------------

To update OpenGB from a previous version:

::

    pip install -U opengb

Create data directories
-----------------------

::

    sudo mkdir /var/opengb
    sudo mkdir /var/opengb/db
    sudo mkdir /var/opengb/gcode
    sudo chown -R <your_user>:<your_group> /var/opengb

Create log directory
--------------------

::

    sudo mkdir /var/log/opengb
    sudo chown <your_user>:<your_group> /var/log/opengb

Deploy config file
------------------

Once deployed edit the config file to set the appropriate parameters for your system.

::

    sudo mkdir /etc/opengb
    sudo chown <your_user>:<your_group> /etc/opengb
    sudo cp ~/virtualenvs/opengb/lib/python3.4/site-packages/opengb/etc/opengb.conf /etc/opengb/

Start
-----

Switch to the virtualenv and start opengb:

::

    source ~/virtualenvs/opengb/bin/activate
    opengb

Navigate to http://localhost:8000 and the OpenGB interface should appear.

.. _PyPI: https://pypi.python.org/ 
