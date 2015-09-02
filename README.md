# Open Gigabot Controller.

_Not yet ready for production use._

## Installation:

_Instructions are for Debian-based distros._

###Python 3.4

Install Python3.4:

    sudo apt-get install python3.4

###Virtualenv

Install Virtualenv: 

    sudo apt-get install python-virtualenv

Create a new python3.4 virtualenv:
    
    mkdir ~/virtualenvs
    virtualenv -p python3.4 ~/virtualenvs/opengb

Switch to the new virtualenv:

    source ~/virtualenvs/opengb/bin/activate

###Install from github

    

###Create database directory

_Note: this will happen automatically when openGB is distributed as a package._

    sudo mkdir /var/opengb
    sudo chown <your_user>:<your_group> /var/opengb

###Deploy config file

_Note: this will happen automatically when openGB is distributed as a package._

    sudo mkdir /etc/opengb
    sudo chown <your_user>:<your_group> /etc/opengb
    sudo cp ~/virtualenvs/opengb/lib/python3.4/site-packages/opengb/etc/opengb.conf /etc/opengb

Once deployed, edit this file to set the appropriate parameters for your system.

###Add user to dialout group

Required for serial port access:

    sudo adduser <your_user> dialout

##Running

Switch to the virtualenv and start opengb:

    source ~/virtualenvs/opengb/bin/activate
    opengb

Navigate to [http://localhost:8080](http://localhost:8080) and the OpenGB interface should appear.
