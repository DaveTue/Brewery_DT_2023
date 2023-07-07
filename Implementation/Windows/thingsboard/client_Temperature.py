from fmpy import *
import requests
import time
import sys
import json
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger()

RPC_TEMPERATUREMOD = "http://localhost:8080/api/v1/ksmoiGnHrccBKDLdxGv2/rpc"
RPC_HEATTRANSFER = "http://localhost:8080/api/v1/SQ2NpIzyii72RkgqCwBt/rpc"
HEADER = {'content-type': 'application/json'}

def start_model(sg, Tamb, T0):
    filename = os.path.join(os.getcwd(), 'FMU', 'Temperature.fmu')
    inLogPath = os.path.join(os.getcwd(), 'logs', 'mod1out.csv')
    traj = read_csv(inLogPath)
    traj.dtype.names = 'time', 'cg_rate'
    start_values = { 
        'sg': (sg, None),
        'T_amb': (Tamb, None),
        'T_0' : (T0, None)
    }
    result = simulate_fmu(filename, 
                          input=traj,
                          start_time=0,
                          start_values=start_values,
                          step_size=10,
                          output_interval=10,
                          stop_time=1000000)
    
    outLogPath = os.path.join(os.getcwd(), 'logs', 'mod2out.csv')
    write_csv(outLogPath, result)

FUNC_MAP = {
    'start_model': start_model,
}

if __name__ == '__main__':
     while True:
        try:
            logger.info("Waiting for trigger...")
            url = RPC_TEMPERATUREMOD
            rep = requests.get(url, verify=False, timeout=300)
            rpcMethod = rep.json().get("method")
            rpcParams = rep.json().get("params")
            if rep.status_code == 503:
                logger.info("%s", rep)
                continue
            logger.info("%s id:%s %s", rep, rep.json().get("id"), rpcMethod)
            
        except KeyboardInterrupt:
            logger.info('interrupted!')
            sys.exit(0)    
        except:
            logger.info("Timeout")
        else:
            FUNC_MAP[rpcMethod](rpcParams.get("sg"), rpcParams.get("Tamb"), rpcParams.get("T"))
            data = json.dumps({"method": "start_model", "params": rpcParams})
            url = RPC_HEATTRANSFER
            rep = requests.post(url, data=data, headers=HEADER)
            logger.info("%s", rep.json())
            logger.info("Sleep")
            time.sleep(230)