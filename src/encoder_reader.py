#!/usr/bin/env python

import RPIO

class EncoderReader:
    
    def __init__(self, port_channelA, port_channelB):
        #port_channelA = 17
        #port_channelB = 27
        
        self.port_channelA = port_channelA
        self.port_channelB = port_channelB

        self.encoderCounter = 0L  # the counter value of the encoder defined as long data-type
        self.lastEncoded = 0
        self.oldChannelAValue = 0
        self.oldChannelBValue = 0

        self.channelAValue = 0
        self.channelBValue = 0
        
        self.setupEncoder()
    
    def getCounterValue(self):
        return self.encoderCounter    

    def encoderHandler_callback(self, port_channel, newChannelAValue):
        # handler routine of LOW to HIGH transition on channel A
        #global encoderCounter
        #global lastEncoded
        
        # read input from channel A
        newChannelAValue = RPIO.input(self.port_channelA)
        # read input from channel B
        newChannelBValue = RPIO.input(self.port_channelB)
        
        encoded = (newChannelAValue << 1) | newChannelBValue
        sumEncoded = (self.lastEncoded << 2) | encoded
        
        if sumEncoded == 0b1101 or sumEncoded == 0b0100 or sumEncoded == 0b0010 or sumEncoded == 0b1011 : 
            self.encoderCounter += 1  # increment the counter value of the encoder 
        
        if sumEncoded == 0b1110 or sumEncoded == 0b0111 or sumEncoded == 0b0001 or sumEncoded == 0b1000 :
            self.encoderCounter -= 1  # decrement the counter value of the encoder
        
        self.lastEncoded = encoded
              
        return True
    
    def channelAHanlder(self, port, value):
        global encoderCounter
        global channelAValue
        global channelBValue
        channelAValue = value
        print ('A: A={} B={} count={}'.format(channelAValue, channelBValue, encoderCounter))
    
        if (channelAValue):
            # channel A rise
            if (channelBValue):
                encoderCounter -= 1
            else:
                encoderCounter += 1
        else:
            # channel A fall
            if (channelBValue):
                encoderCounter += 1
            else:
                encoderCounter -= 1
    
    def channelBHanlder(self, port, value):
        global encoderCounter
        global channelAValue
        global channelBValue
        channelBValue = value
        print ('B: A={} B={} count={}'.format(channelAValue, channelBValue, encoderCounter))
    
        if (channelBValue):
            # channel A rise
            if (channelAValue):
                encoderCounter += 1
            else:
                encoderCounter -= 1
        else:
            if (channelAValue):
                encoderCounter -= 1
            else:
                encoderCounter += 1
    
    
    def setupEncoder(self):
        # change to BOARD numbering schema
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(self.port_channelA, RPIO.IN)
        RPIO.setup(self.port_channelB, RPIO.IN)
        RPIO.wait_for_interrupts(threaded=True)
        RPIO.add_interrupt_callback(self.port_channelA, self.encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)
        RPIO.add_interrupt_callback(self.port_channelB, self.encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)


