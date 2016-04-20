#!/bin/bash

# Configures a host to act as a graphical interface to a locally-running
# OpenGB daemon.

BROWSER=iceweasel
FS_EXTENSION="mFull"
FS_URL="https://addons.mozilla.org/en-US/firefox/addon/mfull/"
HOSTNAME_CURRENT=$(hostname)
HOSTNAME_NEW=opengb
USER=$(whoami)

read -d '' MESSAGE <<- EOF
	This script will configure a host to act as a graphical interface to a
	locally-running OpenGB daemon.

	This configuration is tested with and designed to run on the Raspberry Pi
	Model 3B with a Raspberry Pi Touch Display, the Raspbian operating system
	and the Iceweasel web browser.

	For more information visit http://opengb.readthedocs.org
EOF

echo "$MESSAGE"
echo

# Change hostname.
read -p "Change hostname from $HOSTNAME_CURRENT to $HOSTNAME_NEW? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo sed -i -e "s/${HOSTNAME_CURRENT}/${HOSTNAME_NEW}/g" /etc/hosts
	sudo sed -i -e "s/${HOSTNAME_CURRENT}/${HOSTNAME_NEW}/g" /etc/hostname
	HOSTNAME_CURRENT=$HOSTNAME_NEW
fi

# Install browser.
read -p "Install $BROWSER? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo apt-get install $BROWSER
fi

# Start browser on boot.
read -p "Start $BROWSER automatically on boot? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	cat <<- EOF >> /home/$USER/.config/lxsession/LXDE-pi/autostart
	@iceweasel http://${HOSTNAME_CURRENT}.local:8000
	EOF
fi

# Install browser fullscreen extension.
read -p "Install $FS_EXTENSION extension for $BROWSER [Y/n] ? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	echo "Follow the directions in $BROWSER to install ${FS_EXTENSION}."
	echo "Close $BROWSER when installation is complete."
	sleep 5
	$BROWSER $FS_URL
fi

# Disable screen blanking.
read -p "Disable screen blanking? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	cat <<- EOF >> /home/$USER/.config/lxsession/LXDE-pi/autostart
	@xset s noblank
	@xset s off
	@xset -dpms
	EOF
fi

# Disable mouse pointer.
read -p "Disable mouse pointer? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo apt-get install unclutter
	echo "unclutter -idle 5" >> /home/$USER/.config/lxsession/LXDE-pi/autostart
fi

read -p "Reboot to apply changes? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo reboot
fi
