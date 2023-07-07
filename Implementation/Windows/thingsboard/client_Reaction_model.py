from fmpy import *
import requests
import time
import sys
import os
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger()

RPC_REACTIONMOD = "http://localhost:8080/api/v1/OWFGsQjAOuLXV8EUO6Wh/rpc"
RPC_TEMPERATUREMOD = "http://localhost:8080/api/v1/ksmoiGnHrccBKDLdxGv2/rpc"
HEADER = {'content-type': 'application/json'}

def start_sim():
    filename = os.path.join(os.getcwd(), 'FMU', 'Reaction_model.fmu')
    start_values = { 
        'batch_volume': (20, None),
        'grams_yeast': (11.5, None),
        'sg_0': (1.054, None),
        'Temperature': (299.15, None)
    }
    result = simulate_fmu(filename, 
                          start_values=start_values,
                          start_time=0,
                          step_size=10,
                          output_interval=10,
                          stop_time=1000000)
    outLogPath = os.path.join(os.getcwd(), 'logs', 'mod1out.csv')
    write_csv(outLogPath, result, columns=["rate_c_sugar"])
    # plot_result(result)
    
FUNC_MAP = {
    'start_sim': start_sim,
}

if __name__ == '__main__':
    while True:
        try:
            url = RPC_REACTIONMOD
            logger.info("Waiting for trigger...")
            rep = requests.get(url, verify=False, timeout=300)
            if rep.status_code == 503:
                logger.info("%s", rep)
                continue
            rpcMethod = rep.json().get("method")
            rpcParams = rep.json().get("params")
            logger.info("%s id:%s %s", rep, rep.json().get("id"), rpcMethod)
            
        except KeyboardInterrupt:
            logger.info('interrupted!')
            sys.exit(0)    
        except:
            logger.info("Timeout")
        else:	
            FUNC_MAP[rpcMethod]()
            data = json.dumps({"method": "start_model", "params": rpcParams})
            url = RPC_TEMPERATUREMOD
            rep = requests.post(url, data=data, headers=HEADER)
            logger.info("%s", rep.json())
            logger.info("Sleep")
            time.sleep(230)
