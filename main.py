from machine import ADC, Pin
from time import sleep
import time
import network
import requests

# Constantes
anemometre_pin = 26     	# pin GPIO de l'anémomètre => V1
#generatriceDC_pin = 27  	# pin GPIO du moteur de l'armoire qui alimente les plaquettes électronique = vitesse du rotor => V2
tensionbatterie_pin = 28 	# pin GPIO des batteries 24V DC => V3

# Activation ADC
adc1 = ADC(Pin(anemometre_pin))
#adc2 = ADC(Pin(generatriceDC_pin))
adc3 = ADC(Pin(tensionbatterie_pin))

# Identifiants WiFi
#ssid = "WiFi"
#pw = "WifiPassword"

# WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pw)

# Initialize watchdog timer (timeout in milliseconds, e.g., 15000ms = 15 seconds) (maximum is 2^24 clock cycles which is about 16.8 seconds)
wdt = WDT(timeout=15000)

while True:
    try:
	# Feed the watchdog to prevent system reset
        wdt.feed()
	    
        if wlan.isconnected():
        	adc1_value = adc1.read_u16()
		#adc2_value = adc2.read_u16()
		adc3_value = adc3.read_u16()

		# Send data via HTTP GET
		url = f"https://jacqueline-michel.com/drapeau/?adc_anemometre={adc1_value}&adc_batteries={adc3_value}"
		response = requests.get(url)

		# Check HTTP response (to uncomment for debugging purpose)
		# if response.status_code == 200:
		#     print("Data sent successfully:", response.text)
		# else:
		#     print(f"HTTP Error: {response.status_code}")
		
		# Blink LED to indicate that the data has been sent success
		led = Pin(25, Pin.OUT)
		led.on()
		sleep(1)
		led.off()
		
		sleep(3)  # Pause between iterations

        else:
            print("WiFi is disconnected. Reconnecting...")
            wlan.connect(ssid, password)
            sleep(5)  # Retry every 5 seconds
    except Exception as e:
        print("Error:", e)
        sleep(5)  # Wait before retrying
