#!/bin/bash
# Fomenko A V (c)

# sudo pip3 install sh
# sudo pip3 install pyqt5

sudo cp -v ms55dd /usr/bin
sudo chmod -v 755 /usr/bin/ms55dd

sudo cp -v ms55dd.desktop /usr/share/applications
sudo chmod -v 755 /usr/share/applications/ms55dd.desktop

sudo cp -v -R MS55DD /opt
sudo chmod -v -R 777 /opt/MS55DD 

cd /opt/MS55DD 

python3 -m venv venv_ms55dd

source venv_ms55dd/bin/activate

pip install sh pyqt5

deactivate

sudo chmod -v -R 755 /opt/MS55DD

echo 'finish'

# /opt/MS55DD/venv_ms55dd/bin/python
