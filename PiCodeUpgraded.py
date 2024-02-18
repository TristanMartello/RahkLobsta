import socket
import RPi.GPIO as GPIO
import time

# selfIp = "10.245.158.11"   # JCC IP
# selfIp = "10.245.145.164"  # NOLOP IP
selfIp = "10.0.0.242"  # HOME IP

# otherIp = "10.245.154.176" # JCC IP
# otherIp = "10.245.154.176" # NOLOP IP
otherIp = "10.0.0.145"  # HOME IP

port = 5005

ledPin = 4
motorPin1 = 23
motorPin2 = 24

motorPin3 = 22
motorPin4 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)

GPIO.setup(motorPin3, GPIO.OUT)
GPIO.setup(motorPin4, GPIO.OUT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((selfIp, port))

def motorOn(pin1, pin2):
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)

def resetPins(pin1, pin2):
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)

def handleMotors(pinA, pinB, pinC, pinD):
    motorOn(pinA, pinB)
    motorOn(pinC, pinD)
    time.sleep(0.08)
    resetPins(pinA, pinC)

def moveBot(direction):
    if direction == "forward":
        handleMotors(motorPin2, motorPin1, motorPin4, motorPin3)

    elif direction == "backward":
        handleMotors(motorPin1, motorPin2, motorPin3, motorPin4)

    elif direction == "left":
        handleMotors(motorPin1, motorPin2, motorPin4, motorPin3)

    elif direction == "right":
        handleMotors(motorPin2, motorPin1, motorPin3, motorPin4)

    return "none"


directionList = ["forward", "backward", "left", "right"]
lastHeadTime = time.monotonic()
headlights = False

while True:
    sock.sendto(bytes("request", "utf-8"), (otherIp, port))
    print("packet sent")

    data, addr = sock.recvfrom(1024)  # 1024 is buffer size
    data = str(data)[2:-1]
    print("received message: ", data)

    if data == "headlights":
        if lastHeadTime + 0.1 < time.monotonic():
            print("headlights pressed")
            headlights = not headlights
            lastHeadTime = time.monotonic()

    if data in directionList:
        data = moveBot(data)

    elif data == "halt":
        resetPins(motorPin1, motorPin2)
        resetPins(motorPin3, motorPin4)

    elif data == "quit":
        print("quitting")
        GPIO.output(ledPin, GPIO.LOW)
        resetPins(motorPin1, motorPin2)
        resetPins(motorPin3, motorPin4)
        GPIO.cleanup()
        break

    if headlights:
        GPIO.output(ledPin, GPIO.HIGH)
    else:
        GPIO.output(ledPin, GPIO.LOW)