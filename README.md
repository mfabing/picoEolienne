### README: Raspberry Pi Pico W Monitoring System

---

#  Monitoring System for Raspberry Pi Pico W

This project demonstrates how to use the **Raspberry Pi Pico W** to monitor parameters using analog sensors, send the data to a remote server via WiFi, and ensure reliability with a watchdog timer.

---

## Features
- **Sensor Integration**: Reads data from:
  - **Anemometer** (wind speed sensor connected to GPIO 26).
  - **Battery Voltage Sensor** (connected to GPIO 28).
- **WiFi Connectivity**: Connects to a specified WiFi network and sends sensor data to a remote server via HTTP GET requests.
- **Watchdog Timer**: Ensures the system resets if the program encounters an error or hangs for too long.
- **Status Indication**: Uses the onboard LED for visual feedback:
  - Blinks during WiFi connection.
  - Lights up briefly after successful data transmission.

---

## Hardware Requirements
- **Raspberry Pi Pico W**
- Sensors:
  - Anemometer (or equivalent wind speed sensor).
  - Voltage measurement module for battery monitoring.
- WiFi access point for internet connectivity.

---

## Software Requirements
- **MicroPython Firmware**: Install MicroPython on the Pico W.
- **Python Libraries**:
  - `machine`: For GPIO and ADC operations.
  - `network`: For WiFi connectivity.
  - `time`: For delays.
  - `requests`: For HTTP requests.

---

## Installation
1. **Flash MicroPython** onto your Raspberry Pi Pico W:
   - Download the latest MicroPython firmware from [here](https://micropython.org/download/rp2-pico-w/).
   - Flash it using tools like [Thonny](https://thonny.org/).

2. **Upload the Code**:
   - Save the provided Python script (`main.py`) and upload it to the Pico W using an IDE like Thonny.

3. **Connect Sensors**:
   - Connect your sensors to the appropriate GPIO pins as defined in the code:
     - GPIO 26 for the anemometer.
     - GPIO 28 for battery voltage.
   - Ensure proper power supply to the sensors.

4. **Configure WiFi Credentials**:
   - Edit the `ssid` and `pw` variables in the code with your WiFi network's name and password.

---

## Usage
1. Power on the Raspberry Pi Pico W.
2. The onboard LED will blink while connecting to WiFi.
3. Once connected, the system will:
   - Read analog values from the sensors.
   - Send the data to the configured server endpoint:
     ```
     https://jacqueline-michel.com/drapeau/?adc_anemometre={value}&adc_batteries={value}
     ```
4. Monitor the console output for status updates, errors, or HTTP response content.

---

## Watchdog Timer
The watchdog timer ensures the system remains responsive:
- If the program hangs for more than **16 seconds**, the Pico W will automatically reset.
- The timeout value can be configured in the line:
  ```python
  wdt = WDT(timeout=5000)  # Timeout in milliseconds
  ```

---

## Troubleshooting
- **WiFi Issues**: Ensure the SSID and password are correct. Check your network signal strength.
- **Sensor Readings**: Verify sensor connections and calibrations.
- **Watchdog Resets**: If the system resets frequently, increase the timeout or debug the main loop for potential delays.

---

## License
This project is open-source under the MIT License. Feel free to use, modify, and distribute the code.

---

## Author
Developed by Michael Fabing. If you have any questions or feedback, feel free to reach out or open an issue on GitHub.
