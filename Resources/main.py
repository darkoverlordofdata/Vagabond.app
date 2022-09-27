#!/usr/bin/env python3
# A guitar effects application for raspberry pi
#from gpiozero import MCP3008, LEDBoard, LEDBarGraph
import signal, time, argparse
import pyo

numlines = 8
# pots = [MCP3008(channel=n) for n in range(numlines)]     
vals = [0] * numlines

# set up pyo input and effectgs
s = pyo.Server().boot()
s.start()
audio    = pyo.Input()
dry      = pyo.Input()


# wah effect
follow   = pyo.Follower(audio)
wahfq    = pyo.Scale(follow, outmin=300, outmax=20000)

delay    = pyo.SmoothDelay(audio, feedback=0.15)
reverb   = pyo.Freeverb(delay)
chorus   = pyo.Chorus(reverb, depth=.5, feedback=0.5, bal=0.5, mul=1).out()
# distort  = pyo.Disto(chorus)
eq       = pyo.MultiBand(chorus, num=3, mul=[1,1,1])

wet      = pyo.Mix([eq], mul=2)
wah      = pyo.ButBP(wet, freq=wahfq, q=30, mul=2)
mix      = pyo.Mix([dry, wet, wah]).out()

start_time = time.time()

dry.mul         = 1 - vals[0]
wet.mul         = vals[0] 

delay.setDelay(0)       # 0.25
delay.setCrossfade(0)   # 0.25

reverb.setSize(0)       # 0.5
reverb.setDamp(0)       # 0.5
reverb.setBal(0)        # 0.5

chorus.setDepth(2.5)    
chorus.setFeedback(0.25)
chorus.setBal(0.5)

# distort.setDrive(0.0)   # 0.75
# distort.setSlope(0.0)   # #0.5

wah.mul         = 0
eq.mul          = [0, 0, 0]


s.gui(locals())

# Available effects in the pyo module are:
#   Disto(input, drive=0.75, slope=0.5, mul=1, add=0)[source]
#   Delay(input, delay=0.25, feedback=0, maxdelay=1, mul=1, add=0)
#   SDelay(input, delay=0.25, maxdelay=1, mul=1, add=0)
#   Waveguide(input, freq=100, dur=10, minfreq=20, mul=1, add=0)
#   AllpassWG(input, freq=100, feed=0.95, detune=0.5, minfreq=20, mul=1, add=0)
#   Freeverb(input, size=0.5, damp=0.5, bal=0.5, mul=1, add=0)
#   WGVerb(input, feedback=0.5, cutoff=5000, bal=0.5, mul=1, add=0)
#   Chorus(input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0)
#   Harmonizer(input, transpo=- 7.0, feedback=0, winsize=0.1, mul=1, add=0)
#   FreqShift(input, shift=100, mul=1, add=0)
#   STRev(input, inpos=0.5, revtime=1, cutoff=5000, bal=0.5, roomSize=1, firstRefGain=- 3, mul=1, add=0)
#   SmoothDelay(input, delay=0.25, feedback=0, crossfade=0.05, maxdelay=1, mul=1, add=0)
#   Clip(input, min=- 1.0, max=1.0, mul=1, add=0)
#   Degrade(input, bitdepth=16, srscale=1.0, mul=1, add=0)
#   Mirror(input, min=0.0, max=1.0, mul=1, add=0)
#   Compress(input, thresh=- 20, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, knee=0, outputAmp=False, mul=1, add=0)
#   Gate(input, thresh=- 70, risetime=0.01, falltime=0.05, lookahead=5.0, outputAmp=False, mul=1, add=0)
#   Expand(input, downthresh=- 40, upthresh=- 10, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, outputAmp=False, mul=1, add=0)

