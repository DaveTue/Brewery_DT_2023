from kafka import KafkaConsumer, TopicPartition
from OMSimulator import OMSimulator, Types
from datetime import datetime, timedelta
from git.repo import Repo
import logging
import json

logging.getLogger("kafka").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger()

consumer = KafkaConsumer('inkbird2','tilt2', auto_offset_reset='earliest', consumer_timeout_ms=1000)
inkbirdTP = TopicPartition('inkbird2', 0)
tiltTP = TopicPartition('tilt2', 0)

inkbirdOffsetNow = consumer.end_offsets([inkbirdTP]).get(inkbirdTP) - 1
tiltOffsetNow = consumer.end_offsets([tiltTP]).get(tiltTP) - 1

oms = OMSimulator()
model, status = oms.importFile("s1.ssp")
logger.info("Import SSP: %s", Types.Status(status))
oms.newResources("s1.root:root.ssv")

for message in consumer:
    # messageTime = datetime.fromtimestamp(int(message.timestamp)/1000).replace(microsecond=0) 
    try: 
        if message.topic == 'inkbird2' and message.offset == inkbirdOffsetNow:
            dictInkbird = json.loads(message.value.decode())
            tempInkbird = dictInkbird.get('temp') + 273.15
            oms.setReal('s1.Root.Temperature.T_amb', tempInkbird)
            logger.info("Get T_amb (Temperature): %s", Types.Status(status))
            oms.setReal('s1.Root.HeatTransfer.Tamb', tempInkbird)
            logger.info("Get T_amb (HeatTransfer): %s", Types.Status(status))
        if message.topic == 'tilt2' and message.offset == tiltOffsetNow:
            dictTilt = json.loads(message.value.decode())
            tempTilt = dictTilt.get('temp') + 273.15
            sgTilt = dictTilt.get('gravity')
            oms.setReal('s1.Root.Temperature.T_0', tempTilt)
            logger.info("Get T_0: %s", Types.Status(status))
            oms.setReal('s1.Root.Temperature.sg', sgTilt)
            logger.info("Get SG: %s", Types.Status(status))
    except:
        pass

status = oms.export(model, "s1.ssp")
logger.info("Update SSP: %s", Types.Status(status))

repo = Repo(".")
logger.info("Local repository: %s", repo)
adds = repo.index.add(['s1.ssp'])
logger.info("Add: %s", adds)
commit = repo.index.commit("New fetched data")
logger.info("Commit: %s", commit)
pushinfo = repo.remotes.origin.push()
logger.info("PushInfo: %s", pushinfo)
