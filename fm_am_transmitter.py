import RPi.GPIO as GPIO
import time

class BaseTransmitter:
    def __init__(self, gpio_pin, frequency):
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        self.pwm = None
        self.pwm_started = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def start(self):
        if self.pwm is None:
            self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
        self.pwm.start(50)  # 50% duty cycle
        self.pwm_started = True

    def stop(self):
        if self.pwm:
            self.pwm.stop()
            self.pwm = None
        self.pwm_started = False

    def set_frequency(self, frequency):
        self.frequency = frequency
        if self.pwm_started and self.pwm:
            self.pwm.ChangeFrequency(self.frequency)

class FMTransmitter(BaseTransmitter):
    """
    FM transmission simulated via high-frequency PWM (requires low-pass filter to work realistically).
    """
    def __init__(self, gpio_pin, frequency=100000000):  # Default: 100 MHz
        super().__init__(gpio_pin, frequency)

class AMTransmitter(BaseTransmitter):
    """
    AM transmission simulated via PWM (with modulation technique if extended).
    """
    def __init__(self, gpio_pin, frequency=1000000):  # Default: 1 MHz
        super().__init__(gpio_pin, frequency)
