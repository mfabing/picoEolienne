import network
import time
from math import sin
from umqtt.simple import MQTTClient
from machine import ADC, Pin, WDT

# Fill in your WiFi network name (ssid) and password here:
wifi_ssid = ""
wifi_password = ""

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = ""  # Your Adafruit IO username
mqtt_password = ""  # Adafruit IO Key
mqtt_publish_topic = ""  # The MQTT topic for your Adafruit IO Feed
# Enter a random ID for this MQTT Client  It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "picoDanielStAmatTallande"

# MQTT topics for the two feeds
mqtt_publish_topic_27 = "your-username/feeds/sensor-27"  # Replace with your feed name for sensor 27
mqtt_publish_topic_29 = "your-username/feeds/sensor-29"  # Replace with your feed name for sensor 29

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

# Initialize ADC for analog pins 26 and 28
adc1 = ADC(Pin(26)) # pin GPIO de l'anémomètre => V1
adc2 = ADC(Pin(27)) # pin GPIO du moteur de l'armoire qui alimente les plaquettes électronique = vitesse du rotor => V2
adc3 = ADC(Pin(28)) # pin GPIO des batteries 24V DC => V3

# Initialize the built-in LED
led = Pin(25, Pin.OUT)

# Initialize the watchdog timer
wdt = WDT(timeout=8300)  # Set the watchdog timeout to 8.3 seconds

# Publish a data point to the Adafruit IO MQTT server every 3 seconds
try:
    while True:
        # Check WiFi connection
        if not wlan.isconnected():
            print("WiFi disconnected. Reconnecting...")
            wlan.connect(wifi_ssid, wifi_password)
            while not wlan.isconnected():
                print('Waiting for connection...')
                time.sleep(1)
            print("Reconnected to WiFi")
            mqtt_client.connect()  # Reconnect to MQTT server

        # Feed the watchdog
        wdt.feed()
        
        # Read the analog values from pins 27 and 29
        value_adc1 = adc1.read_u16()
        value_adc3 = adc3.read_u16()

        # Turn on the LED
        led.on()
        
        # Publish the data to the respective topics!
        print(f'Publish 27: {value_adc1}')
        mqtt_client.publish(mqtt_publish_topic_27, str(value_adc1))

        print(f'Publish 29: {value_adc3}')
        mqtt_client.publish(mqtt_publish_topic_29, str(value_adc3))

        # Turn off the LED
        led.off()

        # Delay a bit to avoid hitting the rate limit (in theory this could be 2 seconds, but 3 is safer)
        time.sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()
    led.off()  # Ensure the LED is turned off in case of an error
