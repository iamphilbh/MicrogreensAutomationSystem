import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("light")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.payload.upper() == "ON":
        print("Turning LED on...")
        GPIO.output(8, GPIO.LOW)
    elif msg.payload.upper() == "OFF":    
        print("Turning LED off...")
        GPIO.output(8, GPIO.HIGH)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()


# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# from time import sleep # Import the sleep function from the time module
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
# while True: # Run forever
#  print("ON")
#  GPIO.output(8, GPIO.HIGH) # Turn on
#  sleep(5) # Sleep for 1 second
#  print("OFF")
#  GPIO.output(8, GPIO.LOW) # Turn off
#  sleep(1) # Sleep for 1 second