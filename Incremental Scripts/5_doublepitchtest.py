###################################################################################
#                                                                                 #
# This script is written by Wells Lucas Santo, for the final project component of #
# EE4163 at the NYU Tandon School of Engineering. Please give credit if you wish  #
# to reproduce this code.                                                         #
#                                                                                 #
# Be sure to read README.md for more information on these scripts.                #
#                                                                                 #
###################################################################################

# This code is used just to test that two different streams in PyAudio can both
# be opened at the same time, and that sound can be played simultaneously from both.

# This code is heavily based off of the script 'play_randomly_plots.py'
# which is provided as part of EE4163, which I modified as part of Lab 5.

import pyaudio
from math import sin, cos, pi
import numpy as np
import struct

# Set up audio properties
BLOCKSIZE   = 1024
WIDTH       = 2
CHANNELS    = 1
RATE        = 8000
T = 10
NumBlocks = T * RATE / BLOCKSIZE
y = [0 for i in range(BLOCKSIZE)]
y2 = [0 for i in range(BLOCKSIZE)]

Ta = 0.8
r = 0.01 ** (1.0 / (Ta * RATE))

# List of frequencies to play from
f = [523, 587, 659, 699, 784, 880, 494]
om = [2.0 * pi * float(f1) / RATE for f1 in f]

# List of filter coefficients (will select randomly from this)
a1 = [-2*r*cos(om1) for om1 in om]
a2 = r**2
b0 = [sin(om1) for om1 in om]

# Open the TWO audio output streams
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

stream2 = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

print 'Playing for {0:f} seconds ...'.format(T),
THRESHOLD = 2.5 / RATE

rand_index = 0
rand_index2 = 1

# Loop through all blocks
for i in range(0, NumBlocks):
    # Generate sound using second-order difference equation
    # and block processing

    for n in range(BLOCKSIZE):
        # Generate random value for random start time
        rand_val = np.random.rand()
        x = 0
        if rand_val < THRESHOLD:
            x = 5000
            # Randomly select a value from 7 possible values for BOTH streams
            rand_index = np.random.randint(0, 7)
            rand_index2 = np.random.randint(0, 7)

        # Update the output on BOTH streams
        y[n] = b0[rand_index] * x - a1[rand_index] * y[n-1] - a2 * y[n-2]
        y2[n] = b0[rand_index2] * x - a1[rand_index2] * y2[n-1] - a2 * y2[n-2]

    # Clip all the output values on BOTH streams
    y = np.clip(y, -32000, 32000)
    y2 = np.clip(y2, -32000, 32000)

    # Convert numeric list to binary string on BOTH streams
    data = struct.pack('h' * BLOCKSIZE, *y)
    data2 = struct.pack('h' * BLOCKSIZE, *y2)

    # Write binary string to BOTH audio output stream
    stream.write(data, BLOCKSIZE)
    stream2.write(data2, BLOCKSIZE)

# Close BOTH streams
stream.stop_stream()
stream.close()
stream2.stop_stream()
stream2.close()

p.terminate()
