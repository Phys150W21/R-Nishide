#!/usr/bin/env python3
# Make standard monitoring plots for the passed run number
# We read all the data in and then make standard plots and write them out as png files.
# We also prepare the html file to display them as we go.
# This is designed to be called either at the end of a run to make summary plots, or even during the run for progress monitoring.

import math
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')  # Force matplotlib not try to use an X server
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import sys
import os

if len(sys.argv) < 2:
    print("You need to pass the run number")
    exit()
    
RunNum = int(sys.argv[1])

# Read in the counts per minute lines and plot that.
# The minutes file is written with this command:
#   print(nMinutes,nMinuteCount, file=minutesOut, end="\n")
# We pull out only the second column which is the counts per minute
minutesfile = "/home/pi/150/data/Run"+sys.argv[1]+"/minutesrates.dat"
minutes_f = open(minutesfile, "r")
counts_per_minute = [] # Counts measured in one minute blocks
minCountsPerMinute = 9999.
maxCountsPerMinute = 0.
nMinutes = 0
for line in minutes_f:
    currentline=np.array(line.split(" "))
    nCounts = float(currentline[1]) 
    counts_per_minute.append(nCounts)
    if nCounts > maxCountsPerMinute:
        maxCountsPerMinute = nCounts
    if nCounts < minCountsPerMinute:
        minCountsPerMinute = nCounts
    nMinutes = nMinutes + 1
minutes_f.close()

# Fit the counts per minute to a gaussian
mean,std=norm.fit(counts_per_minute)

# Make a histogram of the counts per minute
plt.figure(1)
bins=np.arange(minCountsPerMinute,maxCountsPerMinute,5)
print("bins pre-patch CPM:", bins)
if len(bins)  < 2: 
  bins = [1, 2, 3, 4, 5]
print("bins post-patch CPM:", bins)
plt.hist(counts_per_minute, bins = bins, histtype = 'step', linestyle=('solid'), linewidth=3, color='blue')
plt.grid()
plt.title('Histogram of counts per minute during the run')
plt.yscale("linear")
plt.ylabel('Number of events per bin')
plt.xlabel('Counters per minute')
plt.savefig("/home/pi/150/data/Run"+sys.argv[1]+"/countsperminute.png")

# Now read the events lines and plot the rate vs time and time between events
# Define the arrays used to build the histograms
time_minutes = [] # Minutes since start of run
max_minutes = 0.
time_btwn_events = [] # Seconds since previous event
max_time_btwn_events = 0.

# Read in the event lines and split them into arrays.
# The data file is written with this command:
#    print(nCount,timeSinceRunStart.total_seconds(), timeSincePrevEvent.total_seconds(), currentTime.year, currentTime.month, currentTime.day, currentTime.hour, currentTime.minute, currentTime.second, currentTime.microsecond, ADC1, ADC2, AUX1, AUX2, AUX3, file=eventsOut, end="\n")
# We pull out only the second column which is the time since start of run.
eventsfile = "/home/pi/150/data/Run"+sys.argv[1]+"/events.dat"
f = open(eventsfile, "r")
for line in f:
    currentline=np.array(line.split(" "))
    evttime_sec = float(currentline[1])  # Time since start of run; Units=seconds
    evttime_min = evttime_sec/60.; # Convert to minutes
    time_minutes.append(evttime_min) 
    if evttime_min>max_minutes:
        max_minutes = evttime_min
    timediff = float(currentline[2])  # Time since previous event; units=seconds
    time_btwn_events.append(timediff)
    if timediff > max_time_btwn_events:
        max_time_btwn_events = timediff
f.close()

# Make a histogram of the event time from start of run
plt.figure(2)
bins=np.arange(0.,max_minutes,1)
print("bins pre-patch CPM:", bins)
if len(bins)  < 2: 
  bins = [1, 2, 3, 4, 5]
print("bins post-patch CPM:", bins)
plt.hist(time_minutes, bins = bins, histtype = 'step', linestyle=('solid'), linewidth=3, color='blue')
plt.grid()
plt.title('Time distribution of counts throughout run')
plt.yscale("linear")
plt.ylabel('Number of events per minute')
plt.xlabel('Time [Minutes]')
plt.savefig("/home/pi/150/data/Run"+sys.argv[1]+"/timedist.png")

# Make a histogram of the time between events
plt.figure(3)
bins=np.arange(0.,max_time_btwn_events,0.1)
print("bins pre-patch CPM:", bins)
if len(bins)  < 2: 
  bins = [1, 2, 3, 4, 5]
print("bins post-patch CPM:", bins)
plt.hist(time_btwn_events, bins = bins, histtype = 'step', linestyle=('solid'), linewidth=3, color='blue')
plt.grid()
plt.title('Live time between events')
plt.yscale("log")
plt.ylabel('Number of events per bin')
plt.xlabel('Live time between events [seconds]')
plt.savefig("/home/pi/150/data/Run"+sys.argv[1]+"/timediff.png")

# Add the plots files to the web page; they will be generated below.
webfile = "/home/pi/150/data/Run"+sys.argv[1]+"/plots.html"
webOut = open(webfile, "w")
print('<IMG WIDTH=30% SRC="timedist.png">',file=webOut)
print('<IMG WIDTH=30% SRC="countsperminute.png">',file=webOut)
print('<IMG WIDTH=30% SRC="timediff.png">',file=webOut)
print('<P>Counts per minute distribution has mean = %.2f &plusmn; %.2f and standard deviation = %.2f' % (mean,std/math.sqrt(nMinutes),std),file=webOut)
print('<P><HR>',file=webOut)
webOut.close()
