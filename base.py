import RPi.GPIO as gpio
import time

seg = [8, 10, 12, 16, 18, 22, 24]
leds = [12, 22, 8]
fnd = [(1, 1, 1, 1, 1, 1, 0),
       (0, 1, 1, 0, 0, 0, 0),
       (1, 1, 0, 1, 1, 0, 1),
       (1, 1, 1, 1, 0, 0, 1),
       (0, 1, 1, 0, 0, 1, 1),
       (1, 0, 1, 1, 0, 1, 1),
       (1, 0, 1, 1, 1, 1, 1),
       (1, 1, 1, 0, 0, 0, 0),
       (1, 1, 1, 1, 1, 1, 1),
       (1, 1, 1, 1, 0, 1, 1)]



def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(seg, gpio.OUT, initial=gpio.LOW)
    gpio.setwarnings(False)


def run():
    while True:
        try:
            i = int(input())
            for a in range(7):
                gpio.output(seg[a], gpio.HIGH if fnd[i][a] == 1 else gpio.LOW)
        except:
            pass
        #for i in range(10):
         #   for j in range(7):
          #      gpio.output(seg[j], gpio.HIGH if fnd[i][j] == 1 else gpio.LOW)
           # time.sleep(1)
    
#    pwmLed.start(1)
 #   
  #  for i in range(100):
   #     pwmLed.ChangeDutyCycle(i + 1)
    #    time.sleep(0.01)
        
    #pwmLed.stop()
        
    

if __name__ == '__main__':
    init()
    #pwmLed = gpio.PWM(leds[0], 1)
    run()