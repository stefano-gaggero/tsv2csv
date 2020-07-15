#!/usr/bin/python
#
#In ingresso file TSV del nanodrop (IN_FILE_PATH) con lunghezze d'onda comprese nell'intervallo [FREQ_FROM, FREQ_TO]
#Esegue un fit con una gaussiana nell'intervallo [FREQ_MIN, FREQ_MAX] per stabilire se è presente un picco di assorbimento
#Dal fit viene calcolato sigma^2 
#Se sigma^2<SIGMASQUARE_TRESHOLD si considera presente il picco di assorbimento
#Visualizza grafici (dati + fit) e stampa i nomi dei campioni su cui è presente il picco
#Crea in uscita un file CSV (OUT_FILE_PATH) in cui i campioni sono in colonne diverse
#La prima riga del CSV contiene i valori di sigma^2
#La seconda riga contiene un flag (0,1) che indica la presenza o meno del picco di assorbimento.
#


import sys

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit

STATE_SKIP, _, _, STATE_SPEC_NAME, STATE_SPEC_DATE, _, STATE_DATA = range(7)
FREQ_FROM, FREQ_TO = 190, 840
FREQ_MIN, FREQ_MAX = 390, 430
SIGMASQUARE_TRESHOLD = 500
A_TRESHOLD = 0.05
IN_FILE_PATH = "" #Input file TSV
OUT_FILE_PATH = "" #Output file CSV


def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

spectrum_names = [] 
def func():
	state = STATE_SPEC_NAME
	for line in open(IN_FILE_PATH,"r"):
		if state == STATE_SPEC_NAME: 
			spectrum_names.append(line.strip())
		elif state == STATE_DATA:
			wavelength, absorbance = line.strip().split()
			if int(wavelength) == (FREQ_TO-1):
				state = STATE_SKIP             
				continue                             
			if (int(wavelength)<FREQ_MIN) or (int(wavelength)>=FREQ_MAX):
				continue 
			yield absorbance
			continue
		state += 1
 
#Lettura del file tsv-----------------------------------------              
data = np.fromiter(func(), float)

wavelengths = np.arange(FREQ_MIN, FREQ_MAX)
spectra = data.reshape(len(spectrum_names), FREQ_MAX - FREQ_MIN).transpose()


#Grafico di tutti i campioni-----------------------------------------              
ax = plt.axes(xlim=(FREQ_MIN, FREQ_MAX))
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.minorticks_on
ax.grid(True, which='both')

plt.ylabel("Absorption")
plt.xlabel("Wavelength [nm]")

plt.plot(wavelengths, spectra)
plt.show()


#FIT e grafici-----------------------------------------

ax = plt.axes(xlim=(FREQ_MIN, FREQ_MAX))
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.minorticks_on

sigmas = []
params = []
gaussianFlag = []
m = len(spectrum_names) #numero delle colonne

x = wavelengths
mean = FREQ_MIN + (FREQ_MAX - FREQ_MIN)/2
sigma = FREQ_MAX-mean
n = len(x)              #numero dei dati
for i in range(0,m):
    y = spectra.transpose()[i]  
    a = y[0]
    try:
        popt,pcov = curve_fit(gaus,x,y,p0=[a,mean,sigma])
        ss = popt[2]**2
        sigmas.append(ss);        
        if (ss<SIGMASQUARE_TRESHOLD and a>A_TRESHOLD):
            ax.plot(wavelengths, y, label=spectrum_names[i]) 
            #plt.plot(wavelengths, gaus(x,popt[0],popt[1],popt[2]))  #Grafico del FIT
            gaussianFlag.append(1)
            print("---> " + spectrum_names[i] +  "(ss=" + str(round(ss)) + ", A=" + str(a) + ")")
        else:
            gaussianFlag.append(0)
    except RuntimeError:
        print("warning " + spectrum_names[i])
        sigmas.append(-1);
        gaussianFlag.append(0)
    
ax.grid(True, which='both')    
ax.legend(loc='best')
plt.show()

#Grafico dei sigmas
#ay = plt.axes(ylim=(0, SIGMASQUARE_TRESHOLD))
#plt.plot(range(0,m), sigmas) 
#plt.show()


#Scrittura del file csv-----------------------------------------
A = np.insert(spectra, 0, wavelengths, axis=1)
with open(OUT_FILE_PATH, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel', delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['wavelength'] + spectrum_names)
    writer.writerow(['sigma square'] + sigmas)
    writer.writerow(['gaussian flag'] + gaussianFlag)
    for row in A:
        writer.writerow(row)

