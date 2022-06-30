import sys
import time
import os
from dotenv import load_dotenv
import RPi.GPIO as GPIO
import requests
import json

# getting environment variables
load_dotenv()
gpio_pin = int(os.getenv('GPIO_PIN'))
temperature_target = float(os.getenv('TEMPERATURE_TARGET'))
api_key = os.getenv('API_KEY')
api_url = os.getenv('API_URL') + '?x-aio-key=' + api_key
request_delay = float(os.getenv('REQUEST_DELAY'))
fan_power = float(os.getenv('FAN_POWER'))
fan_current_power = 0
fan_is_on = False
amount_seconds_fan_on = 0
temperature_dif_percentage = 0
power_consumption = 0

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)
fan_clockwise = GPIO.PWM(gpio_pin, 50)
fan_clockwise.start(0)


def get_temperature_in_celsius():
    r = requests.get(api_url)
    data = json.loads(r.text)
    return float(data['value'])


try:
    while True:
        print("Current Power Consumption = " + str(power_consumption) + " Ws")
        current_temperature = get_temperature_in_celsius()
        print("Current temperature: " + str(current_temperature))
        # temperature is too high, start fan
        if current_temperature > temperature_target:
            temperature_dif_percentage = int(round((current_temperature - temperature_target) / temperature_target * 100))
            if temperature_dif_percentage > 100:
                temperature_dif_percentage = 100
            power_consumption = fan_current_power * (temperature_dif_percentage / 100) * amount_seconds_fan_on
            # set power to temp dif percentage
            fan_clockwise.start(temperature_dif_percentage)
        # temperature is low enough, stop fan
        else:
            print("stopping fan")
            fan_clockwise.stop()

        if fan_is_on:
            amount_seconds_fan_on += request_delay

        time.sleep(request_delay)

except KeyboardInterrupt:
    print('Closing')
    GPIO.cleanup()
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    sys.exit(0)
