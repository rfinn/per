#!/usr/bin/env python
from scipy.stats.stats import spearmanr
from scipy.stats import ks_2samp
from anderson import *


def spearman(x,y):
    rho,pvalue=spearmanr(x,y)
    print 'Spearman Rank Test:'
    print 'rho = %6.2f'%(rho)
    print 'p-vale = %6.5e (prob that samples are uncorrelated)'%(pvalue) 
    return rho,pvalue

def ks(x,y):
    D,pvalue=ks_2samp(x,y)
    print 'KS Test:'
    print 'D = %6.2f'%(D)
    print 'p-vale = %6.5e (prob that samples are from same distribution)'%(pvalue) 
    return D,pvalue

def anderson(x,y):
    t=anderson_ksamp([x,y])
    print 'Anderson-Darling test Test:'
    print 'D = %6.2f'%(t[0])
    print 'p-vale = %6.5e (prob that samples are from same distribution)'%(t[2]) 
    return t[0],t[2]
