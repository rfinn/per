#!/usr/bin/env python

import numpy as np

from stat_tests import *

dat = np.loadtxt('EMCAvsBEMA.csv',skiprows=1,delimiter=',')
flag = dat[:,1] >= 0
spearman(dat[:,0][flag],dat[:,1][flag])
