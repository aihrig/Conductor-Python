# TODO: Implement features for each MCU
class NodeMCU_Amica:
    '''
    A Microcontroller management class for the Amica NodeMCU
    '''

    class Led1:
        '''
        Built-in led 1
        '''

        def __init__(self):
            self._led = Pin(2, Pin.OUT)

        def on(self):
            self._led.value(0)

        def off(self):
            self._led.value(1)

    class Led2:
        '''
        Built-in led 2
        '''

        def __init__(self):
            self._led = Pin(16, Pin.OUT)

        def on(self):
            self._led.value(0)

        def off(self):
            self._led.value(1)
