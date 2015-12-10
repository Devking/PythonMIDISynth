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

midi.init()
input = midi.Input(midi.get_default_input_id())

# Here, I am specifying two values that correspond to specific MIDI events
# that my particular MIDI keyboard uses. You may have different values for
# your own MIDI controller.
KEYDOWN   = 144
KEYUP     = 128

print '** Ready to play **'

# We want to keep this running for the entire program
while True:

    # Detect MIDI input
    if input.poll():

        # Save concurrent MIDI events as a list
        eventslist = input.read(1000)

        # Go through all of the events in this list
        for e in eventslist:

            # Get just the event information (discard the timestamp)
            event = e[0]
            eventType  = event[0]
            eventID    = event[1]
            eventValue = event[2]

            # This just tests to see that my keydown/keyup events are picked up
            # correctly, and that the key ID and the intensity are correct
            if eventType == KEYDOWN:
                print 'Keydown on key', eventID, 'with intensity', eventValue
            elif eventType == KEYUP:
                print 'Keyup on key', eventID

        print ''

midi.quit()
