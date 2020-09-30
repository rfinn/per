
import numpy as np
import pylab as pl
from makeMastertable import *
from astropy.table import Table

class afullsample(fullsample):
    def plot_emhake_sat(self):
        print 'making a plot'
        x=a.mt['SAT']
        y=a.mt['em_hake']
        flag=(a.mt['em_post_match'] == 1) & (a.mt['aux_match'] == 1) & (a.mt['SAT'] != -99.)
        pl.figure()
        pl.plot(x[flag],y[flag],'bo')
    def plot_empost_sat(self):
        print 'making a plot'
        x=a.mt['SAT']
        y=a.mt['em_post_score']
        flag=(a.mt['em_post_match'] == 1) & (a.mt['aux_match'] == 1) & (a.mt['SAT'] != -99.)
        pl.figure()
        pl.plot(x[flag],y[flag],'bo')
    def plot_fcihake_sat(self):
        print 'making a plot'
        flag=(a.mt['fci_post_match'] == 1) & (a.mt['aux_match'] == 1) & (a.mt['SAT'] != -99.)
        x=a.mt['SAT'][flag]
        y=a.mt['fci_hake'][flag]
        pl.figure()
        pl.plot(x,y,'bo')
        spearman(x,y)
    def plot_fcipost_sat(self):
        print 'making a plot'
        flag=(a.mt['fci_post_match'] == 1) & (a.mt['aux_match'] == 1) & (a.mt['SAT'] != -99.)
        x=a.mt['SAT'][flag]
        y=a.mt['fci_post_score'][flag]

        pl.figure()
        pl.plot(x,y,'bo')
        spearman(x,y)
    def plot_emhake_fcihake(self):
        print 'making a plot'
        flag=(a.mt['fci_post_match'] == 1) & (a.mt['em_post_match'] == 1) 
        x=a.mt['fci_hake'][flag]
        y=a.mt['em_hake'][flag]

        pl.figure()
        pl.plot(x,y,'bo')

        rho,p=spearman(x,y)
        ax=pl.gca()
        pl.text(.95,.9,r'$\rho = %4.2f$'%(rho),horizontalalignment='right',transform=ax.transAxes,fontsize=18)
        pl.text(.95,.8,'$p = %5.4f$'%(p),horizontalalignment='right',transform=ax.transAxes,fontsize=18)
        pl.xlabel('$ FCI \ Hake \ Score $',fontsize=20)
        pl.ylabel('$ EM  \ Hake  \ Score $',fontsize=20)
        pl.savefig(PERdir+'plots/EM_FCI_hake.png')
    def plot_emhake_gender(self):
        print 'making a plot'
        pl.figure()
        flag=(a.mt['aux_match'] == 1) & (a.mt['em_post_match'] == 1) & (a.mt['gender'] == 'f')
        x1=a.mt['em_hake'][flag]
        pl.hist(x1,bins=len(x1),color='r',label='Female',histtype='step',cumulative=True,normed=True)
        flag=(a.mt['aux_match'] == 1) & (a.mt['em_post_match'] == 1) & (a.mt['gender'] == 'm')
        x2=a.mt['em_hake'][flag]
        pl.hist(x2,bins=len(x2),color='b',label='Male',histtype='step',cumulative=True,normed=True)

        rho,p=ks(x1,x2)
        anderson(x1,x2)
        ax=pl.gca()
        pl.text(.95,.9,r'$D = %4.2f$'%(rho),horizontalalignment='right',transform=ax.transAxes,fontsize=18)
        pl.text(.95,.8,'$p = %5.4f$'%(p),horizontalalignment='right',transform=ax.transAxes,fontsize=18)
        pl.xlabel('$ EM \ Hake \ Score $',fontsize=20)
        pl.legend(loc='upper left')
        pl.axis([-.4,1.,0.,1.05])
        pl.savefig(PERdir+'plots/EM_hake_gender.png')
        

if __name__ == '__main__':
    a = afullsample()
    a.read_table()
    
