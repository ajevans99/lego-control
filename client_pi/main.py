#!/usr/bin/env python
import time
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
import RPi.GPIO as GPIO

CONTROL_POINT_ID = 1

def configure_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) ## Indicates which pin numbering configuration to use

    ledMouth = 8

    GPIO.setup(ledMouth, GPIO.OUT)
    GPIO.output(ledMouth, GPIO.HIGH)

    led = GPIO.PWM(ledMouth, 100)

    led.start(0)         

    return led

def open_websocket(led):
    query = gql('''
    subscription ($controlPointId: Int!) {
        lightStripBrightnessMonitor(controlPointId: $controlPointId) {
            lightStripId
            previousBrightness
            brightness
            gpioControlPin
        }
    }
    ''')

    transport = WebsocketsTransport(url='ws://192.168.86.58:8000/graphql')

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    for result in client.subscribe(query, variable_values={'controlPointId': CONTROL_POINT_ID}):
        print (result)
        brightness = result['data']['lightStripBrightnessMonitor'['brightness']]
        print(brightness)
        led.ChangeDutyCycle(result)

while True:
    try:
        led = configure_gpio()
        open_websocket(led)
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(e)
        time.sleep(5)
