import RPi.GPIO as gpio
from time import *
import I2C_driver
from Adafruit_BME280 import *

PWMpin= 35

seg = [8, 10, 12, 16, 18, 22, 24, 35]
fnd = [(1, 1, 1, 1, 1, 1, 0),
       (0, 1, 1, 0, 0, 0, 0),
       (1, 1, 0, 1, 1, 0, 1),
       (1, 1, 1, 1, 0, 0, 1),
       (0, 1, 1, 0, 0, 1, 1),
       (1, 0, 1, 1, 0, 1, 1),
       (1, 0, 1, 1, 1, 1, 1),
       (1, 1, 1, 0, 0, 0, 0),
       (1, 1, 1, 1, 1, 1, 1),
       (1, 1, 1, 1, 0, 1, 1),
       (0, 0, 0, 0, 0, 0, 0)]

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(seg, gpio.OUT, initial=gpio.LOW)
    gpio.setwarnings(False)
    
def segmentNumber(num):
    for a in range(7):
            gpio.output(seg[a], gpio.HIGH if fnd[num][a] == 1 else gpio.LOW)
    
def select():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("1. FND", 1)
    mylcd.lcd_display_string("2. motor", 2)
    print("1. FND\n2. motor\n3. ultrasonic\n4. tempPressure")
    return int(input())


def fndFun():
    mylcd.lcd_clear()
    for i in range(10):
        segmentNumber(i)
        mylcd.lcd_display_string(f"num {i}", 1)
        sleep(1)
    segmentNumber(10)
    

def motor():
    angle = int(input())
    mylcd.lcd_clear()
    mylcd.lcd_display_string(f"angle {angle}", 1)
    Servo.start(1)
    #print('Wating for 1 sec') 
    sleep(1) 
    
    #print('Rotating at interval of 0-12 degrees')
    Servo.ChangeDutyCycle(angle / 18)
    sleep(1)
    Servo.ChangeDutyCycle(1)
    sleep(1)
    #gpio.cleanup()
    #print('Everythings cleanup')
    
def ultrasonic():
    PinTrig=11
    PinEcho=13
    gpio.setmode(gpio.BOARD)  
    gpio.setup(PinTrig, gpio.OUT)           
    gpio.setup(PinEcho, gpio.IN)                    

    startTime=0
    stopTime=0
    while True:
        gpio.output(PinTrig, False)    
        sleep(2)

        print ('Calculating Distance. 1 nanosec pulse')
        gpio.output(PinTrig, True)          
        sleep(0.00001)            
        gpio.output(PinTrig, False)         

        while gpio.input(PinEcho) == 0:   
            startTime = time()
        while gpio.input(PinEcho) == 1:   
            stopTime = time()

        Time_interval= stopTime - startTime     
        Distance = Time_interval * 17000
        Distance = round(Distance, 2)
        
        mylcd.lcd_clear()
        mylcd.lcd_display_string(f"Distance => {Distance}cm", 2)
        
        if Distance >= 30:
            segmentNumber(3)
        elif Distance >= 20:
            segmentNumber(2)
        elif Distance >= 10:
            segmentNumber(1)
        else:
            segmentNumber(0)
            mylcd.lcd_display_string(f"door closer", 1)
            sleep(3)
            segmentNumber(10)
            break

        
def tempPressure():
    warning = 10
    while True:
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
#        humidity = sensor.read_humidity()
        
        mylcd.lcd_display_string(f"temp: {degrees}", 1)
        mylcd.lcd_display_string(f"pressure: {hectopascals}hPa", 2)

        if degrees >= 28:
            segmentNumber(warning)
            warning = abs(warning - 10)
            Servo.start(1)
            sleep(1) 
    
            #print('Rotating at interval of 0-12 degrees')
            Servo.ChangeDutyCycle(1 if warning == 0 else 10)
            sleep(1)
        
        
        
        
    
function = {
    1: fndFun,
    2: motor,
    3: ultrasonic,
    4: tempPressure}
    
if __name__ == '__main__':
    init()
    Servo=gpio.PWM(PWMpin, 50)
    sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
    mylcd = I2C_driver.lcd()
    while True:
        gpio.setmode(gpio.BOARD)
        num = select()
        function[num]()
