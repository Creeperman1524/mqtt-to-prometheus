import configparser
import sys

from flask import Flask
from flask_mqtt import Mqtt

# Setup config file
config_path = "./settings.conf"
if len(sys.argv) == 2:
    config_path = sys.argv[1]

config = configparser.ConfigParser()
if len(config.read(config_path)) == 0:
    raise RuntimeError(
        "Failed to find configuration file at {0}, is the application properly installed?".format(
            config_path
        )
    )

app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = config.get("mqtt", "broker")
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = config.get("mqtt", "user")
app.config["MQTT_PASSWORD"] = config.get("mqtt", "password")
app.config["MQTT_REFRESH_TIME"] = config.get("mqtt", "refresh_time")
mqtt = Mqtt(app)

data: dict[str, str] = {}

mapping = {
    "ON": 1,
    "OFF": 0,
}


@app.route("/metrics")
def metrics():
    payload = ""
    for topic in data:
        name = topic.split("/")[-1]
        value = data[topic]

        # Mapping string to num
        if value in mapping:
            value = mapping[value]
        payload += f"{name} {value}\n"

    return f"{payload}", 200, {"Content-Type": "text/plain; charset=utf-8"}


@mqtt.on_connect()
def connect(client, userdata, flags, rc):
    mqtt.subscribe(config.get("mqtt", "path"))


@mqtt.on_message()
def message(client, userdata, message):
    data[message.topic] = message.payload.decode("utf-8")


if __name__ == "__main__":
    print("Starting prometheus to MQTT bridge")
    app.run(host="0.0.0.0")
