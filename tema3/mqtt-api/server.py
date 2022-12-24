import os
import re
import pytz
import time
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime

MQTT_BROKER_HOST = os.environ.get("MQTTBROKER_HOST", "mqtt_broker")
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxdb")
INFLUXDB_DB = os.environ.get("INFLUXDB_DB", "influxdb_data_db")

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TIMEZONE = "Europe/Bucharest"

def on_message(client, userdata, message):
    topic = message.topic
    topic_matches = re.match(r"(?P<location>[^/]*?)/(?P<station>.*)", topic)

    if not topic_matches:
        print("Wrong format", topic)
        return

    location = topic_matches['location']
    station = topic_matches['station']

    payload = json.loads(message.payload)

    timestamp = payload.get('timestamp', None)
    if not timestamp:
        timestamp = datetime.strftime(datetime.now(pytz.timezone(TIMEZONE)), TIME_FORMAT)

    db_data = []
    for key, value in payload.items():
        if not isinstance(value, int) and not isinstance(value, float) and key != "timestamp":
            continue

        measurement = location + "." + station + "." + key

        entry = {}
        entry.update({'measurement': measurement})
        entry.update({
            'tags': {
                'location': location,
                'station': station,
            }
        })
        entry.update({'fields': {
            'value': value
        }})
        entry.update({'time': timestamp})

        db_data.append(entry)

    if len(db_data) != 0:
        global influxdb_client
        influxdb_client.write_points(db_data)
        

if __name__ == "__main__":
    global influxdb_client
    influxdb_client = InfluxDBClient(INFLUXDB_HOST)
    influxdb_client.switch_database(INFLUXDB_DB)

    client = mqtt.Client("SPRC Adaptor")

    client.connect(MQTT_BROKER_HOST) 
    client.subscribe("#")
    client.on_message=on_message 

    print("Adaptor started the connection to broker and is listening")

    client.loop_forever()

influxdb_client = None
