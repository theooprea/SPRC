import time
import json
import pytz
import paho.mqtt.client as mqtt 
from random import choice
from datetime import datetime

MQTT_BROKER = "localhost"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TIMEZONE = "Europe/Bucharest"

if __name__ == "__main__":
    client = mqtt.Client("IOT DEVICE")
    client.connect(MQTT_BROKER) 

    while True:
        battery = choice(list(range(1, 101)))
        humidity = choice(list(range(20, 81)))
        temperature = choice(list(range(150, 280))) / 10
        non_numerical_option = choice(["PRJ", "status", "random_option"])
        non_numerical_value = choice(["SPRC", "OK", "random_value"])

        location = choice(["UPB", "Dorinel"])
        station = choice(["RPi_1", "RPi_2", "RPi_3", "Zeus"])

        payload = {
            "BAT": battery,
            "HUMID": humidity,
            "TMP": temperature,
            non_numerical_option: non_numerical_value,
        }

        include_timestamp = choice([False, True])

        if include_timestamp:
            payload.update({'timestamp': datetime.strftime(datetime.now(pytz.timezone(TIMEZONE)), TIME_FORMAT)})

        publish_location = location + "/" + station
        client.publish(publish_location, json.dumps(payload))

        print("Published ", json.dumps(payload), " into ", publish_location)

        time.sleep(1)
