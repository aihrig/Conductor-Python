import os
import sys

sys.path.append('/')
from machine import Pin, PWM
from time import sleep
import _thread
from conductor.mcu import NodeMCU_Amica
from instance import config as cfg

class Train:
    '''
    A class to represent physical train functions

    Attributes
    ----------
    name : str
        The name of the train
    speed : int
        Speed of the train from -100 (reverse) to 100 (forward)

    Methods
    -------
    None

    '''

    def __init__(self, name):
        '''
        Parameters
        ----------
        name : str
            Unique name to represent physical train
        '''

        self.name = name
        # TODO: make controller dynamically assigned based on config
        self._controller = NodeMCU_Amica()
        self._headlights = Train._Headlights()
        self._engine = Train._Engine()
        self.speed = 0
        self.direction = 1

    class _Headlights:
        '''
        A class to manage the train's headlights

        Attributes
        ----------
        None

        Methods
        -------
        on()
            Turns on train headlights
        off()
            Turns off train headlights
        '''

        def __init__(self):
            # TODO: make this based on self.controller object.
            # Setup config to allow pins to be specified for motor and LEDs.
            # self._led_left = Pin(14, Pin.OUT)
            self._led_right = Pin(int(cfg.led_pins['headlight_right_pin']), Pin.OUT)
            self._led_left = Pin(int(cfg.led_pins['headlight_left_pin']), Pin.OUT)
            self._led_freq = 5000
            self._is_alternating = False

        def on(self):
            ''' Turn on headlights full power '''
            print("Turning headlights on")
            self._led_left.on()
            self._led_right.on()
            self._is_alternating = False            

        def off(self):
            ''' Turn off headlights '''
            print("Turning headlights off")
            self._led_left.off()
            self._led_right.off()
            self._is_alternating = False            

        def _alternate(self):
            ''' Alternate and fade on/off headlights '''
            print("Alternating headlights")

            # Initialize PWM for led
            led_left = PWM(self._led_left, self._led_freq)
            led_right = PWM(self._led_right, self._led_freq)
            while self._is_alternating:
                # TODO: Add left LED once ground bus is finished
                for duty_cycle in range(0, 1024):
                    led_right.duty(duty_cycle)
                    led_left.duty(1023 - duty_cycle)
                    sleep(0.001)

                for duty_cycle in range(1023, 25, -1):
                    led_right.duty(duty_cycle)
                    led_left.duty(1023 - duty_cycle)
                    sleep(0.001)
            
            # Revert led pin to standard digital
            led_right.deinit()
            led_left.deinit()

        def alternate_start(self):
            ''' Start thread to alternate and fade on/off headlights '''
            self._is_alternating = True
            _thread.start_new_thread(self._alternate(), ())


    class _Engine:
        '''
        A class to manage the train's motor

        Attributes
        ----------
        speed : int
            Current speed percentage from -100 (reverse) to 100 (forward)

        Methods
        -------
        forward(speed)
            Sets forward speed in percentage from 0 to 100
        reverse(speed)
            Sets reverse speed in percentage from 0 to 100
        '''

        def __init__(self):
            self._speed = 0
            self._direction = 1

            # Initialize pin values from config.py
            try:
                self._pwm_pin = PWM(Pin(int(cfg.motor_pins['pwm_pin'])))
                self._pwm_pin.duty(0)
                self._pwm_pin.freq(200)
                self._dir1_pin = Pin(int(cfg.motor_pins['dir1_pin']), Pin.OUT)
                self._dir2_pin = Pin(int(cfg.motor_pins['dir2_pin']), Pin.OUT)
                self.direction = 1
            # TODO Add global error handler mechanism
            except ValueError as ex:
                print('Error: Pin values in config file must be numbers.')

        @property
        def direction(self):
            ''' Get direction of train '''
            return self._direction

        @direction.setter
        def direction(self, value):
            ''' Set direction of train - 1 = forward, -1 = reverse '''
            if not value==1 and not value==-1:
                raise ValueError("Direction value must be 1 for forward or "
                                + "-1 for reverse.")
            elif value == 1:
                # Motor direction configuration forward
                print('Setting direction to forward')
                self._dir1_pin.value(1)
                self._dir2_pin.value(0)
                self._direction = 1
            else:
                # Motor direction configuration reverse
                print('Setting direction to reverse')
                self._dir1_pin.value(0)
                self._dir2_pin.value(1)
                self._direction = -1
        
        def speed(self, speed):
            self._pwm_pin.duty(speed)
