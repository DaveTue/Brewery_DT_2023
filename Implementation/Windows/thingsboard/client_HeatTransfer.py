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

RPC_HEATTRANSFER = "http://localhost:8080/api/v1/SQ2NpIzyii72RkgqCwBt/rpc"

def start_model(Tamb):
    filename = os.path.join(os.getcwd(), 'FMU', 'HeatTransfer.fmu')
    inLogPath = os.path.join(os.getcwd(), 'logs', 'mod2out.csv')
    traj = read_csv(inLogPath)
    traj.dtype.names = 'time', 'T'
    start_values = { 
        'Tamb': (Tamb, None),
    }
    result = simulate_fmu(filename, 
                          input=traj,
                          start_time=0,
                          start_values=start_values,
                          step_size=10,
                          output_interval=10,
                          stop_time=1000000)
    outLogPath = os.path.join(os.getcwd(), 'logs', 'mod3out.csv')
    write_csv(outLogPath, result)

FUNC_MAP = {
    'start_model': start_model,
}

if __name__ == '__main__':
     while True:
        try:
            logger.info("Waiting for trigger...")
            url = RPC_HEATTRANSFER
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
            FUNC_MAP[rpcMethod](rpcParams.get("Tamb"))
            logger.info("Sleep")
            time.sleep(230)