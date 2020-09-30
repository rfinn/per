from pylab import *
import os
from scipy.stats.stats import spearmanr
from scipy.stats import ks_2samp
from scipy.stats import scoreatpercentile

def ks_boot(x,y,N=1000,conf_int=68.):
    boot_p=zeros(N,'f')
    boot_D=zeros(N,'f')
    for i in range(N):
        xboot=x[randint(0,len(x)-1,len(x))]
        yboot=y[randint(0,len(y)-1,len(y))]
        boot_D[i],boot_p[i]=ks_2samp(xboot,yboot)
    return scoreatpercentile(boot_D,per=50),scoreatpercentile(boot_p,per=50) 
def ks(x,y,run_anderson=True):
    #D,pvalue=ks_2samp(x,y)
    D,pvalue=ks_boot(x,y)
    print 'KS Test:'
    print 'D = %6.2f'%(D)
    print 'p-vale = %6.5f (prob that samples are from same distribution)'%(pvalue)
    if run_anderson:
        anderson(x,y)
    return D,pvalue

