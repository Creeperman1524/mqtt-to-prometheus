# mqtt-to-prometheus

This script allows you to control the brightness and power state of a Rasberry Pi's Screen through
This script publishes data from [MQTT](https://mqtt.org/) to [Prometheus](https://prometheus.io/), an open source time-series database

- Utilizes the [`flask-mqtt`](https://github.com/stlehmann/Flask-MQTT) python package as an extention to [`Flask`](https://github.com/pallets/flask)

> [!WARNING]
> This is a very basic script that can only display a very limited amount of information from MQTT. This is mostly used for a personal project of mine. Further tinkering is recommended!

## Features

- Serves messages recieved from your MQTT broker to a webpage, which prometheus can scrape (as defined from the `path` attribute in the `settings.conf`)
  - This is served to Flask's default port of `:5000`
- Maps "ON" and "OFF" states to 1 and 0, respectively

<p align="center">
  <img src="https://github.com/user-attachments/assets/7cf1c839-42d3-4bbb-9bc9-eb1b1a560208" style="height:400px"/>
</p>

> [!NOTE]
> This is being displayed using [Grafana](https://www.grafana.com)

## Configuration

Using the given `settings.conf.example` file, create a `settings.conf` file in the root of the project directory

- Fill out its information according to the comments
- More information regarding the `path` field can be found [here](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)

Or as an example:

```ini
path = stat/#
```

- This will publish all messages recieved starting with `stat/`

## Building/Running

Run the provided docker build script `./build.sh` to build the docker image

Here are examples of running the container through docker:

### Docker CLI

```bash
docker run -d \
    -v /PATH/TO/REPO/settings.conf:/app/settings.conf \
    mqtt-prometheus
```

### Docker Compose

```yaml
mqtt-prometheus:
  image: mqtt-prometheus
  volumes:
    - /PATH/TO/REPO/settings.conf:/app/settings.conf
```
