# TILT™ HYDROMETER
from datetime import datetime
from struct import unpack

def decode(dev):
    # print(dev.rawData.hex())
    # print(dev.getScanData()[1])
    temp = (unpack('>H', dev.rawData[25:27])[0]) # temperature in degree F
    gravity = (unpack('>H', dev.rawData[27:29])[0]) # specific gravity x1000
    gravity = gravity / 1000
    tempC = round((temp-32) * 5.0/9.0, 2) # convert F to C
    print('-------------------------------------------------')
    print(datetime.now().replace(microsecond=0))
    print('temp: ', tempC)
    print('gravity: ', gravity)
    print('-------------------------------------------------')
    data = {'temp':tempC,
            'gravity':gravity}
    return data
