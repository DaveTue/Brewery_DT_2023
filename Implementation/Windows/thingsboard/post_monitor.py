from kafka import KafkaConsumer, TopicPartition
import requests
from datetime import datetime, timedelta
from git.repo import Repo
import logging
import json

TELEMETRY_TILT = "http://localhost:8080/api/v1/LvPPBG3KFzPioX0KIIZP/telemetry"
TELEMETRY_INKBIRD = "http://localhost:8080/api/v1/5Ps5f43zjTStzUVcYkiV/telemetry"
HEADER = {'content-type': 'application/json'}

logging.getLogger("kafka").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger()

consumer = KafkaConsumer('inkbird2','tilt2', auto_offset_reset='latest')
# consumer = KafkaConsumer('inkbird2','tilt2', auto_offset_reset='earliest', consumer_timeout_ms=1000)
inkbirdTP = TopicPartition('inkbird2', 0)
tiltTP = TopicPartition('tilt2', 0)

inkbirdOffsetNow = consumer.end_offsets([inkbirdTP]).get(inkbirdTP) - 1
tiltOffsetNow = consumer.end_offsets([tiltTP]).get(tiltTP) - 1


for message in consumer:
    # messageTime = datetime.fromtimestamp(int(message.timestamp)/1000).replace(microsecond=0) 
    try: 
        # if message.topic == 'inkbird2' and message.offset == inkbirdOffsetNow:
        if message.topic == 'inkbird2':
            data = (message.value.decode())
            rep = requests.post(TELEMETRY_INKBIRD, data=data, headers=HEADER)
            logger.info("POST: %s %s", rep, data)
        # if message.topic == 'tilt2' and message.offset == tiltOffsetNow:
        if message.topic == 'tilt2':
            data = (message.value.decode())
            rep = requests.post(TELEMETRY_TILT, data=data, headers=HEADER)
            logger.info("POST: %s %s", rep, data)      
    except:
        pass
