import sys
import time
import os
from dotenv import load_dotenv
#import RPi.GPIO as GPIO
import requests
import json
from pprint import pprint

# getting environment variables
load_dotenv()
gpio_pin = float(os.getenv('GPIO_PIN'))
temperature_start_fan = float(os.getenv('TEMPERATURE_START_FAN'))
temperature_stop_fan = float(os.getenv('TEMPERATURE_STOP_FAN'))
api_key = os.getenv('API_KEY')
api_url = os.getenv('API_URL') + '?x-aio-key=' + api_key
request_delay = float(os.getenv('REQUEST_DELAY'))

# GPIO setup
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(gpio_pin, GPIO.OUT)


def get_temperature_in_celsius():
    r = requests.get(api_url)
    data = json.loads(r.text)
    return float(data['value'])


try:
    while True:
        current_temperature = get_temperature_in_celsius()
        pprint(current_temperature)
        print("Current temperature: " + str(current_temperature))
        # temperature is too high, start fan
        if current_temperature >= temperature_start_fan:
            print("starting fan")
            #GPIO.output(gpio_pin, True)
        # temperature is low enough, stop fan
        elif current_temperature <= temperature_stop_fan:
            print("stopping fan")
            #GPIO.output(gpio_pin, False)
        time.sleep(request_delay)

except KeyboardInterrupt:
    print('Closing')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    sys.exit(0)
