import os
import re
import pytz
import time
import json
import logging
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime

# Extract env variables
MQTT_BROKER_HOST = os.environ.get("MQTTBROKER_HOST", "mqtt_broker")
INFLUXDB_DB = os.environ.get("INFLUXDB_DB", "influxdb_data_db")
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxdb")
DEBUG_DATA_FLOW = os.environ.get("DEBUG_DATA_FLOW", False)

# Time format and timezone
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TIMEZONE = "Europe/Bucharest"

# Message callback function
def on_message(client, userdata, message):
    '''
    Function that processes a message that is received by the broker and forwarded to the adaptor
    '''
    # Get the topic of the message and try to match it to a <location>/<station> format
    topic = message.topic
    topic_matches = re.match(r"(?P<location>[^/]*?)/(?P<station>.*)", topic)

    # If the topic is not in the required format, ignore the message
    if not topic_matches:
        logging.info("Wrong format {topic}".format(topic))
        return

    # Extract location and station form the message topic
    location = topic_matches['location']
    station = topic_matches['station']

    # Log the message receival
    if DEBUG_DATA_FLOW == 'true':
        logging.info("Received a message by topic {location}/{station}".format(location=location, station=station))

    # Extract the payload
    payload = json.loads(message.payload)

    # Get the timestamp from the message, and if the message doesn't contain a timestamp, generate from current time
    timestamp = payload.get('timestamp', None)
    if not timestamp:
        timestamp = datetime.strftime(datetime.now(pytz.timezone(TIMEZONE)), TIME_FORMAT)

    # Print the timestamp of the message
    if DEBUG_DATA_FLOW == 'true':
        if payload.get('timestamp', None):
            logging.info("Data timestamp is {timestamp}".format(timestamp=timestamp))
        else:
            logging.info("Data timestamp is NOW")

    # Build the data to be sent to the DB
    db_data = []

    # For each key-value pair in the payload
    for key, value in payload.items():
        # Check the type of the "value", if it's not an integer or a float, and the key isn't timestamp
        # (exception to value type = string), ignore the field
        if not isinstance(value, int) and not isinstance(value, float) and key != "timestamp":
            continue

        # Log the field
        if DEBUG_DATA_FLOW == 'true':
            logging.info("{location}.{station}.{key} {value}".format(location=location, station=station, key=key, value=value))

        # Build the measurement as the <station>.<key>
        measurement = station + "." + key

        # Build the entry object
        entry = {}

        # Add the measurement
        entry.update({'measurement': measurement})

        # Add the tags
        entry.update({
            'tags': {
                'location': location,
                'station': station,
            }
        })

        # Add the field with the current value
        entry.update({'fields': {
            'value': value
        }})

        # Add the timestamp
        entry.update({'time': timestamp})

        # Add the current entry to the list of 'to-add' data
        db_data.append(entry)

    # If at least one field was valid, add the data in the database
    if len(db_data) != 0:
        global influxdb_client
        influxdb_client.write_points(db_data)

if __name__ == "__main__":
    # Create a Influxdb client
    global influxdb_client
    influxdb_client = InfluxDBClient(INFLUXDB_HOST)

    # Connect the Influxdb client to the database
    influxdb_client.switch_database(INFLUXDB_DB)

    # Create a MQTT client
    client = mqtt.Client("SPRC Adaptor")

    # Connect the MQTT client to the broker and subscribe them to every topic
    client.connect(MQTT_BROKER_HOST) 
    client.subscribe("#")
    client.on_message=on_message 

    # Configure the logging module
    logging.basicConfig(filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

    # Log the starting of the adaptor
    if DEBUG_DATA_FLOW == 'true':
        logging.info("Adaptor started the connection to broker and is listening")

    client.loop_forever()

influxdb_client = None
