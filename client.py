import os, subprocess
import glob
import time
from gpiozero import Buzzer, InputDevice
import requests, json

no_rain = InputDevice(18)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def get_uptime():
    out = subprocess.check_output("uptime -p", shell=True)
    return out

def get_temp():
    out = subprocess.check_output("./temp-check.sh", shell=True) 
    return out

def send(celsius, temp, uptime, raining):
    if raining == True:
        pioggia = "Sta piovendo"
    if raining == False:
        pioggia = "Non sta piovendo"

    headers = {
        "temperatura": str(celsius),
        "pioggia": pioggia,
	      "key": "key" # replace with your key
	
    }
    headers2  = {
        "temperatura": str(temp),
        "uptime": str(uptime),
	      "key": "key" # replace with your key
    }
    rq = requests.post("http://wsfoundation.pythonanywhere.com/api/stazione", headers=headers) # replace with your url
    rq2 = requests.post("http://wsfoundation.pythonanywhere.com/api/admin", headers=headers2) # replace with your url
    print(str(rq.status_code))

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    raining = False
    if not no_rain.is_active:
    	raining = True
    celsius = read_temp()
    print(celsius)
    temp = get_temp()
    uptime = get_uptime()
    send(celsius, temp, uptime, raining)
    time.sleep(60)

