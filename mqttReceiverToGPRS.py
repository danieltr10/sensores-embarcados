import paho.mqtt.client as mqtt
import serial
import time

MQTT_SERVER = "172.24.1.1"
MQTT_PORT = 1883
MQTT_PATH = "sensor"
MQTT_USER = "username"
MQTT_PASSWORD = "grupo6"

mauricioSMS = '+5511987725802'
mauricioCall = '011987725802'

isSystemOn = False

shouldSensSMS = False

def callTo(phoneNumber):
    ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)  # open serial port
    print(ser.name) # check which port was really used
    time.sleep(0.4)
    ser.write('AT') # Return to online command state from online data state
    time.sleep(1)
    ser.write('ATD' + phoneNumber + ';') # make a call
    time.sleep(5)
    ser.write('ATH') # Disconnect existing call
    ser.close() # close port

def sendSMS(phoneNumber, text):
    if (!shouldSensSMS):
        return
    ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)  # open serial port
    print(ser.name) # check which port was really used
    time.sleep(0.4)
    setTextModeCmd="AT+CMGF=1\r"
    ser.write(setTextModeCmd.encode()) # Configuring TEXT mode
    time.sleep(1)
    print(ser.readall())
    smsCmd="AT+CMGS=\"" + phoneNumber + "\"\r"
    ser.write(smsCmd.encode())
    time.sleep(1)
    print(ser.readall())
    ser.write(text.encode())
    time.sleep(1)
    print(ser.readall())
    ser.write(chr(26))
    time.sleep(1)
    print(ser.readall())
    ser.close() # close port

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # Rerencia de codigos da placa GPRS https://www.makerfabs.com/desfile/files/A6A7A6CA20_AT_Commends.pdf
    print(msg.topic + " " + str(msg.payload))
    if (msg.topic == 'esp/controle'):
        isSystemOn = not (isSystemOn)
    else:
        if (msg.payload == 'luz'):
            sendSMS(mauricioSMS, 'PERIGO: COFRE ABERTO!')
            shouldSensSMS = False
        if (msg.payload == 'solto'):
            sendSMS(mauricioSMS, 'PERIGO: COFRE VIOLADO!')
            shouldSensSMS = False
        if (msg.payload == 'presente')
        if (msg.payload == 'ok' or msg.payload == 'pressionado' or msg.payload == 'faltou'):
            shouldSensSMS = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
