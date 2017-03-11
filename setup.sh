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
sudo pip install -t requests

echo "Install bluetooth"
sudo apt-get install -y bluetooth libbluetooth-dev

echo "Install Bluez"
sudo pip install -t pybluez pybluez[ble]

echo "Install Gattlib"
sudo pip install -t gattlib

echo "Download program file"
git clone https://github.com/aqover/StudentLocation-Receiver.git locating

echo "Install crontab"
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/5 * * * * /home/fa/locating/update.py" >> mycron
#install new cron file
crontab mycron
rm mycron