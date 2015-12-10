###################################################################################
#                                                                                 #
# This script is written by Wells Lucas Santo, for the final project component of #
# EE4163 at the NYU Tandon School of Engineering. Please give credit if you wish  #
# to reproduce this code.                                                         #
#                                                                                 #
# Be sure to read README.md for more information on these scripts.                #
#                                                                                 #
###################################################################################

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

# List of frequencies to play from
f = [494, 523, 554, 587, 622, 659, 699, 740, 784, 831, 880, 932]

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

y = np.zeros(blockSize)
x = np.zeros(blockSize)
rand_index = 0

#######################################
# Initialize input detection for MIDI #
#######################################

midi.init()
input = midi.Input(midi.get_default_input_id())

KEYDOWN   = 144
KEYUP     = 128

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
                # Notice in this case that I'm randomly choosing between different
                # pitches instead of using just a single pitch
                rand_index = np.random.randint(0, 7)

            elif eventType == KEYUP:
                print 'Keyup on key', eventID

        # Some output formatting specific to my MIDI controller
        if eventType == KEYDOWN or eventType == KEYUP:
            print '-------------'

    # Update the value of the difference equation
    for n in range(blockSize):
        y[n] = b0[rand_index] * x[n] - a1[rand_index] * y[n-1] - a2 * y[n-2]

    y = np.clip(y, -2**15+1, 2**15-1)
    data = struct.pack('h' * blockSize, *y)
    stream.write(data, blockSize)

stream.stop_stream()
stream.close()
p.terminate()
midi.quit()
