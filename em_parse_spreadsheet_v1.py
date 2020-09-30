#!/usr/bin/env python

'''
   GOAL:
    read in xlsx version of answers that is downloaded from google forms
    
   PROCEDURE:
    - download file from google drive
    - save as csv file, using naming convention:
      Electromagnetism-Assessment-Post-PHYS140.01M.S15-Finn.csv
    - run code 
   USAGE:

   REQUIRED MODULES:
     xlrd
   
   UPDATES:
     - Written by Rose Finn on June 3, 2015

    
create a class for student that contains
- email
- answers to pre-test
- binary array of pre-test score (0/1 for each question)
- answers to post-test
- binary array of post-test score (0/1 for each question)
- hake score
- instructor


Need:
- post-score
- hake score
- item analysis
  - 
     
'''
import sys
import glob
import numpy as np
import pylab as pl

#correct_answers=np.array(['c', 'e', 'a', 'e', 'e', 'b', 'a', 'a', 'b', 'a', 'a', 'c', 'd','c', 'b', 'c', 'a', 'a', 'a', 'e', 'e', 'b', 'd', 'c', 'd', 'b','d', 'b', 'e', 'c'])

correct_answers=np.array(['a','d','d','b','c','b','a','b','b','a','a','c','d','c','b','a','b','b','a','b','a','c','a','a','a','c','c','d','b','a'])
correct_answers=np.array(['c','e','d','e','c','b','a','b','b','a','a','c','d','c','b','a','b','b','a','e','d','c','d','c','d','a','d','b','e','c'])
mchoices=['a','b','c','d','e']
def countabc(x):
    count=np.zeros(len(mchoices),'f')
    for i in range(len(mchoices)):
        count[i]=np.sum(x == mchoices[i])
    return count

def histabc(x,normflag=False): # feed in array of letter choices, assuming a-e
    count=countabc(x)
    if normflag:
        count=count/(1.*len(x))
    #pl.figure()
    w=0.8 # width of the bar
    pl.bar(np.arange(len(count))-.5*w,count,width=w)
    pl.xticks(np.arange(len(count)),mchoices)
    pl.xlim(-.5,len(count)-.5)
def plot_correctchoice(i):
    t=correct_answers[i]
    if t == 'a':
        xloc=0
    elif t == 'b':
        xloc=1
    elif t == 'c':
        xloc=2
    elif t == 'd':
        xloc = 3
    elif t == 'e':
        xloc = 4
    try:
        pl.axvline(xloc,color='r')
    except UnboundLocalError:
        print 'could not find match for ',i
    
def readcsv(file):
    infile=open(file,'r')
    dat=[]
    for line in infile:
        dat.append(line.split(','))
    infile.close()
    return dat

def readtsv(file):
    infile=open(file,'r')
    dat=[]
    for line in infile:
        #print line.split('\t')
        dat.append(line.rstrip().split('\t'))
    infile.close()
    return dat

def make2darray(dat):
    #darray=np.zeros((len(dat),len(correct_answers)),dtype='|S1')
    temp=[]
    for i in range(len(dat)):
        #print len(dat[i][3:33]),dat[i][3:33]
        #print len(darray[i,:])
        #darray[i,:]=np.array(dat[i][3:33])
        temp.append(dat[i][4:34])
    return np.array(temp)

def transform_array(darray): # convert character array into binary array
    i=0
    binary_data=np.zeros(darray.shape,'f')
    print binary_data.shape
    for i in range(len(darray)):
        binary_data[i]=darray[i] == correct_answers
    return binary_data

class emdata():
    def __init__(self,fstring):
        self.match_string = fstring
        self.read_predat()
        self.read_postdat()
        self.match_prepost()
        self.cull_sample()
        self.flag140=(self.predat_array[:,2] == '140')
        self.calculate_hake()
    def read_predat(self):
        match_this = '*Pre'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this
        files=glob.glob(match_this)
        print 'found these'
        print files
        predat=[]
        for f in files:
            t=readtsv(f)
            #print t
            predat=predat+t[1:] # omit header row
        #print predat
        self.predat=predat
        self.pre_darray=make2darray(predat)

        self.predat_array=np.array(predat)
        self.pre_binary=transform_array(self.pre_darray)
    def read_postdat(self):
        files=glob.glob('*Post-*'+self.match_string+'*.tsv')
        postdat=[]
        for f in files:
            t=readtsv(f)
            postdat=postdat+t[1:] # omit header row
        self.postdat=np.array(postdat)
        self.post_darray=make2darray(postdat)
    def match_prepost(self):
        # find matches between pre and post data using student email id

        post_sid_dict=dict((a,b) for a,b in zip(self.postdat[:,1],np.arange(len(self.postdat[:,1]))))
        self.prepostmatch=np.zeros(len(self.predat),'bool')
        i=0
        self.postdatsort=np.zeros(self.predat_array.shape,dtype=self.predat_array.dtype)
        for name in self.predat_array[:,1]:
            try:
                j = post_sid_dict[name]
                self.prepostmatch[i] = True
                #print self.postdat[j]
                #print self.postdatsort[j]
                self.postdatsort[i,:] = self.postdat[j]
            except KeyError:
                self.prepostmatch[i]=False
                print 'no post-test match for ',name
            i += 1
        self.post_darray=make2darray(self.postdatsort)
        self.post_binary=transform_array(self.post_darray)
        
    def cull_sample(self): # only keep students that took pre and post tests
        self.pre_darray=self.pre_darray[self.prepostmatch] # answers to questions
        self.pre_binary = self.pre_binary[self.prepostmatch] # binary score to questions
        self.predat_array=self.predat_array[self.prepostmatch] # entire data array
        self.post_darray=self.post_darray[self.prepostmatch]
        self.post_binary=self.post_binary[self.prepostmatch]
        self.postdat_array=self.postdatsort[self.prepostmatch]

    def calculate_hake(self):
        self.pre_score=np.sum(self.pre_binary,axis=1)
        self.post_score=np.sum(self.post_binary,axis=1)
        self.hake=(self.post_score-self.pre_score)/(len(correct_answers)-self.pre_score)
    def plot_hake(self):
        self.calculate_hake()
        pl.figure()
        pl.subplots_adjust(hspace=.35)
        pl.subplot(2,1,1)
        pl.hist(self.pre_score,histtype='step',label='Pre-test')
        pl.hist(self.post_score,histtype='step',label='Post-test')
        pl.xlabel('Score (out of 30)',fontsize=16)
        pl.ylabel('Number of Students',fontsize=16)
        pl.legend()
        pl.subplot(2,1,2)
        pl.hist(self.hake)
        pl.xlabel('Hake Score',fontsize=16)
        pl.ylabel('Number of Students',fontsize=16)
    def plotchoices(self,normflag=False):
        nstudent,nquestion=self.post_darray.shape
        nrow=6
        ncol=5
        pl.figure(figsize=(10,12))
        left_edge=[0,5,10,15,20,25]
        pl.subplots_adjust(hspace=.08,wspace=.05,bottom=0.1,left=0.1,right=.9,top=.9)
        for i in range(nquestion):
            pl.subplot(nrow,ncol,i+1)
            histabc(self.post_darray[:,i],normflag=normflag)
            plot_correctchoice(i)
            if normflag:

                ymin=0
                ymax=.8
                ystep=.2
            else:
                ymin=0
                ymax=85
                ystep=20
            pl.ylim(ymin,ymax)
            if i in left_edge:
                pl.yticks(np.arange(ymin,ymax+.5*ystep,ystep))
            else:
                pl.yticks([])
            if i < 25:
                pl.xticks([])
            pl.text(0.5,0.8,'Q'+str(i+1),fontsize=16,transform=pl.gca().transAxes,horizontalalignment='center')
            if normflag:
                pl.axhline(y=0.5,ls='--',color='k')
        pl.savefig('../plots/question_choices.png')
        
if __name__ == "__main__":
    p=emdata('*S15*')

    
# plots for poster
# choice distribution for each question
# item difficulty versus question number
# point biserial coefficient vs question number

# table 

