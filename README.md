# Python MIDI Synthesizer

This is the README for my Python MIDI Synthesizer project, which I completed in Fall 2015 as part of EE4163 (DSP Lab) at the NYU Tandon School of Engineering with Professor Ivan Selesnick.

This README only covers a general overview of the different scripts that you will find in this repository. For a more detailed explanation of my project, please read the `Report.pdf` file.

To actually run the main `MIDIKeyboardSynthesizer.py` script, you will need to use the hardware/software specifically listed below.

## Background

This project makes use of the **PyGame** and **PyAudio** packages within Python to detect MIDI events triggered from my **Alesis Q49** MIDI keyboard and then output audio corresponding to the pitches played.

That is, when you play a note on the MIDI keyboard, the script will detect the note using the MIDI functionality in PyGame and play the appropriate pitch based on which note you played using PyAudio. This code does not make use of any pre-recorded audio. The audio is generated in real time using a second-order difference equation that generates a series of time-domain output values.

You can find more about the hardware/software I used from the following links:
* [Alesis Q59](http://www.alesis.com/products/legacy/q49)
* [PyGame](https://www.pygame.org)
* [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)

If you have your own MIDI keyboard, it will be pretty easy to go in and modify my script so that it works for your MIDI keyboard. You can make use of my incremental scripts to do this modification as well.

## Incremental Scripts

I personally like to engage in an incremental coding process. That is, instead of tackling the final script at once, I like to write smaller scripts that break up the problem into smaller, separate subproblems so that I can test different pieces of the project one step at a time.

Within the `Incremental Scripts` folder, I have 6 Python scripts and one plain text file that I wrote during my incremental coding process. Each script builds on the last, so that I'm closer to solving the overall MIDI synthesizer task with each increment.

### 0_miditest.py

The first thing I needed to test was that I could actually get PyGame working, so that it could detect MIDI events from my Alesis Q49 MIDI keyboard.

This script merely tests the basic MIDI functionality provided by PyGame in order to get the MIDI devices available and poll the default input device for events. This script then prints out the specific MIDI events that are triggered, so that I could identify what exactly was going on with my Alesis Q49 keyboard.

If you wish to modify the main script by using your own MIDI controller, this script will be important for you to:
 1. Identify that your MIDI device is successfully connected and detected by your computer
 2. Identify which MIDI device you want to take input from (it may not necessarily be the default)
 3. Identify the MIDI events that your device triggers

After running this script, I populated the `AlesisQ49MIDIvalues.txt` text file with empirical information about the MIDI events that I found were specific to my Alesis Q49.

### 1_alesisdetect.py

Now that I know my MIDI controller can be detected, and I know what sorts of events I want to detect, it's time to actually sort out just the information I need for my project.

I only need to get keydown and keyup events, so I only check for those events in this script.

Once I get a keydown/keyup event, I also want to know what key I pressed, and with what intensity.

This script is really just a sanity check that I can pull out the specific information I need.

### 2_alesiswithsound.py

This script is a bit more complicated, since I'm outputting sound for the first time. In order to generate audio, I'm using a second-order difference equation with set parameters for decay time, amplitude, pitch, etc. This audio code comes directly from the EE4163 course that this project was completed as part of.

With this second-order difference equation, I trigger an impulse response in the input that will be sent into linear / time-invariant (LTI) system described by the second-order difference equation. This generates output values that correspond to an output audio signal, and I use PyAudio to send these output values to the speakers.

The difficult component with this script is getting the keypress that we detected in the last two scripts to trigger an impulse (and output audio). I also make use of the intensity of the keypress here to manipulate how loud the output audio should be.

Note that this script will only play one note at a time, and no matter where you press on the keyboard, the same pitch will be played. The purpose of this script is just to make sure that audio can be output from the speakers when you hit a key on the MIDI controller.

### 3_alesiswithrandompitch.py

In order to prepare for playing pitches that correspond to the key/pitch you play on the keyboard, it's important to first make sure that we can output multiple pitches to begin with.

This script is really just a bit more manipulation with the second-order difference equation, so that we make sure we keep a list of coefficients corresponding to different frequencies/pitches to use when keys are pressed. So when a key is pressed, we will select one set of coefficients to plug into the difference equation.

This code still only plays one note at a time, but now the frequency of the notes is different. This is accomplished by using a list of different filter coefficients.

### 4_alesiswithsinglepitch.py

Since we can get different pitches to be played, it's important to match up those pitches with the actual keys being played. This might be a bit difficult for those who are not familiar with the theory behind musical pitches, but it's quite easy to code up. 

### 5_doublepitchtest.py

### 6_alesiswithmultiplepitches.py

## MIDIKeyboardSynthesizer.py
