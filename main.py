import sys
import time
import os
from dotenv import load_dotenv
import RPi.GPIO as GPIO

# getting environment variables
load_dotenv()
sensor = '/sys/bus/w1/devices/' + os.getenv('SENSOR_FOLDER') + '/w1_slave'
# gpio_pin = float(os.getenv('GPIO_PIN'))
temperature_start_fan = float(os.getenv('TEMPERATURE_START_FAN'))
temperature_stop_fan = float(os.getenv('TEMPERATURE_STOP_FAN'))
temperature_measurement_interval = float(os.getenv('TEMPERATURE_MEASUREMENT_INTERVAL'))

# GPIO setup
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(gpio_pin, GPIO.OUT)


def read_temperature_sensor(sensor_name):
    # read sensor
    f = open(sensor_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


def get_temperature_in_celsius(sensor_name):
    lines = read_temperature_sensor(sensor_name)
    # try again until its data could be read
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temperature_sensor(sensor_name)
    temperature_str = lines[1].find('t=')
    # if temperature is found
    if temperature_str != -1:
        temperature_data = lines[1][temperature_str + 2:]
        temperature_celsius = float(temperature_data) / 1000.0
        return temperature_celsius


try:
    while True:
        current_temperature = get_temperature_in_celsius(sensor)
        print("Current temperature: " + str(current_temperature))
        # temperature is too high, start fan
        if current_temperature >= temperature_start_fan:
            print("starting fan")
            # GPIO.output(gpio_pin, True)
        # temperature is low enough, stop fan
        elif current_temperature <= temperature_stop_fan:
            print("stopping fan")
            # GPIO.output(gpio_pin, False)
        time.sleep(temperature_measurement_interval)

except KeyboardInterrupt:
    print('Closing')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    sys.exit(0)
