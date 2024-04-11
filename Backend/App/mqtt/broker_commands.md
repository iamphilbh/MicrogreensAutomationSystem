# Usefull MQTT Broker Commands

#### Start MQTT Broker
With custom config:
```{bash}
sudo mosquitto -c /etc/mosquitto/mosquitto.conf
```


#### Interact (Send/Receive) messages to MQTT broker
```{bash}
mosquitto_pub -h localhost -t "light/switch" -m "off"
```
```{bash}
mosquitto_sub -h localhost -t "light/status"
```

#### Kill any running Mosquitto processes
```{bash}
sudo pkill mosquitto
```