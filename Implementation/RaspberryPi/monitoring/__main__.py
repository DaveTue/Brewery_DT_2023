import os
import sys
import requests
import json
import time
import subprocess
import configparser
import argparse
from bluepy.btle import Scanner, DefaultDelegate
from .sensors import tilt
from .sensors import inkbird

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
comm_config = configparser.ConfigParser()
comm_config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
MAC_INKBIRD = comm_config['MAC']['Inkbird']
URL_INKBIRD = comm_config['URL']['Inkbird']
MAC_TILT = comm_config['MAC']['Tilt']
URL_TILT = comm_config['URL']['Tilt']

parser = argparse.ArgumentParser()
parser.add_argument("-t","--time", type= int, default=60,
                    help="Data receiving period in second")
args = vars(parser.parse_args())
period = args['time']
scanner = Scanner().withDelegate(ScanDelegate())
while True:
    try:
        devices = scanner.scan(timeout=10)
        for dev in devices:
            if (dev.addr.upper() == MAC_INKBIRD):
                inkbirdValues = inkbird.decode(dev)
            if (dev.addr.upper() == MAC_TILT):
                tiltValues = tilt.decode(dev)
    except:
        print('retry scan')
        prc = subprocess.run(['sudo','hciconfig','hci0','reset'])
        time.sleep(2)
        scanner = Scanner().withDelegate(ScanDelegate())
        continue
        
    else:
        r1 = requests.post(URL_INKBIRD, data=json.dumps(inkbirdValues), headers={'Content-Type': 'application/json'})
        r2 = requests.post(URL_TILT, data=json.dumps(tiltValues), headers={'Content-Type': 'application/json'})
        
    time.sleep(period - 10)

