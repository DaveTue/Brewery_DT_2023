from datetime import datetime
import os
import time
import requests
import sys
import json

URL = "SOME URL"
strStartTime = input("Enter batch start time (yyyy-mm-dd hh:mm): ")
startTime = datetime.strptime(strStartTime, '%Y-%m-%d %H:%M')

while(True):
    try: 
        diffTime = datetime.now() - startTime
        # round to nearest minutes
        spanMinutes = round(diffTime.total_seconds() / 60)
        # round to nearest simulation steps
        stepsStart = round(spanMinutes / 10)

        # ============= Request modeling =======================
        params = json.dump({"stepsStart": stepsStart})
        rep = requests.get(url=URL, params=params)
        data = json.load(rep.json())

        # ============= Parsing =======================
        listT = data['listT']
        listTCool = data['listTCool']
        listTime = list(range(1, 31))

        # ============= Display results =======================
        os.system('CLS')
        print("Batch start time: " + startTime.strftime('%Y-%m-%d %H:%M'))
        print("Current time: " + datetime.now().strftime('%Y-%m-%d %H:%M'))
        res = "\n".join("{:<10s} {:<20s} {:<30s}".format(str(t), str(x), str(y)) for t, x, y in zip(listTime, listT, listTCool))
        print("{:<10s} {:<20s} {:<30s}".format("Minutes", "T", "T_Cool"))
        print(res)
        # Wait for next update cycle
        time.sleep(30)
        
    except KeyboardInterrupt:
        print('interrupted!')
        sys.exit(0)   