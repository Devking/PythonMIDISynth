###################################################################################
#                                                                                 #
# This script is written by Wells Lucas Santo, for the final project component of #
# EE4163 at the NYU Tandon School of Engineering. Please give credit if you wish  #
# to reproduce this code.                                                         #
#                                                                                 #
# Be sure to read README.md for more information on these scripts.                #
#                                                                                 #
###################################################################################

# Import the PyGame package, with the MIDI functionality specifically
from pygame import midi

# To use MIDI functionality, we need to first initialize MIDI
midi.init()

# This prints the default device ids that we are outputting to / taking input from
print 'Output ID', midi.get_default_output_id()
print 'Input ID', midi.get_default_input_id()

# List the MIDI devices that can be used
for i in range(0, midi.get_count()):
    print i, midi.get_device_info(i)

# Here, you must check what the device # for your MIDI controller is
# You will not be guaranteed that the MIDI controller you want to use is the default

# Start the input stream
input = midi.Input(midi.get_default_input_id())

# Here's an example of setting the input device to something other than the default
# input = midi.Input(3)

print '** Ready to play **'

while True:

    # Detect keypress on input
    if input.poll():

        # Get MIDI event information
        print input.read(1000)

# Look at the file 'AlesisQ49MIDIvalues.txt' for more information on MIDI events

# Close the midi interface
midi.quit()
