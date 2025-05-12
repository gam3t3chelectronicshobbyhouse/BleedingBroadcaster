import RPi.GPIO as GPIO
import time
import threading

class WidebandTransmitter:
    def __init__(self, gpio_pin=4, frequency=100000):
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        self.pwm = None
        self.pwm_started = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def start(self):
        if not self.pwm_started:
            self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
            self.pwm.start(50)  # 50% duty cycle
            self.pwm_started = True

    def stop(self):
        if self.pwm_started and self.pwm:
            self.pwm.stop()
            self.pwm_started = False
            self.pwm = None

    def set_frequency(self, freq):
        self.frequency = freq
        if self.pwm_started and self.pwm:
            self.pwm.ChangeFrequency(self.frequency)
