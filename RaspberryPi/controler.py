import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

def on_connect(client:mqtt.Client, userdata, flags, rc:int) -> None:
    print("Connected with result code "+str(rc))
    client.subscribe("light/switch")

def on_message(client:mqtt.Client, userdata, msg:mqtt.MQTTMessage) -> None:
    print("Topic: "+msg.topic+", payload: "+str(msg.payload))

    payload = msg.payload.decode('utf-8')  # Decode the payload

    if payload.upper() == "ON":
        print("Turning LED on...")
        GPIO.output(8, GPIO.HIGH)
        client.publish("light/status", "ON")
    elif payload.upper() == "OFF":    
        print("Turning LED off...")
        GPIO.output(8, GPIO.LOW)
        client.publish("light/status", "OFF")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()