#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:11:18 2022

@author: qinohr
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import os

opened_data = pd.read_csv("tau_hash.csv", header=None)
tau = opened_data[0]
hash_d = opened_data[1]
new_tau = np.linspace(0.0000000999999999999999,1000,100000)
fig, ax = plt.subplots()
fit = interpolate.interp1d(tau, hash_d, kind = 'cubic')
plt.title("Hash function vs Linguistic Temperature (Fitted)")
plt.xlabel("Hash Function H(\u03C4)")
plt.ylabel("Linguistic Temperature \u03C4")
plt.plot(tau,hash_d, "o", new_tau, fit(new_tau), "-")
plt.savefig("HashTau.png", dpi=1000)
plt.show()