from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
from get_monitor import getMonitor
import numpy as np
import shutil
import socket
import struct
import sys
import os


UDP_IP = "127.0.0.1"
UDP_INPORT = 8088
UDP_OUTPORT = 8089
UDP_OUTPORT_END = 8090

def run_simulate(fmuFilename, 
                 startTime, 
                 stopTime, 
                 stepSize, 
                 startVals):

    model_description = read_model_description(fmuFilename)

    # collect the value references
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference

    vrInputs = []
    vrInputs  = [vrs['Tamb']]  
    vrOutputs = vrs['Q'] 

    # extract the FMU
    unzipdir = extract(fmuFilename)

    fmu = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.coSimulation.modelIdentifier)

    # initialize
    fmu.instantiate()
    fmu.setupExperiment(startTime=startTime, stopTime=stopTime)
    fmu.enterInitializationMode()
    fmu.setReal(vrInputs, startVals)
    fmu.exitInitializationMode()
    time = startTime
    rows = []

    # simulation loop
    while time < stopTime:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            value = struct.unpack('!d', data)[0]
            fmu.setReal([vrs['T']], [value])
            # print("received message: %s" % str(value))
        except socket.timeout:
            break 
        except KeyboardInterrupt:
            print('interrupted!')
            sys.exit(0)   

        # perform one step
        fmu.doStep(currentCommunicationPoint=time, communicationStepSize=stepSize)
        time += stepSize

        outputs = fmu.getReal([vrOutputs])
        # append the results
        rows.append((time, outputs[0]))

        try:
            data = struct.pack('!d', outputs[0])
            sock.sendto(data, (UDP_IP, UDP_OUTPORT))
        except KeyboardInterrupt:
            print('interrupted!')
            sys.exit(0)    
    fmu.terminate()
    fmu.freeInstance()

    # clean up
    shutil.rmtree(unzipdir, ignore_errors=True)

    # convert the results to a structured NumPy array
    result = np.array(rows, dtype=np.dtype([('time', np.float64), ('Q', np.float64)]))
    print(result)
    plot_result(result)

    return time


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind((UDP_IP, UDP_INPORT))
    sock.settimeout(15.0)

    fmuFilename = os.path.join(os.getcwd(), 'FMUs', 'HeatTransfer.fmu')
    startTime = 0.0
    stopTime = 1000000
    stepSize = 10
    startVals = [getMonitor('T_amb')]
    run_simulate(fmuFilename, 
                 startTime, 
                 stopTime, 
                 stepSize, 
                 startVals)
    try:
        sock.sendto(b"computation completed", (UDP_IP, UDP_OUTPORT_END))
    except KeyboardInterrupt:
        print('interrupted!')
        sys.exit(0)    