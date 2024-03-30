# Usefull commands

#### Connect to Raspberry Pi through SSH protocol
```{bash}
ssh pi@192.168.0.68
```

#### Copy file to Raspberry Pi through SSH protocol
```{bash}
scp controler.py pi@192.168.0.68:~/Documents/MicrogreensAutomationSystem/controler.py
```

#### Interact (Send/Receive) messages to MQTT broker
```{bash}
mosquitto_pub -h localhost -t "light/switch" -m "off"
```
```{bash}
mosquitto_sub -h localhost -t "light/status"
```