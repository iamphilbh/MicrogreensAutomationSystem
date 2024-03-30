# Usefull MQTT Broker Commands

#### Interact (Send/Receive) messages to MQTT broker
```{bash}
mosquitto_pub -h localhost -t "light/switch" -m "off"
```
```{bash}
mosquitto_sub -h localhost -t "light/status"
```