#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:12:05 2022

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

def isogloss(hash_v, frequency):
    
    iso = 2*hash_v*frequency*(1-frequency)
    return iso
    

rho_01 = [0, 0.248, 0.502, 0.752, 1]
iso_01 = [0, 0.241, 0.322, 0.240, 0]
rho_1 = [0, 0.251, 0.501, 0.750, 1]
iso_1 = [0, 0.324, 0.432, 0.324, 0]
freqs = np.linspace(0,1,10000)
fit_01 = fitting_tau_and_hash(0.1)
fit_1 = fitting_tau_and_hash(1)

fig, ax = plt.subplots()
plt.xlabel("Frequency of Features")
plt.ylabel("Isogloss Density")
plt.title("Frequency of Features against Isogloss Desity")

plt.plot(rho_01, iso_01, "o", label="Tau = 0.1") 
plt.plot(rho_1, iso_1, "x", label="Tau = 1")
plt.plot(freqs, isogloss(fit_01, freqs), "-")
plt.plot(freqs, isogloss(fit_1, freqs), "-")
plt.legend(loc=0)
plt.savefig("Results_graph", dpi=300)
plt.show()