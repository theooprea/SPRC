# MQTT and Microservices - Theodor-Alin Oprea - 341C1
Time to implement: ~30-35h

## Gneral info
The project imlpments an IoT devices monitoring systems, using Eclipse-mosquitte
as the MQTT message broker, InfluxDB to store the measurements data, Grafana to
visualize the devices' data and Python for a custom message adaptor logic.

The workflow is as follows: The IoT devices send messages to the MQTT Broker,
the Python custom adaptor filters out unnecessary data and saves it in an
InfluxDB instance, from which a Grafana instance collects data and renders it in
2 dashboards, `UPB IoT Data` and `Battery Dashboard`. The Grafana instance is
configured to preload the dashboard configurations and datasource (`InfluxDB`)
from a `grafana` folder.

To easily generate data, without having actual IoT devices, there is a
`publisher.py` script in the `mqtt-publisher` folder, easily configurable, which
continuously generates dummy data for the Broker to be consumed.

The solution comes as a `Docker Swarm` stack, which can be set up using:
```
docker swarm init
./run.sh
```
and can be stopped by using:
```
./down.sh
docker system prune -a --volumes
```

## Custom Adaptor
The adaptor extracts env variables regarding the InlfuxDB instance, the MQTT Broker
instance and Logging info. In order to see the logs of the adaptor, simply set the
`DEBUG_DATA_FLOW` variable to `true` in the `.env` file. The adaptor initiates 2
clients, one for the InfluxDB which is then connected to the `influxdb_data_db`
DB, and one for the MQTT Broker, which is subscribed to every topic, by using `#`.

Each message trigges the `on_message` callback, which checks the topic for the
requested format, `<location>/<station>`, extracts the timestamp from the message
and if not provided, uses the local time, parses out the non integer and non float
fields and sends the data to the Database.

The logs are visible using:
```
docker service logs sprc3_mqtt_api
```

## Grafana
The grafana instance is configured to load the datasource (InfluxDB) and dashboards
upon creating. The datasource was configured using a `.yml` file, and the dashboards
were created in the GUI, and exported as JSON under grafana. The files are then
mounted in the instance's `/etc/grafana/provisioning` file, which auto-loads the
configs.

## Final Disclaimers
From time to time, the `./run.sh` command may fail, if that's the case, simply run
```
./down.sh
docker system prune -a --volumes
```
and rerun `./run.sh`
