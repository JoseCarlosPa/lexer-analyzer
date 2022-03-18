#!/bin/bash

sudo apt update
sudo apt install software-properties-common -y

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 -y

python3.9 --version
echo "Instalacion de Python 3.9 Exitoso!! "
python3 main.py