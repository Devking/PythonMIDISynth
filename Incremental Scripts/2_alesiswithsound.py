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

BLOCKSIZE = 32      # Number of frames per block
WIDTH = 2           # Bytes per sample
CHANNELS = 1        # Mono
RATE = 16000        # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 1.2            # Decay time (seconds)
f1 = 440            # Frequency (Hz)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))        # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format            = PA_FORMAT,
                channels          = CHANNELS,
                frames_per_buffer = BLOCKSIZE,
                rate              = RATE,
                input             = False,
                output            = True)

y = np.zeros(BLOCKSIZE)
x = np.zeros(BLOCKSIZE)

#######################################
# Initialize input detection for MIDI #
#######################################

# This code comes from the building blocks that we've explored in
# the previous two scripts, '0_miditest.py' and '1_alesisdetect.py'

midi.init()
input = midi.Input(midi.get_default_input_id())

KEYDOWN   = 144
KEYUP     = 128

print '*******************'
print '** Ready to play **'
print '*******************'

# We want to keep this running for the entire program
while True:

    # Set the current input to 0, since nothing is being played
    # at the moment
    x[0] = 0.0

    if input.poll():

        # Go through all of the events picked up
        eventslist = input.read(1000)

        for e in eventslist:
            # Get just the event information (discard the timestamp)
            event      = e[0]
            eventType  = event[0]
            eventID    = event[1]
            eventValue = event[2]

            # Capture the keyups and the keydowns
            if eventType == KEYDOWN:
                print 'Keydown on key', eventID, 'with intensity', eventValue

                # Produce output due to the keydown (also take into account intensity)
                x[0] = 15000 * (eventValue / 130.0)

            elif eventType == KEYUP:
                print 'Keyup on key', eventID

        # Just to ignore the pitch and modulation knobs for some print-out styling
        # This is just some command line output formatting specific to my MIDI controller
        if eventType == KEYDOWN or eventType == KEYUP:
            print '-------------'

    # Update the value of the difference equation
    for n in range(BLOCKSIZE):
        y[n] = b0 * x[n] - a1 * y[n-1] - a2 * y[n-2]

    # Output the value of the difference equation to audio, using PyAudio
    y = np.clip(y, -MAXVALUE, MAXVALUE)
    data = struct.pack('h' * BLOCKSIZE, *y)
    stream.write(data, BLOCKSIZE)

# Close everything up nicely
stream.stop_stream()
stream.close()
p.terminate()
midi.quit()
