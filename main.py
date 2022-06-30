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
temperature_start_fan = float(os.getenv('TEMPERATURE_START_FAN'))
temperature_stop_fan = float(os.getenv('TEMPERATURE_STOP_FAN'))
api_key = os.getenv('API_KEY')
api_url = os.getenv('API_URL') + '?x-aio-key=' + api_key
request_delay = float(os.getenv('REQUEST_DELAY'))
fan_power = float(os.getenv('FAN_POWER'))
fan_is_on = False
amount_seconds_fan_on = 0

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)


def get_temperature_in_celsius():
    r = requests.get(api_url)
    data = json.loads(r.text)
    return float(data['value'])


try:
    while True:
        power_consumption = fan_power * amount_seconds_fan_on
        print("Current Power Consumption = " + str(power_consumption) + " Ws")
        current_temperature = get_temperature_in_celsius()
        print("Current temperature: " + str(current_temperature))
        # temperature is too high, start fan
        if current_temperature >= temperature_start_fan:
            if not fan_is_on:
                print("starting fan")
                fan_is_on = True
                GPIO.output(gpio_pin, True)
        # temperature is low enough, stop fan
        elif current_temperature <= temperature_stop_fan:
            if fan_is_on:
                print("stopping fan")
                fan_is_on = False
                GPIO.output(gpio_pin, False)

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
