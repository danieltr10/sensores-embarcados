import paho.mqtt.client as mqtt
import serial
import time

MQTT_SERVER = "172.24.1.1"
MQTT_PORT = 1883
MQTT_PATH = "sensor"
MQTT_USER = "username"
MQTT_PASSWORD = "grupo6"

lucasNumber = '+5511987725802'


def callTo(phoneNumber):
    ser = serial.Serial('/dev/ttyS0')  # open serial port
    print(ser.name) # check which port was really used
    time.sleep(0.4)
    ser.write('AT') # Return to online command state from online data state
    time.sleep(1)
    ser.write('ATD') # make a call
    ser.write(phoneNumber) # make a call
    time.sleep(8)
    ser.write('ATH') # Disconnect existing call
    ser.close() # close port

def sendSMS(phoneNumber, text):
    ser = serial.Serial('/dev/ttyS0')  # open serial port
    print(ser.name) # check which port was really used
    time.sleep(0.4)
    ser.write('AT+CMGF=1') # Configuring TEXT mode
    ser.write("AT+CMGS=\"" + phoneNumber + "\"")
    ser.write(text)
    packet = bytearray()
    packet.append(0x26) # send ctrl+z command indicating the text end
    ser.write(packet)
    ser.close() # close port

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # Rerencia de códigos da placa GPRS https://www.makerfabs.com/desfile/files/A6A7A6CA20_AT_Commends.pdf
    print(msg.topic + " " + str(msg.payload))
    callTo(lucasNumber)
    sendSMS(lucasNumber, 'Atenção: houve uma invasão no cofre!')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
