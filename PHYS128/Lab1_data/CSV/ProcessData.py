#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def ReadFile(infile):
	read = open(infile, 'r')
	lines =read.readlines()
	read.close()
	return(lines)

def VelocityUncertainty(h, dh, g):
	dv = ((2*g)/h)**(0.5)*dh
	return round(dv, 3)

def HeightUncertainty(v0, dv0, t, g):
	dv = (t/2)*dv0
	dt = ((v0/2)-g*t*(1/4))*0.001
	dh = (dv**2+dt**2)**(0.5)
	return round(dh, 3)

def EpUncertainty(v0, dv0, vf, dvf):
	ddv0=vf*dv0
	ddvf = (1/v0)*dvf
	dcr = (ddv0**2+ddvf**2)**(0.5)
	return round(dcr, 3)
### Process Raw Data
data = {}
keys = []
for i in range(1, 11):
	key = "Exp_"+str(i)
	keys.append(key)
	raw = ReadFile(key+".csv")
	raw = raw[1:]
	times = [key, 0 , 0 , 0 , 0, 0]
	for j in range(len(raw)):
		event = raw[j].split(',')
		t = event[0].strip()
		t = round(float(t), 3)
		times[j+1] = t
	data.update({key:times})
raw_headers=["Run", "Event 0", "Event 1", "Event 2", "Event 3", "Event 4"]
raw_data = []
for i in keys:
	raw_data.append(data[i])
"""
Get height and epsilon data
v_0 = sqrt(2gh_0)
h_i = v_(i-1)((t/2)-0.5g(t/2)^2
v_i = sqrt(2gh_i)
e_i = v_i/v_0
uncertainties propogated as function of variables for independent random errors/power, propogated accordingly

"""

height_headers = ["Run", "Bounce 1", "Bounce 2", "Bounce 3", "Bounce 4", "Bounce 5"]
height_data = []
height_uncert = []
g = 9.806
dg = 0
h0 = 1.0160
dh = 0.0005

e = str('\u03B5')
epsilon_headers = ["Run", e + "1", e + "2", e+"3", e+"4"] 
v0 = (2*g*h0)**(0.5)
dv0 = VelocityUncertainty(h0, dh, g)
velocity_data = []
epsilon_data = []
velocity_uncert = []
epsilon_uncert=[]

ALL_E = []

for i in raw_data:
	hd = [0, 0, 0, 0, 0, 0]
	u_hd = [0, 0, 0, 0, 0, 0]
	ed = [0, 0, 0, 0, 0]
	u_ed = [0, 0, 0, 0, 0]
	vd = [0, 0, 0, 0, 0]
	u_vd = [0, 0, 0, 0, 0]
	vf = v0
	for j in range(len(i)-1):
		if j == 0:
			hd[j] = i[j]
			vd[j] = i[j]
		else:
			if i[j+1] != 0:
				interval = i[j+1] - i[j]
				peak = interval/2
				bh = vf*peak -0.5*g*peak**2
				dbh = HeightUncertainty(v0, dv0, interval, g)
				vf = (2*g*bh)**(0.5)
				dvf = VelocityUncertainty(bh, dbh, g)
				cr = vf/v0
				dcr = EpUncertainty(v0, dv0, vf, dvf)
				if float(cr) != 0:
					ALL_E.append(cr)
				u_hd[j] = dbh
				u_ed[j] = dcr
				u_vd[j] = dvf
				hd[j] = format(bh, '.3f')
				vd[j] = format(vf, '.3f')
				ed[j] = format(cr, '.3f')
	height_data.append(hd), height_uncert.append(u_hd)
	velocity_data.append(vd), velocity_uncert.append(u_vd)
	epsilon_data.append(ed), epsilon_uncert.append(u_ed)

def MakeTable(headers, data, uncert, title):
	Table=[]
	for i in range(0,len(data)):
		nl = [str(i+1)]
		set = data[i]
		un = uncert[i]
		for j in range(1, len(set)):
			val = set[j]
			u = un[j]
			if u ==0:
				u = 0.001
			full = str(val) + r'$\pm$' + str(u)
			if val == 0:
				full = "N/A"
			nl.append(full)
		Table.append(nl)
	fig = plt.figure(dpi=80)
	ax = fig.add_subplot(1,1,1)
	table = ax.table(cellText=Table, colLabels=headers, loc='center')
	table.auto_set_font_size(False)
	table.set_fontsize(12)
	plt.title(title)
	ax.axis('off')
	plt.show()
h1, h2, h3, h4 = [], [], [], []
def NonZeroIndex(a):
	count = 0
	for i in a:
		if i != 0:
			count = count + 1
	return int(count)

for i in height_data:
	h1.append(float(i[1]))
	h2.append(float(i[2]))
	h3.append(float(i[3]))
	h4.append(float(i[4]))

print(NonZeroIndex(h1))
norm = sum(h1)/NonZeroIndex(h1)

def NormalizedAvg(h, norm):
	mean = sum(h)/NonZeroIndex(h)
	if norm != False:
		mean = mean/norm
	add = 0
	for i in h:
		if norm != False:
			i = i/norm
		add  = add + (i-mean)**2
	N = NonZeroIndex(h)
	std = ((1/(N-1))*add)**(0.5)
	return mean, std

def AvgTable(header, vals, std, title):
	Table = []
	for i in range(len(vals)):
		nl = [i+1, format(vals[i], '.3f'), format(std[i], '.3f')]
		Table.append(nl)
	fig = plt.figure(dpi=80)
	ax = fig.add_subplot(1, 1, 1)
	table = ax.table(cellText=Table, colLabels=header, loc='center')
	table.auto_set_font_size(False)
	table.set_fontsize(12)
	ax.axis('off')
	plt.title(title)
	plt.show()
 
AvgHeights, StdHeights = [], []
use = [h1, h2, h3, h4]

for i in use:
	out = NormalizedAvg(i,norm)
	AvgHeights.append(out[0])
	StdHeights.append(out[1])

AvgHeightHeader = ["Bounce", "Normalized Height", str('\u03c3')]
#AvgTable(AvgHeightHeader, AvgHeights, StdHeights, "Average Height of Each Bounce")

e1, e2, e3, e4 = [], [], [], []
for i in epsilon_data:
	print(i)
	e1.append(float(i[1]))
	e2.append(float(i[2]))
	e3.append(float(i[3]))
	e4.append(float(i[4]))
AvgE_Bounce, StdE_Bounce = [], []
use = [e1, e2, e3, e4]
for i in use:
	out = NormalizedAvg(i, False)
	AvgE_Bounce.append(out[0])
	StdE_Bounce.append(out[1])

AvgE_BounceHeader = ["Bounce", e, str('\u03c3')]
#AvgTable(AvgE_BounceHeader, AvgE_Bounce, StdE_Bounce, "Average " + e+ " of Each Bounce")

AvgE_Run, StdE_Run = [], []
print("epsilon_data:", epsilon_data)
for i in epsilon_data:
	for j in range(len(i)):
		i[j] = float(i[j])
	print(i)
	out = NormalizedAvg(i[1:], False)
	AvgE_Run.append(out[0])
	StdE_Run.append(out[1])
AvgE_RunHeader = ["Run", e, str('\u03c3')]
#AvgTable(AvgE_RunHeader, AvgE_Run, StdE_Run, "Average " + e + " of each Run")

AvgE_Total = sum(ALL_E)/len(ALL_E)
add = 0
for i in ALL_E:
	add = add +(i-AvgE_Total)**2
StdE_Total = ((1/(len(ALL_E)-1))*add)**(0.5)
print("Total e average:", AvgE_Total, "Total e stdev: ", StdE_Total)

#MakeTable(height_headers, height_data, height_uncert, "Height of Bounce (m)")
#MakeTable(epsilon_headers, epsilon_data, epsilon_uncert, "Coefficient of Restitution of Bounce ("+str(e)+")")

"""
plot
ideal fit by average e --> h = e^2h0
"""

bounces = [1, 2, 3, 4]
ideal = [1]
e_sqr = AvgE_Total**2
for i in range(len(bounces)-1):
	ideal.append(ideal[i]*e_sqr)
print("Hegihts:", AvgHeights, StdHeights)
plt.plot(bounces, ideal, label= r'$h=\epsilon^{2}h_{0}$')
plt.errorbar(bounces, AvgHeights, yerr=StdHeights, label="Data", capsize=5)
plt.locator_params(axis="both", integer=True, tight=True)
plt.margins(0.05)
plt.tight_layout()
plt.show()
