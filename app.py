from flask import *
import RPi.GPIO as GPIO
import time


app = Flask(__name__)

# define pin number
red_pin = 12
green_pin = 10
blue_pin = 8

# set pin numbering mode
GPIO.setmode(GPIO.BOARD)

# setup pins as output
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

red = GPIO.PWM(red_pin, 100)
green = GPIO.PWM(green_pin, 100)
blue = GPIO.PWM(blue_pin, 100)

# current values of RGB pins
red_value = 0
green_value = 0
blue_value = 0

off = True

# if user go to http://<ip> he will see /templates/html page with current values for red, green and blue
@app.route('/')
def home():
    return render_template('index.html', red=red_value, green=green_value, blue=blue_value)

#route where js sends request to change value of RGB pins
@app.route('/rgb/<int:red_val>/<int:green_val>/<int:blue_val>')
def rgb(red_val, green_val, blue_val):
   # inicializing global variables
   global off
   global red_value
   global green_value
   global blue_value

   # assigning values in request to global variables
   red_value = red_val
   green_value = green_val
   blue_value = blue_val

   # if RGB values in request are higher than 0, led will shine
   if off:
      red.start(red_val)
      green.start(green_val)
      blue.start(blue_val)
      off = False
   
   # changing RGB values
   red.ChangeDutyCycle(red_val)
   green.ChangeDutyCycle(green_val)
   blue.ChangeDutyCycle(blue_val)
   
   # if RGB values are equal to 1, then led will stop shining
   # it's because PWM can never be 0
   if red_val == 1 and blue_val == 1 and green_val == 1:
      red.stop()
      green.stop()
      blue.stop()
      off = True
   
   # just for make sure i don't break the pins
   time.sleep(0.01)

   # this can return nothing, however you don't see annoying error message in log
   return "True"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
