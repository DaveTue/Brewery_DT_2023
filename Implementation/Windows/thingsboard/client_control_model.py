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

RPC_CONTROLMOD = "http://localhost:8080/api/v1/OLBXZDixCU556nWh7ly3/rpc"
TEL_CONTROLMOD = "http://localhost:8080/api/v1/OLBXZDixCU556nWh7ly3/telemetry"
HEADER = {'content-type': 'application/json'}

def start_model(T_senorK):
    filename = os.path.join(os.getcwd(), 'FMU', 'control_model.fmu')
    start_values = { 
        'T_sensor': (T_senorK - 273.15, None),
        'T_set': (22, None),
    }
    result = simulate_fmu(filename, 
                          start_time=0,
                          start_values=start_values,
                          step_size=10,
                          output_interval=10,
                          stop_time=50)
    outLogPath = os.path.join(os.getcwd(), 'logs', 'mod4out.csv')
    write_csv(outLogPath, result)
    return int(result[4][1])

FUNC_MAP = {
    'start_model': start_model,
}

if __name__ == '__main__':
     while True:
        try:
            logger.info("Waiting for trigger...")
            url = RPC_CONTROLMOD
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
            command = FUNC_MAP[rpcMethod](rpcParams.get("T"))
            data = json.dumps({"command": command})
            url = TEL_CONTROLMOD
            rep = requests.post(url, data=data, headers=HEADER)
            logger.info("POST: %s %s", rep, data)
            logger.info("Sleep")
            time.sleep(230)