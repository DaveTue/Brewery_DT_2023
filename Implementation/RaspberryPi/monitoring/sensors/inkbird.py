# Inkbird IBS-TH1
from datetime import datetime
from struct import unpack

def decode(dev):
    temp = unpack('<H', dev.rawData[14:16])[0] / 100 # temperature in degree C
    humi = unpack('<H', dev.rawData[16:18])[0] / 100 # specific gravity
    # probe = unpack('<b', dev.rawData[18:19])[0] # probe type: 0->internal, 1->external
    print('-------------------------------------------------')
    print(datetime.now().replace(microsecond=0))
    print('temp: ', temp)
    print('humi: ', humi)
    print('-------------------------------------------------')
    data = {'temp':temp,
            'humi':humi}         
    return data