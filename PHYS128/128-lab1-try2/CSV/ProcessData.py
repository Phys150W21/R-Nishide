#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
l = 7
def ReadFile(infile):
	read = open(infile, 'r')
	lines =read.readlines()
	read.close()
	return(lines)

def VelocityUncertainty(h, dh, g):
	dv = ((2*g)/h)**(0.5)*dh
	return round(dv, 3)

def HeightUncertainty(t, g):
	dh = (1/4)*g*t*0.001
	return round(dh, 3)

def eeUncert(hi, hb, dhi, dhb):
	a = (1/2)*(hb*hi)**(-1/2)*dhi
	b = (1/2)*(hi)**(1/2)*(hb)*(-3/2)*dhb
	u = (a**2+b**2)**(1/2)
	return round(u, 3)

def EpUncertainty(v0, dv0, vf, dvf):
	ddv0=vf*dv0
	ddvf = (1/v0)*dvf
	dcr = (ddv0**2+ddvf**2)**(0.5)
	return round(dcr, 3)
### Process Raw Data
data = {}
keys = []
for i in range(1, 14):
	key = "Exp_"+str(i)
	keys.append(key)
	raw = ReadFile(key+".csv")
	raw = raw[1:]
	times = [key, 0 , 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0]
	for j in range(len(raw)):
		event = raw[j].split(',')
		t = event[0].strip()
		t = format(float(t), '.3f')
		times[j+1] = t
	data.update({key:times})
raw_headers = ["Run"]
for i in range(l+1):
	raw_headers.append("Impact " + str(i + 1))

raw_data = []
for i in keys:
	raw_data.append(data[i])

def Table(headers, data, title):
	Table=[]
	for i in range(0,len(data)):
		nl = ["Run " + str(i+1)]
		set = data[i]
		for j in range(1, 9):
			val = set[j]
			if val == 0:
				full = "N/A"
			else:
				full = val
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
#Table(raw_headers, raw_data, "Raw time data, " + r'$\delta$' +"t=0.001 s")
"""
Get height and epsilon data
v_0 = sqrt(2gh_0)
h_i = v_(i-1)((t/2)-0.5g(t/2)^2
v_i = sqrt(2gh_i)
e_i = v_i/v_0
uncertainties propogated as function of variables for independent random errors/power, propogated accordingly

"""

height_headers = ["Run"]
for i in range(1, l+1):
	height_headers.append("Bounce " + str(i))
height_data = []
height_uncert = []
g = 9.806
dg = 0
h0 = 1.000
dh = 0.0005

e = str('\u03B5')
epsilon_headers = ["Run"]
for i in range(1, l+1):
	epsilon_headers.append(e+str(i))
v0 = (2*g*h0)**(0.5)
dv0 = VelocityUncertainty(h0, dh, g)
velocity_data = []
epsilon_data = []
velocity_uncert = []
epsilon_uncert=[]

def emptyList(l):
	list = [None]*(l+1)
	for i in range(len(list)):
		list[i] = 0
	return list 
ALL_E = []
ALL_Eu = []
for i in raw_data:
	hd = emptyList(l)
	u_hd = emptyList(l)
	ed = emptyList(l)
	u_ed = emptyList(l)
	vd = emptyList(l)
	print("vd", vd)
	u_vd = emptyList(l)
	vf = v0
	vi = v0
	for j in range(l+1):
		if j == 0:
			hd[j] = i[j]
		else:
			if i[j+1] != 0:
				print(i, j)
				interval = float(i[j+1]) - float(i[j])
				if interval <0:
					continue
				bh = (1/8)*g*interval**2
				dbh = HeightUncertainty(interval, g)
				u_hd[j] = dbh
				hd[j] = format(bh, '.3f')
	print("hd:", hd)
	for k in range(1, len(hd)):
		print(hd[k])
		if k == 1:
			ee = float(hd[k])/h0
		else:
			ee = (float(hd[k])/float(hd[k-1]))**(1/2)
			if ee != 0:
				ALL_E.append(ee)
				ed[k] = format(ee, '.3f')
				uue = eeUncert(float(hd[k]), float(hd[k-1]), u_hd[k], u_hd[k-1])		
				u_ed[k] = uue
				ALL_Eu.append(uue)
	height_data.append(hd), height_uncert.append(u_hd)
	epsilon_data.append(ed), epsilon_uncert.append(u_ed)

print("epsilon_data", epsilon_data, epsilon_uncert)
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
MakeTable(height_headers, height_data, height_uncert, "Height of Bounce (m)")
MakeTable(epsilon_headers, epsilon_data, epsilon_uncert, "Coefficient of Restitution of Bounce ("+str(e)+")")
h1, h2, h3, h4, h5, h6, h7= [],[],[],[],[],[], []
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
	h5.append(float(i[5]))
	h6.append(float(i[6]))
	h7.append(float(i[7]))

print(NonZeroIndex(h1))
norm = sum(h1)/NonZeroIndex(h1)


def NormalizedAvg(h, norm):
	mean = sum(h)/NonZeroIndex(h)
	if norm != False:
		mean = mean/norm
	add = 0
	for i in h:
		if i ==0:
			continue
		if norm != False:
			i = i/norm
		add  = add + (i-mean)**2
	N = NonZeroIndex(h)
	std = ((1/(N-1))*add)**(0.5)
	return mean, std

def AvgTable(header, vals, std, title, *args):
	Table = []
	for i in range(len(vals)):
		if args == True:
			k = i +1
		else:
			k = i
		nl = [k+1, format(vals[i], '.3f'), format(std[i], '.3f')]
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
use = [h1, h2, h3, h4, h5, h6, h7]

for i in use:
	out = NormalizedAvg(i, False)
	AvgHeights.append(out[0])
	StdHeights.append(out[1])

AvgHeightHeader = ["Bounce", "Height", str('\u03c3')]
AvgTable(AvgHeightHeader, AvgHeights, StdHeights, "Average Height of Each Bounce")

e2, e3, e4, e5, e6, e7= [], [], [], [],[], []
for i in epsilon_data:
	print(i)
	e2.append(float(i[2]))
	e3.append(float(i[3]))
	e4.append(float(i[4]))
	e5.append(float(i[5]))
	e6.append(float(i[6]))
	e7.append(float(i[7]))
AvgE_Bounce, StdE_Bounce = [], []
use = [e2, e3, e4, e5, e6, e7]
for i in use:
	out = NormalizedAvg(i, False)
	AvgE_Bounce.append(out[0])
	StdE_Bounce.append(out[1])

AvgE_BounceHeader = ["Bounce", e, str('\u03c3')]
AvgTable(AvgE_BounceHeader, AvgE_Bounce, StdE_Bounce, "Average " + e+ " of Each Bounce", True)

AvgE_Run, StdE_Run = [], []
print("epsilon_data:", epsilon_data)
for i in epsilon_data:
	print("epsilon_data i: ", i)
	for j in range(len(i)):
		i[j] = float(i[j])
	out = NormalizedAvg(i[1:], False)
	AvgE_Run.append(out[0])
	StdE_Run.append(out[1])

AvgE_RunHeader = ["Run", e, str('\u03c3')]

AvgE_Total = sum(ALL_E)/len(ALL_E)
add = 0
for i in ALL_E:
	add = add +(i-AvgE_Total)**2
StdE_Total = ((1/(len(ALL_E)-1))*add)**(0.5)
StdMeanE_Total = StdE_Total*(1/(len(ALL_E)**2))
print("Total e average:", AvgE_Total, "Total e stdev: ", StdE_Total, "StdMeanE_Total: ", StdMeanE_Total)
propogate_total = 0
for i in ALL_Eu:
	propogate_total = propogate_total + i**2

total_err = (propogate_total)**(1/2)
print(total_err)
sys.exit()

AvgTable(AvgE_RunHeader, AvgE_Run, StdE_Run, "Average " + e + " of each Run")

"""
plot
ideal fit by average e --> h = e^2h0
"""
fig, ax =plt.subplots()

bounces = [1, 2, 3, 4, 5, 6, 7]
ideal = [1]
e_sqr = AvgE_Total**2

for i in range(len(bounces)-1):
	ideal.append(ideal[i]*e_sqr)

x = np.linspace(0, 7.5, 1000)
y = np.zeros(len(x))
fit = np.zeros(len(x))
fit[0]=1
for i in range(1, len(x)):
	fit[i] = AvgE_Total**(2*i-2)


for i in range(len(AvgHeights)):
        print(AvgHeights, norm)
        AvgHeights[i] = AvgHeights[i]/norm
	
def parabola(x, y, height, count):
	print(len(x), len(y))
	for i in range(len(x)):
		val = x[i]
		coeff = -1*height*4
		xterm = (x[i] - float(count))
		a = coeff*xterm*xterm + height
		y[i] = a
	return y
upperH = []
lowerH=[]
for i in range(len(AvgHeights)):
	H = AvgHeights[i]
	tolerance = StdHeights[i]
	upperH.append(H+tolerance)
	lowerH.append(H-tolerance)
print(upperH, lowerH)
for i in (range(len(ideal))):
	ax.plot(x, parabola(x, y, ideal[i], bounces[i]), color="red")
	#ax.fill_between(x, 0, parabola(x, y,ideal[i], bounces[i]), facecolor='red', alpha=0.15)
	ax.plot(x,parabola(x, y, AvgHeights[i], bounces[i]), color='blue')
#	ax.fill_between(x, parabola(x, y, AvgHeights[i], bounces[i]), parabola(x, y, upperH[i], bounces[i]), facecolor='yellow')
yer = np.zeros(len(ideal))
for i in range(len(yer)):
	yer[i] = StdE_Total
norm = max(AvgHeights)
for i in range(len(AvgHeights)):
	print(AvgHeights, norm)
	AvgHeights[i] = AvgHeights[i]/norm
#plt.errorbar(bounces, ideal, yerr=ideal_err, label= r'$h=\epsilon^{2}h_{0}$',	capsize=5,color="red", fmt='.')
plt.scatter(bounces, ideal, label = r'$h=\epsilon^{2}h_{0}$', color="red")
#plt.plot(x, fit, label=r'$h_i=\epsilon^{(2i-2)}$', color ="red")
plt.errorbar(bounces, AvgHeights, yerr=StdHeights, label="Height Data, "+ '\u03c3' + " error bars", capsize=2,color="blue", fmt='.')
plt.locator_params(axis="both", integer=True, tight=True)
plt.ylabel("Normalized Height")
plt.legend()
plt.rcParams.update({'font.size': 35})
plt.xlabel("Bounce Number")
plt.ylim(0, 1.1)
plt.margins(0.05)
plt.tight_layout()
plt.show()

xg= np.linspace(0, 1.1, 1000)
def FitGauss(x, mean, std, mh):
	mean = float(mean)
	std = float(std)
	coeff = (2*(355/113)*std*std)**(-0.5)
	y = np.zeros(len(x))
	for i in range(len(x)):
		exp = -(1/2)*(x[i]-mean)*(x[i]-mean)*(1/(std**2))
		y[i] = coeff*2.718**exp
	if mh != False:
		norm = max(y)
		for i in range(len(x)):
			y[i] = y[i]*(1/norm)*mh
	return y
import statistics
fig1, axs1 = plt.subplots(7, sharex=True, gridspec_kw={'hspace':0})
fig1.suptitle("Histogram: " + e +" per Bounce over 13 Runs")
for i in range(6):
	dat = []
	txt = "Bounce " + str(i+2) + "\n" + r'$\overline{\epsilon}$'+"="+str(format(AvgE_Bounce[i], '.3f'))+"\n"+r'$\sigma$' + "=" + str(format(StdE_Bounce[i], '.3f'))
	print(txt)
	fig1.text(0.2, 0.9-(0.11*(i+1)), txt, fontsize=12)
	counts, edges, plot = axs1[i].hist(use[i], bins =3, label = "Bounce " + str(i+2))
	axs1[i].plot(xg, FitGauss(xg, AvgE_Bounce[i], StdE_Bounce[i], max(counts)), color="red")
	axs1[i].set_yticklabels([])
axs1[6].plot(xg, FitGauss(xg, AvgE_Total, StdE_Total, 1), color="red")
txt = r'$\overline{\epsilon}_{total}$'+"="+str(format(AvgE_Total, '.3f'))+"\n"+r'$\sigma_{total}$' + "=" + str(format(StdE_Total, '.3f'))
fig1.text(0.8, 0.16, txt, fontsize=12)
plt.yticks([])
plt.xlim(min(ALL_E)-0.1, max(ALL_E)+0.15)
plt.xlabel(e + " value")
plt.show()

use = [h1, h2, h3, h4, h5, h6]

fig2, axs2 = plt.subplots(6, sharex=True, gridspec_kw={'hspace':0})
fig2.suptitle("Histogram: Bounce Height (" + r'$h_{0} = 1.000 m$' + ")")
plt.xlabel("Height of Bounce (m)")
for i in range(6):
	dat = []
	txt = "Bounce " + str(i+1) + "\n" + r'$\overline{\epsilon}$'+"="+str(format(AvgHeights[i], '.3f'))+"\n"+r'$\sigma$' + "=" + str(format(StdHeights[i], '.3f'))
	print(txt)
	fig2.text(0.8, 0.9-(0.127*(i+1)), txt, fontsize=12)
	counts, edges, plot = axs2[i].hist(use[i], bins =3, label = "Bounce " + str(i+1))
	axs2[i].plot(xg, FitGauss(xg, AvgHeights[i], StdHeights[i], max(counts)), color="red")
	axs2[i].set_yticklabels([])
plt.yticks([])
plt.show()


input("Press Enter to escape")
