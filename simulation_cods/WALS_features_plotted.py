#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:44:59 2022

@author: qinohr
"""


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import matplotlib.collections as mc
from scipy import interpolate
import imageio
import os

def fitting_tau_and_hash(tau_point):
    opened_data = pd.read_csv("tau_hash.csv", header=None)
    tau = opened_data[0]
    hash_d = opened_data[1]
    #new_tau = np.linspace(0.0000000999999999999999,1000,100000)
    #fig, ax = plt.subplots()
    fit = interpolate.interp1d(tau, hash_d, kind = 'cubic')
    #plt.plot(tau,hash_d, "o", new_tau, fit(new_tau), "-")
    #plt.show()
    return float(fit(tau_point))

def reverse_fit(hash_point):
    
    opened_data = pd.read_csv("tau_hash.csv", header=None)
    tau = opened_data[0]
    hash_d = opened_data[1]
    #new_tau = np.linspace(0.0000000999999999999999,1000,100000)
    #fig, ax = plt.subplots()
    fit = interpolate.interp1d(hash_d, tau, kind = 'cubic')
    #plt.plot(tau,hash_d, "o", new_tau, fit(new_tau), "-")
    #plt.show()
    return float(fit(hash_point))

def isogloss(hash_v, frequency):
    
    iso = 2*hash_v*frequency*(1-frequency)
    return iso

def hash_form(freq, isogloss):
    top = isogloss
    bottom = 2*freq*(1-freq)
    return top/bottom

#WALS: 130A, 37A, 77A, 48A
rho_01 = [0.12142, 0.60806, 0.45337, 0.83333]
iso_01 = [0.18876, 0.36313, 0.32420, 0.20930]
WALS = ["130A", "37A", "120A", "48A"]

taus = np.linspace(0.1, 1.5, 15)
freqs = np.linspace(0,1,1000)

fig, ax = plt.subplots()
plt.xlabel("Frequency of Features")
plt.ylabel("Isogloss Density")
plt.title("Frequency of Features against Isogloss Desity with WALS Features")

for n in range(len(rho_01)):

    plt.plot(rho_01[n], iso_01[n], "x", color="black", zorder=1, label=WALS[n]) 

for x in range(len(taus)):
    plt.plot(freqs, isogloss(fitting_tau_and_hash(taus[x]),freqs), "-",zorder=-1)
    
for i in range(len(WALS)):
    #ax.annotate(WALS[i], (rho_01[i], iso_01[i]))
    h = hash_form(rho_01[i], iso_01[i])
    tau = "{:.3f}".format(reverse_fit(h))
    print(tau)
    ax.annotate(str(tau) +" " + "WALS ID: " + WALS[i], (rho_01[i], iso_01[i]), zorder=1)

plt.savefig("WALS_features", dpi=300)
plt.show()

