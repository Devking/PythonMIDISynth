###################################################################################
#                                                                                 #
# This script is written by Wells Lucas Santo, for the final project component of #
# EE4163 at the NYU Tandon School of Engineering. Please give credit if you wish  #
# to reproduce this code.                                                         #
#                                                                                 #
# Be sure to read README.md for more information on these scripts.                #
#                                                                                 #
###################################################################################

# Again, be sure to read README.md (and look at the previous scripts) for more
# insight on how this code works.

# Note: 
# Separation of two consecutive pitches is by 1.059463
# Use this to get pitches across an entire range of 60 keys
f = [130.81 * 1.059463 ** i for i in range(0, 60)]

KEYDOWN   = 144
KEYUP     = 128

from pygame import midi
import pyaudio
import struct
import numpy as np
from math import sin, cos, pi

###############################
# Initialize sound parameters #
###############################

# This is based on the second-order difference equation code that we have used
# in the class, written by Professor Ivan Selesnick.

blockSize    = 32
sampleWidth  = 2
numChannels  = 1
samplingRate = 16000

Ta = 0.8
r = 0.01 ** (1.0 / (Ta * samplingRate))

# Calculate coefficients based on frequencies
om = [2.0 * pi * float(f1) / samplingRate for f1 in f]
a1 = [-2*r*cos(om1) for om1 in om]
a2 = r**2
b0 = [sin(om1) for om1 in om]

# Open the audio output stream
p = pyaudio.PyAudio()
stream = p.open(format            = p.get_format_from_width(sampleWidth),
                channels          = numChannels,
                frames_per_buffer = blockSize,
                rate              = samplingRate,
                input             = False,
                output            = True)

# Initialize the input and output values to 0
x = np.zeros(blockSize)
y = np.zeros(blockSize)

# Initialize the first pitch index to be 0
pitch = 0

###############################
# Initialize input detection for MIDI
###############################

midi.init()

INPUTNO = midi.get_default_input_id()
input = midi.Input(INPUTNO)

print '*******************'
print '** Ready to play **'
print '*******************'

while True:
    x[0] = 0.0

    if input.poll():
        eventslist = input.read(1000)
        for e in eventslist:
            event      = e[0]
            eventType  = event[0]
            eventID    = event[1]
            eventValue = event[2]

            if eventType == KEYDOWN:
                print 'Keydown on key', eventID, 'with intensity', eventValue

                # Produce output due to the keydown
                x[0] = 15000 * (eventValue / 130.0)
                # Notice that I'm only getting 60 keys of different pitches
                # So I take a modulo of 60 here
                pitch = eventID % 60;

            elif eventType == KEYUP:
                print 'Keyup on key', eventID

        # For formatting specific to my MIDI controller
        if eventType == KEYUP or eventType == KEYDOWN:
            print '-------------'

    # Update the value of the difference equation
    for n in range(blockSize):
        y[n] = b0[pitch] * x[n] - a1[pitch] * y[n-1] - a2 * y[n-2]

    # Output value of difference equation
    y = np.clip(y, -2**15+1, 2**15-1)
    data = struct.pack('h' * blockSize, *y)
    stream.write(data, blockSize)

# Close everything nicely
stream.stop_stream()
stream.close()
p.terminate()
midi.quit()
