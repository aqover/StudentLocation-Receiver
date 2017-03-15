#!/bin/bash

clear

echo "Update system"
sudo apt-get update

echo "###############################"
echo "#      Prepare to Install     #"
echo "###############################"

echo "Install Git"
sudo apt-get install -y git

echo "Install python module"
sudo apt-get install -y python-pip python-dev ipython

echo "Install library-dev"
sudo apt-get install -y libbluetooth3-dev libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev libglib2.0

echo "Install requests"
sudo pip install requests

echo "Install bluetooth"
sudo apt-get install -y bluetooth libbluetooth-dev

echo "Install Bluez"
sudo pip install pybluez pybluez[ble]

echo "Install Gattlib"
sudo pip install gattlib

echo "Download program file"
cd ~
git clone https://github.com/aqover/StudentLocation-Receiver.git locating

cd locating
chmod +x locating.sh
sudo mv locating.sh /etc/init.d/locating
update-rc.d -f locating add