#!/usr/bin/env python

import RPIO
from time import sleep

PORT_ENCODER_CHANNELA = 17
PORT_ENCODER_CHANNELB = 27

encoderCounter = 0L  # the counter value of the encoder defined as long data-type
lastEncoded = 0
oldChannelAValue = 0
oldChannelBValue = 0

channelAValue = 0
channelBValue = 0

def encoderHandler_callback(port_channel, newChannelAValue):
    # handler routine of LOW to HIGH transition on channel A
    global encoderCounter
    global lastEncoded
    
    # read input from channel A
    newChannelAValue = RPIO.input(PORT_ENCODER_CHANNELA)
    # read input from channel B
    newChannelBValue = RPIO.input(PORT_ENCODER_CHANNELB)
    
    encoded = (newChannelAValue << 1) | newChannelBValue
    sumEncoded = (lastEncoded << 2) | encoded
    
    if sumEncoded == 0b1101 or sumEncoded == 0b0100 or sumEncoded == 0b0010 or sumEncoded == 0b1011 : 
        encoderCounter += 1  # increment the counter value of the encoder 
    
    if sumEncoded == 0b1110 or sumEncoded == 0b0111 or sumEncoded == 0b0001 or sumEncoded == 0b1000 :
        encoderCounter -= 1  # decrement the counter value of the encoder
    
    lastEncoded = encoded
          
    return True

def channelAHanlder(port, value):
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

def channelBHanlder(port, value):
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


def setupEncoder():
    # change to BOARD numbering schema
    RPIO.setmode(RPIO.BCM)
    RPIO.setup(PORT_ENCODER_CHANNELA, RPIO.IN)
    RPIO.setup(PORT_ENCODER_CHANNELB, RPIO.IN)
    RPIO.wait_for_interrupts(threaded=True)
    RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELA, encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)
    RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELB, encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)
    #RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELA, encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)
    #RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELB, encoderHandler_callback, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True, debounce_timeout_ms=None)
    #RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELA, channelAHanlder, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True)
    #RPIO.add_interrupt_callback(PORT_ENCODER_CHANNELB, channelBHanlder, edge='both', pull_up_down=RPIO.PUD_OFF, threaded_callback=True)
    
setupEncoder()        

while True:
    sleep(0.01)
    print ('Encoder counter {}'.format(encoderCounter))

