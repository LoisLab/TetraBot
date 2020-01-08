import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
GPIO.output(40, GPIO.LOW)
GPIO.cleanup()
