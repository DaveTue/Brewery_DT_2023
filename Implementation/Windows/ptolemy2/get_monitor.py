from kafka import KafkaConsumer, TopicPartition
import json

def getMonitor(var):
    consumer = KafkaConsumer('inkbird2','tilt2', auto_offset_reset='earliest', consumer_timeout_ms=1000)
    inkbirdTP = TopicPartition('inkbird2', 0)
    tiltTP = TopicPartition('tilt2', 0)

    inkbirdOffsetNow = consumer.end_offsets([inkbirdTP]).get(inkbirdTP) - 1
    tiltOffsetNow = consumer.end_offsets([tiltTP]).get(tiltTP) - 1

    if var == 'T_amb':
        for message in consumer:
            try: 
                if message.topic == 'inkbird2' and message.offset == inkbirdOffsetNow:
                    dictInkbird = json.loads(message.value.decode())
                    return dictInkbird.get('temp') + 273.15
            except:
                print('No data')      
    elif var == 'T_0':
        for message in consumer:
            try: 
                if message.topic == 'tilt2' and message.offset == tiltOffsetNow:
                    dictTilt = json.loads(message.value.decode())
                    return dictTilt.get('temp') + 273.15
            except:
                print('No data')
    elif var == 'sg':
        for message in consumer:
            try: 
                if message.topic == 'tilt2' and message.offset == tiltOffsetNow:
                    dictTilt = json.loads(message.value.decode())
                    return dictTilt.get('gravity')   
            except:
                print('No data')