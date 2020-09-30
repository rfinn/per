#!/usr/bin/env python

'''
   GOAL:
    - read in tab-separated files that have been downloaded from google forms
    - convert data into 2-D arrays for further analysis
    
   PREPARING DATA:
    - download file from google drive
    - save as tsv file, using naming convention:
      Electromagnetism-Assessment-Post-PHYS140.01M.S15-Finn.tsv

   PROCEDURE:
   - call class, passing the string to use when globbing files
     e.g.: p = emdata('*S15*') # to read in files from Spring 2015
   - init function
     - reads in pre-test data
     - reads in post-test data
     - matches post-test to pre-test data using student email addresses
     - culls the sample to keep only students with both pre and post test data
      
   USAGE:
    - run from the PER/pythonCode directory
    - in ipython, 
      > %run em_parse_spreadsheet.py
      > e15.plot_hake()
      > e15.plot_choices()
      > f14.plot_hake()
      > f14.plot_choices()

      To print email, pre and post scores:
      
      for i in range(len(f14.pre_score)): print i, f14.predat_array[:,1][i],f14.pre_score[i],f14.post_score[i]

   REQUIRED MODULES:
     numpy
     pylab
     glob
   
   UPDATES:
     - Written by Rose Finn on June 3, 2015

    
Need:
- post-score
- hake score
- item analysis
  - 
     
'''
#import sys
import glob
import numpy as np
import pylab as plt
import os
from stat_tests import *
from astropy.table import Table
#from PERcommon import *

mypath=os.getcwd()
print mypath
if mypath.find('per') > -1:
    t=mypath.split('per')
elif mypath.find('PER') > -1:
    t=mypath.split('PER')
#print mypath.split('PER')

#PERdir=t[0]+'/PER/'
#t=mypath.split('per')
PERdir=t[0]+'PER/'
print 'PER directory is ',PERdir
paperdir = PERdir+'papers/EMCA/submitted/'
#correct_answers=np.array(['c', 'e', 'a', 'e', 'e', 'b', 'a', 'a', 'b', 'a', 'a', 'c', 'd','c', 'b', 'c', 'a', 'a', 'a', 'e', 'e', 'b', 'd', 'c', 'd', 'b','d', 'b', 'e', 'c'])

correct_answers_S14=np.array(['a','d','d','b','c','b','a','b','b','a','a','c','d','c','b','a','b','b','a','b','a','c','a','a','a','c','c','d','b','a'])

# correct answers for Spring 2015
correct_answers=np.array(['c','e','d','e','c','b','a','b','b','a','a','c','d','c','b','a','b','b','a','e','d','c','d','c','d','a','d','b','e','c'])

#questions by subtopic
kinematics = np.array([20,21,23,24,25,7],'i') -1
first_law = np.array([4,6,10,26,27,18,28],'i') -1
second_law = np.array([6,7,24,25],'i') -1
third_law = np.array([2,11,13,14],'i') -1
superposition = np.array([19,9,18,28],'i') -1
contact_force = np.array([9,12,15,29],'i') -1
fluid_force =np.array( [22,12],'i') -1
gravity = np.array([5,9,12,17,18,22],'i') -1
grav_acceleration = np.array([1,3],'i') -1
projectiles = np.array([16,23],'i') -1

topics = [kinematics,first_law,second_law,third_law,
          superposition,contact_force, fluid_force,
          gravity, grav_acceleration, projectiles]
topic_names = ['kinematics','first_law','second_law','third_law',
          'superposition','contact_force', 'fluid_force',
          'gravity', 'grav_acceleration', 'projectiles']


# same as above for EMCA test

conductors = np.array([1,20,25],'i')-1
charge = np.array([4,6,9],'i')-1
coulumbs_law = np.array([2,3,9],'i')-1
gauss_law = np.array([5],'i')-1
electric_field = np.array([6,7,8,25],'i')-1
#force_from_E = np.array([7],'i')-1
electric_pot = np.array([9,10],'i')-1
series = np.array([11,12,13],'i')-1
parallel = np.array([14,15,16],'i')-1
equiv_resistance = np.array([17],'i')-1
resistance = np.array([18,19],'i')-1
current_Bfield = np.array([21,28,29],'i')-1
lorentz_force = np.array([7,22,25,30],'i')-1
magnets = np.array([23],'i')-1
induction = np.array([24],'i')-1
sepcharge = np.array([25],'i')-1
F_on_wire = np.array([26],'i')-1
B_flux = np.array([27],'i')-1
B_field = np.array([28,29],'i')-1

emca_topics = [conductors,
               charge,
               coulumbs_law,
               gauss_law ,
               electric_field ,
               electric_pot ,
               series ,
               parallel ,
               equiv_resistance ,
               resistance ,
               current_Bfield ,
               lorentz_force ,
               magnets ,
               induction,
               sepcharge ,
               F_on_wire ,
               B_flux ,
               B_field ]

emca_topic_names = ['conduct',
               'charge',
               'coulumbs',
               'gauss',
               'E_field',
               'E_pot',
               'series',
               'parallel',
               'eq_resist',
               'resist',
               'current_B',
               'lorentz_F',
               'magnets',
               'induct',
               'sepcharge',
               'F_wire',
               'B_flux',
               'B_field'  ]
infile=PERdir+'FCI/data/FCI-Assessment-Answer_Key.txt'
in1=open(infile,'r')
t=in1.readline()
s=t.split('\t')
fci_correct_answers=np.array(s[0:30])

mchoices=['a','b','c','d','e'] # choices for multiple choice questions (not all have 5 choices)
fci_mchoices=['A','B','C','D','E'] # choices for multiple choice questions (not all have 5 choices)

def calculate_discrimination(binary_scores):
    # get indices for lowest to highest post score
    sorted_index=np.argsort(np.sum(binary_scores,axis=1))
    sorted_answers=binary_scores[sorted_index,:]
    n=len(sorted_index)
    midpoint=len(sorted_index)/2.
    discrim=(np.sum(sorted_answers[n/2:n,:],axis=0)-np.sum(sorted_answers[0:n/2,:],axis=0))/midpoint
    return discrim

#def read_gender():

def countabc(x,mchoices):
    count=np.zeros(len(mchoices),'f')
    for i in range(len(mchoices)):
        count[i]=np.sum(x == mchoices[i])
    return count

def plot_correctchoice(i,flagS14=False,fciflag=False):
    if flagS14:
        t=correct_answers_S14[i]
    elif fciflag:
        t=fci_correct_answers[i]
    else:
        t=correct_answers[i]
    if t in ['a','A']:
        xloc=0
    elif t in ['b', 'B']:
        xloc=1
    elif t in ['c', 'C']:
        xloc=2
    elif t in ['d','D']:
        xloc = 3
    elif t in ['e','E']:
        xloc = 4
    try:
        plt.axvline(xloc,color='c',lw=2)
    except UnboundLocalError:
        print 'could not find match for question',i,' (choice = ',t,')'


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
        dat.append(line.replace('\'','').rstrip().split('\t'))
    infile.close()
    return dat
def readauxtsv(file):
    infile=open(file,'r')
    dat=[]
    for line in infile:
        if line.startswith('#'):
            continue
        dat.append(line.replace('\'','').rstrip().split('\t'))
    infile.close()
    return dat

def make2darray(dat):
    #darray=np.zeros((len(dat),len(correct_answers)),dtype='|S1')
    temp=[]
    for i in range(len(dat)):
        #print len(dat[i][3:33]),dat[i][3:33]
        #print len(darray[i,:])
        #darray[i,:]=np.array(dat[i][3:33])
        temp.append(dat[i][3:33])# fixed to make S15 and S16 consistent
    return np.array(temp)
def make2darrayfci(dat):
    #darray=np.zeros((len(dat),len(correct_answers)),dtype='|S1')
    temp=[]
    for i in range(len(dat)):
        #print len(dat[i][3:33]),dat[i][3:33]
        #print len(darray[i,:])
        #darray[i,:]=np.array(dat[i][3:33])
        temp.append(dat[i][3:33])
    return np.array(temp)


def make2darrayEM2014pre(dat):
    #darray=np.zeros((len(dat),len(correct_answers)),dtype='|S1')
    temp=[]
    for i in range(len(dat)):
        #print len(dat[i][3:33]),dat[i][3:33]
        #print len(darray[i,:])
        #darray[i,:]=np.array(dat[i][3:33])
        temp.append(dat[i][3:33])
    return np.array(temp)

def transform_array(darray,flagS14=False,fciflag=False): # convert character array into binary array
    i=0
    binary_data=np.zeros(darray.shape,'f')
    if fciflag:
        answers=fci_correct_answers
    else:
        if flagS14:
            answers=correct_answers_S14
        else:
            answers=correct_answers
    print binary_data.shape
    for i in range(len(darray)):
        binary_data[i]=darray[i] == answers
    return binary_data

class analysis():
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
        if self.fciflag:
            self.post_darray=make2darrayfci(self.postdatsort)
        else:
            self.post_darray=make2darray(self.postdatsort)
        print 'fciflag = ',self.fciflag
        self.post_binary=transform_array(self.post_darray,flagS14=self.flagS14,fciflag=self.fciflag)

        self.post_score=np.sum(self.post_binary,axis=1)
        self.hake = (self.post_score - self.pre_score)/(30.-self.pre_score)
        
    def match_prepostpost(self):
        # find matches between pre and post data using student email id

        postpost_sid_dict=dict((a,b) for a,b in zip(self.postpostdat[:,1],np.arange(len(self.postpostdat[:,1]))))
        self.prepostpostmatch=np.zeros(len(self.predat),'bool')
        i=0
        self.postpostdatsort=np.zeros(self.predat_array.shape,dtype=self.predat_array.dtype)
        for name in self.predat_array[:,1]:
            try:
                j = postpost_sid_dict[name]
                self.prepostpostmatch[i] = True
                #print self.postdat[j]
                #print self.postdatsort[j]
                self.postpostdatsort[i,:] = self.postpostdat[j]
            except KeyError:
                self.prepostpostmatch[i]=False
                print 'no post-post-test match for ',name
            i += 1
        if self.fciflag:
            self.postpost_darray=make2darrayfci(self.postpostdatsort)
        else:
            self.postpost_darray=make2darray(self.postpostdatsort)
        print 'fciflag = ',self.fciflag
        self.postpost_binary=transform_array(self.postpost_darray,flagS14=self.flagS14,fciflag=self.fciflag)

        self.postpost_score=np.sum(self.postpost_binary,axis=1)
        self.pre_postpost_hake=(self.postpost_score-self.pre_score)/(len(correct_answers)-self.pre_score) # gain between pre and post test divided by potential gain
    def get_aux_data(self):
        print 'working on this'
        auxpath=PERdir+'Other/'
        print auxpath

        # book
        infile=auxpath+'book.tsv'
        self.book,self.book_matchflag=self.match_aux(infile)

        


        # fresh_senior
        infile=auxpath+'Class_year_frosh_senior.tsv'
        self.gradyear,self.gradyear_matchflag=self.match_aux(infile)
        # hs_gpa
        infile=auxpath+'HSGPA.tsv'
        self.hsgpa,self.hsgpa_matchflag=self.match_aux(infile)
        #self.hsgpa=np.array(self.hsgpa,'f')
        # instructor
        infile=auxpath+'instructor.tsv'
        self.instructor,self.instructor_matchflag=self.match_aux(infile)
        # sat
        infile=auxpath+'SAT.tsv'
        self.sat,self.sat_matchflag=self.match_aux(infile)
        #self.sat=np.array(self.sat,'f')
        # section
        infile=auxpath+'section.tsv'
        self.section,self.section_matchflag=self.match_aux(infile)
        # math_prep
        infile=auxpath+'Siena_math_brad.tsv'
        self.sienamath,self.sienamath_matchflag=self.match_aux(infile)

        # teaching_method
        infile=auxpath+'teaching_method.tsv'
        self.teaching,self.teaching_matchflag=self.match_aux(infile)

        # final_exam
        infile=auxpath+'took_final.tsv'
        self.final,self.final_matchflag=self.match_aux(infile)
        # year_semester
        infile=auxpath+'year_semester.tsv'
        self.semester,self.semester_matchflag=self.match_aux(infile)
        # lawson
        try:
            infile=auxpath+'lawson.tsv'
            self.lawson,self.lawson_matchflag=self.match_aux(infile)
        except IOError:
            print 'no lawson file'
        # gender
        infile=auxpath+'gender.tsv'
        print infile
        self.gender,self.gender_matchflag=self.match_aux(infile)

    def match_aux(self,infile):
        t=readauxtsv(infile)
        t=np.array(t)
        #print t
        emails=t[:,0]
        dat=t[:,1]
        matchedarray=np.zeros(len(self.predat_array[:,1]),dtype='S12')
        matchedflag=np.zeros(len(self.predat_array[:,1]),dtype='bool')
        for i in range(len(emails)):
            try:
                matchindex=self.pre_dict[emails[i]]
                matchedarray[matchindex]=dat[i]
                matchedflag[matchindex]=True
                if dat[i].find('z') > -1:
                    matchedarray[matchindex]='-99'
            except KeyError:
                #print 'no aux match for ',emails[i]
                continue
        return matchedarray,matchedflag

            
    def cull_sample(self): # only keep students that took pre and post tests
        self.pre_darray=self.pre_darray[self.prepostmatch] # answers to questions
        self.pre_binary = self.pre_binary[self.prepostmatch] # binary score to questions
        self.predat_array=self.predat_array[self.prepostmatch] # entire data array
        self.post_darray=self.post_darray[self.prepostmatch]
        self.post_binary=self.post_binary[self.prepostmatch]
        self.postdat_array=self.postdatsort[self.prepostmatch]
        self.pre_score=self.pre_score[self.prepostmatch] # score on pretest
        self.post_score=self.post_score[self.prepostmatch] # score on post test
    def calculate_hake(self):
        self.pre_score=np.sum(self.pre_binary,axis=1)
        self.post_score=np.sum(self.post_binary,axis=1)
        self.hake=(self.post_score-self.pre_score)/(len(correct_answers)-self.pre_score)
    def plot_hake_junk(self,flag=None,normflag=True,title='Test'):
        self.calculate_hake()
        if flag == None:
            flag = np.ones(len(self.pre_score))
        plt.figure(figsize=(6,6))
        plt.subplots_adjust(hspace=.1)
        plt.subplot(2,1,1)
        plt.hist(self.pre_score[flag],bins=np.sum(flag),histtype='step',label='Pre-test',normed=normflag,cumulative=True,color='k')
        plt.hist(self.post_score[flag],bins=np.sum(flag),histtype='step',label='Post-test',normed=normflag,cumulative=True,color='0.5')
        plt.title(title)
        plt.xlabel('Score (out of 30)',fontsize=16)
        #plt.ylabel('Number of Students',fontsize=16)
        plt.legend(loc='upper left')
        plt.ylim(-.05,1.05)
        plt.xlim(0,30.2)
        plt.subplot(2,1,2)
        plt.hist(self.hake[flag],bins=np.sum(flag),normed=normflag,cumulative=True,color='k',histtype='step')
        plt.xlabel('Hake Score',fontsize=16)
        plt.text(-.8,1.1,'Number of Students',transform=plt.gca().transAxes,fontsize=20,rotation=90,verticalalignment='center')
        plt.ylim(-.05,1.05)
        plt.xlim(-.4,1.05)
        plt.savefig('em_hake_scores_'+title+'.png')
    def plot_hake(self,flag=None,normflag=True,title=''):
        #self.calculate_hake()
        plt.figure(figsize=(6,6))
        plt.subplots_adjust(hspace=.35)
        plt.subplot(2,1,1)
        score_bins=np.arange(0,31,2)
        hake_bins=np.arange(-1.,1.,.1)

        if flag != None:
            flag = flag & self.prepostmatch
        else:
            flag = self.prepostmatch

        if normflag:
            plt.hist(self.pre_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label='Pre-test',color='k')
            plt.hist(self.post_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label='Post-test',color='0.4')
        else:
            plt.hist(self.pre_score[flag],histtype='step',label='Pre-test',bins=score_bins)
            plt.hist(self.post_score[flag],histtype='step',label='Post-test',bins=score_bins)
            
        plt.xlabel('Score (out of 30)',fontsize=16)
        #plt.ylabel('Number of Students',fontsize=16)
        plt.legend(loc='upper left')
        plt.axis([0,30,-.05,1.05])
        #plt.title('Distribution of Raw and Hake Scores')
        plt.subplot(2,1,2)
        if normflag:
            plt.hist(self.hake[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',color='k')
        else:
            plt.hist(self.hake[flag],bins=hake_bins)            
        plt.xlabel('Hake Score',fontsize=16)
        ax=plt.gca()
        plt.text(-.09,1.5,'Cumulative Distribution',horizontalalignment='center',fontsize=16,transform=ax.transAxes,rotation=90)
        plt.axis([-.41,1,-.05,1.05])
        #plt.ylabel('Number of Students',fontsize=16)
        print 'output filename = ','../plots/'+self.testname+'_hake_scores_'+title+'.png'
        plt.savefig('../plots/'+self.testname+'_hake_scores_'+title+'.png')
    def plot_hake_4panel(self,normflag=False,title='',ymax=30):
        #self.calculate_hake()
        plt.figure(figsize=(9,6))
        plt.subplots_adjust(hspace=.35,top=.95,right=.95,left=.1)
        flags = [self.gpflag, ~self.gpflag]
        labels=['Calc-','Alg-']
        score_bins=np.arange(0,31,2)
        hake_bins=np.arange(-1.,1.,.1)

        for i in range(2):
            flag = flags[i] & self.prepostmatch
            plt.subplot(2,2,2*i+1)
            if normflag:
                plt.hist(self.pre_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label=labels[i]+'pre',color='k')
                plt.hist(self.post_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label=labels[i]+'post',color='r')
                print 'inside normflag, normflag = ',normflag
            else:
                plt.hist(self.pre_score[flag],histtype='stepfilled',label=labels[i]+'pre',bins=score_bins,color='k',hatch='/',alpha=0.5)
                plt.hist(self.post_score[flag],histtype='stepfilled',label=labels[i]+'post',bins=score_bins,color='r',hatch='\\',alpha=0.5)
            
            plt.xlabel('Score (out of 30)',fontsize=16)
            #plt.ylabel('Number of Students',fontsize=16)
            plt.legend(loc='upper right')
            if normflag:
                plt.axis([0,30,-.05,1.05])
            else:
                plt.axis([0,30,-.05,ymax])
            if i == 0:
                ax=plt.gca()
                plt.text(-.15,0,'Distribution',horizontalalignment='center',fontsize=20,transform=ax.transAxes,rotation=90)
            #plt.title('Distribution of Raw and Hake Scores')
            plt.subplot(2,2,2*i+2)
            if normflag:
                plt.hist(self.hake[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',color='k')
            else:
                plt.hist(self.hake[flag],bins=hake_bins,histtype='stepfilled',color='b',label=labels[i][0:-1],alpha=1)  
            plt.xlabel('Hake Score',fontsize=16)
            plt.legend(loc = 'upper right')
            if normflag:
                plt.axis([-.41,1,-.05,1.05])
            else:
                plt.axis([-.41,1,-.05,ymax])
        #plt.ylabel('Number of Students',fontsize=16)
            #print 'output filename = ','../plots/'+self.testname+'_hake_scores_'+title+'.png'
        plt.savefig(paperdir+self.testname+'_hake_scores_4panel.pdf')
        plt.savefig(paperdir+self.testname+'_hake_scores_4panel.png')

    def calculate_stuff(self):
        self.hake=(self.post_score-self.pre_score)/(len(correct_answers)-self.pre_score) # gain between pre and post test divided by potential gain
        self.calculate_item_difficulty()
        self.calculate_discrimination()
        self.calculate_point_biserial()
        #self.item_diff=np.sum(self.post_binary,axis=0)/self.pre_score.shape[0] # fraction of students who got the question right
        k=len(self.item_diff)*1.
        krsum=np.sum(self.item_diff*(1.-self.item_diff))
        krsigmax=np.std(self.post_score)
        self.kr21=k/(k-1)*(1-krsum/krsigmax**2)
        k=len(self.item_diff_gp)*1.
        krsum=np.sum(self.item_diff_gp*(1.-self.item_diff_gp))
        krsigmax=np.std(self.post_score[self.gpflag])
        self.kr21_gp=k/(k-1)*(1-krsum/krsigmax**2)
        k=len(self.item_diff_gpa)*1.
        krsum=np.sum(self.item_diff_gpa*(1.-self.item_diff_gpa))
        krsigmax=np.std(self.post_score[~self.gpflag])
        self.kr21_gpa=k/(k-1)*(1-krsum/krsigmax**2)

        ## Ferguson Delta
        flag=self.prepostmatch
        self.ferguson_delta=self.calc_ferguson(self.post_score[flag])
        flag=self.prepostmatch & self.gpflag
        self.ferguson_delta_gp=self.calc_ferguson(self.post_score[flag])
        flag=self.prepostmatch & ~self.gpflag
        self.ferguson_delta_gpa=self.calc_ferguson(self.post_score[flag])

        
    def calc_ferguson(self,x):
        t=plt.hist(x,bins=np.arange(0,31,1))
        f=t[0]
        N=len(x)
        K=30.
        return (N**2-np.sum(f**2))/(N**2*(1-1./(K+1)))
    def print_item_analysis(self):
        print '        OVERALL    |  Calc-based |  Alg-based'
        print '        diff discr |  diff discr |  diff discrim'
        print '------------------------------------------------'
        for i in range(len(self.item_diff)):
            print 'Q%2i  | %5.3f %5.3f | %5.3f %5.3f | %5.3f %5.3f'%(i+1,self.item_diff[i],self.discrim[i],self.item_diff_gp[i],self.discrim_gp[i],self.item_diff_gpa[i],self.discrim_gpa[i])
        names=['Question',
               'Difficulty',
               'Discrimination',
               'Point Biserial',
               'Diff (Calc)',
               'Discr (Calc)',
               'Point Bi (Calc)',
               'Diff (Alg)',
               'Discr (Alg)',
               'Point Bi (Alg)']
        qnum=np.arange(len(self.item_diff))+1
        columns=[qnum,
                 self.item_diff,
                 self.discrim,
                 self.point_biserial,
                 self.item_diff_gp,
                 self.discrim_gp,
                 self.point_biserial_gp,
                 self.item_diff_gpa,
                 self.discrim_gpa,
                 self.point_biserial_gpa]
        print len(names),len(columns)
        self.t=Table(columns,names=names)
        fname = PERdir+'plots/EM_item.tex'
        self.t.write(fname,format='latex',formats={'Difficulty':'%5.3f','Discrimination':'%5.3f','Diff (Calc)':'%5.3f','Discr (Calc)':'%5.3f','Diff (Alg)':'%5.3f','Discr (Alg)':'%5.3f','Point Biserial':'%5.3f','Point Bi (Calc)':'%5.3f','Point Bi (Alg)':'%5.3f'})

        s = 'Ave & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f& %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f & %5.3f $\pm$ %5.3f \n'%(np.mean(self.item_diff),np.std(self.item_diff), np.mean(self.discrim),np.std(self.discrim), np.mean(self.point_biserial),np.std(self.point_biserial),np.mean(self.item_diff_gp),np.std(self.item_diff_gp), np.mean(self.discrim_gp),np.std(self.discrim_gp),np.mean(self.point_biserial_gp),np.std(self.point_biserial_gp),np.mean(self.item_diff_gpa),np.std(self.item_diff_gpa),np.mean(self.discrim_gpa),np.std(self.discrim_gpa),np.mean(self.point_biserial_gpa),np.std(self.point_biserial_gpa))
        print s
        outfile = open(fname,'a')
        outfile.write(s)
        outfile.close()

                     
    def hake_bysubset(self,plotflag=False,colnum=39):
        '''
        col 39 = instructor
        col 3 == 120/140
        '''
        names=set(self.predat_array[:,colnum])
        print names
        print 'Hake Scores'
        for name in names: 
            flag=self.predat_array[:,colnum] == name
            print '%10s (Nstud = %i) mean(med)+/-error_mean=%4.2f(%4.2f)+/-%4.2f, ave pre,post score = %3.1f, %3.1f '%(name, np.sum(flag),np.mean(self.hake[flag]),np.median(self.hake[flag]),np.std(self.hake[flag])/np.sqrt(sum(flag)),np.mean(self.pre_score[flag]),np.mean(self.post_score[flag]))
            if plotflag:
                plt.figure()
                plt.hist(self.hake[flag])
                plt.title(name)
    def histabc(self,x,normflag=False,edgecolor='k',lw=1): # feed in array of letter choices, assuming a-e
        if self.testname == 'FCI':
            count=countabc(x,fci_mchoices)
        else:
            count=countabc(x,mchoices)
        if normflag:
            count=count/(1.*len(x))
        #plt.figure()
        w=0.8 # width of the bar
        plt.bar(np.arange(len(count))-.5*w,count,width=w,color='None',edgecolor=edgecolor,lw=lw)
        plt.xticks(np.arange(len(count)),mchoices)
        plt.xlim(-.5,len(count)-.5)
                
    def hake_func(self,flag=None,normflag=False,title=None):
        #self.calculate_hake()
        plt.figure(figsize=(6,6))
        plt.subplots_adjust(hspace=.35)
        plt.subplot(2,1,1)
        score_bins=np.arange(0,31,2)
        hake_bins=np.arange(-1.,1.,.1)

        if flag != None:
            flag = flag & self.prepostmatch
        else:
            flag = self.prepostmatch

        if normflag:
            plt.hist(self.pre_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label='Pre-test',color='k')
            plt.hist(self.post_score[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',label='Post-test',color='0.4')
        else:
            plt.hist(self.pre_score[flag],histtype='step',label='Pre-test',bins=score_bins)
            plt.hist(self.post_score[flag],histtype='step',label='Post-test',bins=score_bins)
            
        plt.xlabel('Score (out of 30)',fontsize=16)
        #plt.ylabel('Number of Students',fontsize=16)
        plt.legend(loc='upper left')
        if normflag:
            plt.axis([0,30,-.05,1.05])
        #plt.title('Distribution of Raw and Hake Scores')
        if title != None:
            plt.title(title)

        plt.subplot(2,1,2)
        if normflag:
            plt.hist(self.hake[flag],bins=sum(flag),normed=True,cumulative=True,histtype='step',color='k')
        else:
            plt.hist(self.hake[flag],bins=hake_bins)            
        plt.xlabel('Hake Score',fontsize=16)
        ax=plt.gca()
        plt.text(-.09,1.5,'Cumulative Distribution',horizontalalignment='center',fontsize=16,transform=ax.transAxes,rotation=90)
        if normflag:
            plt.axis([-.41,1,-.05,1.05])
        #plt.ylabel('Number of Students',fontsize=16)
        print 'output filename = ','../plots/'+self.testname+'_hake_scores_'+title+'.png'
        plt.savefig('../plots/'+self.testname+'_hake_scores_'+title+'.png')
    def plot_choices_bysubset(self, colnum=2):
        names=set(self.predat_array[:,colnum])
        print names
        for name in names: 
            flag=self.predat_array[:,colnum] == name
            self.plot_choices(normflag=True,subsetflag=flag,title=name)
            plt.text(-1.6,6.5,name,fontsize=20,transform=plt.gca().transAxes,horizontalalignment='center')
    def plot_choices(self,normflag=False,subsetflag=None,title=None):
        nstudent,nquestion=self.post_darray.shape
        nrow=6
        ncol=5
        plt.figure(figsize=(10,12))
        left_edge=[0,5,10,15,20,25]
        plt.subplots_adjust(hspace=.1,wspace=.05,bottom=0.1,left=0.1,right=.9,top=.9)
        if subsetflag == None:
            subsetflag=np.ones(len(self.pre_darray[:,0]))
        for i in range(nquestion):
            plt.subplot(nrow,ncol,i+1)
            self.histabc(self.pre_darray[:,i][subsetflag],normflag=normflag,edgecolor='k',lw=2)
            self.histabc(self.post_darray[:,i][subsetflag],normflag=normflag,edgecolor='r',lw=1.5)
            if self.flagS14:
                plot_correctchoice(i,flagS14=True)
            else:
                plot_correctchoice(i,fciflag=self.fciflag)
            if normflag:

                ymin=0
                ymax=.85
                ystep=.2
            else:
                ymin=0
                ymax=85
                ystep=20
            plt.ylim(ymin,ymax)
            if i in left_edge:
                plt.yticks(np.arange(ymin,ymax+.5*ystep,ystep))
            else:
                plt.yticks([])
            if i < 25:
                plt.xticks([])
            plt.text(0.5,0.8,'Q'+str(i+1),fontsize=16,transform=plt.gca().transAxes,horizontalalignment='center')
            if normflag:
                plt.axhline(y=0.5,ls='--',color='k')
        if title == '120':
            t = 'Algebra-Based Course'
        elif title == '140':
            t = 'Calculus-Based Course'
        plt.text(-1.5,6.7,t,transform=plt.gca().transAxes,horizontalalignment='center',fontsize=18)
        plt.savefig(paperdir+self.testname+'-'+title+'-question_choices.pdf')
        
    def calculate_item_difficulty(self,subset=None):
        self.item_diff=1.*np.sum(self.post_binary,axis=0)/np.shape(self.post_binary)[0]
        self.item_diff_gp=1.*np.sum(self.post_binary[self.gpflag],axis=0)/np.shape(self.post_binary[self.gpflag])[0]
        self.item_diff_gpa=1.*np.sum(self.post_binary[~self.gpflag],axis=0)/np.shape(self.post_binary[~self.gpflag])[0]
        
    def calculate_point_biserial(self):
        ave_post=np.mean(self.post_score)
        std_post=np.std(self.post_score)
        self.point_biserial=np.zeros(len(self.item_diff),'f')
        
        for i in range(len(self.point_biserial)):
            self.point_biserial[i]=(np.mean(self.post_score[(np.array(self.post_binary[:,i],'bool'))]) - ave_post)/std_post*np.sqrt(self.item_diff[i]/(1.-self.item_diff[i]))

        ave_post=np.mean(self.post_score[self.gpflag])
        std_post=np.std(self.post_score[self.gpflag])
        self.point_biserial_gp=np.zeros(len(self.item_diff),'f')
        for i in range(len(self.point_biserial)):
            self.point_biserial_gp[i]=(np.mean(self.post_score[(self.gpflag & np.array(self.post_binary[:,i],'bool'))] )- ave_post)/std_post*np.sqrt(self.item_diff_gp[i]/(1.-self.item_diff_gp[i]))
            
        ave_post=np.mean(self.post_score[~self.gpflag])
        std_post=np.std(self.post_score[~self.gpflag])
        self.point_biserial_gpa=np.zeros(len(self.item_diff),'f')
        for i in range(len(self.point_biserial)):
            self.point_biserial_gpa[i]=(np.mean(self.post_score[(~self.gpflag & np.array(self.post_binary[:,i],'bool'))]) - ave_post)/std_post*np.sqrt(self.item_diff_gpa[i]/(1.-self.item_diff_gpa[i]))
        
    def calculate_discrimination(self):
        self.discrim=calculate_discrimination(self.post_binary)
        self.discrim_gp=calculate_discrimination(self.post_binary[self.gpflag])
        self.discrim_gpa=calculate_discrimination(self.post_binary[~self.gpflag])
    def analyze_final_postpost(self):
        flag=self.prepostmatch & self.prepostpostmatch
        postpost_score_final=self.postpost_score[flag & (self.final == '1')]
        postpost_score_nofinal=self.postpost_score[flag & (self.final == '0')]
        post_score_final=self.post_score[flag & (self.final == '1')]
        post_score_nofinal=self.post_score[flag & (self.final == '0')]
        diff_final=postpost_score_final-post_score_final
        diff_nofinal=postpost_score_nofinal-post_score_nofinal
        plt.figure()
        plt.hist(diff_final,histtype='step')
        plt.hist(diff_nofinal,histtype='step')
        ks(diff_final,diff_nofinal)
    def analyze_teaching_postpost(self):
        flag=self.prepostmatch & self.prepostpostmatch
        postpost_score_final=self.postpost_score[flag & (self.teaching == 'I')]
        postpost_score_nofinal=self.postpost_score[flag & (self.teaching == 'T')]
        post_score_final=self.post_score[flag & (self.final == '1')]
        post_score_nofinal=self.post_score[flag & (self.final == '0')]
        diff_final=postpost_score_final-post_score_final
        diff_nofinal=postpost_score_nofinal-post_score_nofinal
        plt.figure()
        plt.hist(diff_final,histtype='step')
        plt.hist(diff_nofinal,histtype='step')
        ks(diff_final,diff_nofinal)
    def plot_hake_hsgpa(self):
        flag = self.hsgpa_matchflag & (self.hsgpa != 'z') & (self.hsgpa != 'Z') & self.prepostmatch & (self.hsgpa > -90.)
        x=np.array(self.hsgpa[flag],'f')
        y=self.hake[flag]
        plt.figure()
        plt.plot(x,y,'bo')
        spearman(x,y)
    def plot_hake_sat(self):
        flag = self.sat_matchflag & (self.sat != 'z') & (self.sat != 'Z') & self.prepostmatch & (self.sat != '-99.') & (self.sat != '')
        x=np.array(self.sat[flag],'f')
        y=self.hake[flag]
        plt.figure()
        plt.plot(x,y,'bo')
        spearman(x,y)
    def compare_hake_gender(self,instructor=None,gpflag=None):
        if instructor:
            flag = self.gender_matchflag & (self.gender != 'z') & (self.gender != 'Z') & self.prepostmatch & (self.instructor == instructor)
        else:
            flag = self.gender_matchflag & (self.gender != 'z') & (self.gender != 'Z') & self.prepostmatch
        if gpflag != None:
            flag = flag & gpflag

        f=self.hake[flag & (self.gender == 'f')]
        m=self.hake[flag & (self.gender == 'm')]
        ks(f,m)
        print 'anderson-darling'
        anderson(f,m)
        plt.figure()
        plt.hist(f,bins=len(f),normed=True,cumulative=True,histtype='step',color='m',label='Female')
        plt.hist(m,bins=len(m),normed=True,cumulative=True,histtype='step',color='b',label='Male')
        plt.xlabel('Hake Score')
        plt.legend(loc='upper left')
        plt.axis([-.5,1,-.05,1.05])

class fcidata(analysis):
    def __init__(self,fstring):
        self.match_string = fstring
        self.testname='FCI'
        self.fciflag=True
        self.datapath=PERdir+'FCI/data/'
        self.read_predat()
        self.read_postdat()
        self.read_postpostdat()

        self.match_prepost()
        #self.match_prepostpost()
        self.get_aux_data()
        #self.cull_sample()
        self.gpflag=(self.predat_array[:,2] == '130')
        self.calculate_stuff()
    def read_predat(self):
        print 'hey'
        match_this = self.datapath+'*Mechanics*Pre*'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this
        files=glob.glob(match_this)
        #print 'found these'
        #print files
        predat=[]
        for f in files:
            print f
            t=readtsv(f)
            #print t
            predat=predat+t[1:] # omit header row
        #print predat
        self.predat=predat
        self.pre_darray=make2darrayEM2014pre(predat)
        self.flagS14=False
        self.predat_array=np.array(predat)
        #print 'flagS14 = ',self.flagS14
        self.pre_binary=transform_array(self.pre_darray,flagS14=self.flagS14,fciflag=True)
        self.pre_score=np.sum(self.pre_binary,axis=1)
        self.pre_dict = dict((a,b) for a,b in zip(self.predat_array[:,1],np.arange(len(self.predat_array[:,1]))))
    def read_postdat(self):
        files=glob.glob(self.datapath+'*Post-*'+self.match_string+'*.tsv')
        postdat=[]
        for f in files:
            t=readtsv(f)
            postdat=postdat+t[1:] # omit header row
        self.postdat=np.array(postdat)
        self.post_darray=make2darrayfci(self.postdat)
        self.post_dict = dict((a,b) for a,b in zip(self.postdat[:,1],np.arange(len(self.postdat[:,1]))))
    def read_postpostdat(self):
        files=glob.glob(self.datapath+'*Follow*'+self.match_string+'*.tsv')
        postdat=[]
        for f in files:
            t=readtsv(f)
            postdat=postdat+t[1:] # omit header row
        self.postpostdat=np.array(postdat)
        self.postpost_darray=make2darrayfci(self.postpostdat)
        try:
            self.postpost_dict = dict((a,b) for a,b in zip(self.postpostdat[:,1],np.arange(len(self.postpostdat[:,1]))))
        except:
            print 'WARNING: PROBLEM MAKING POSTPOST_DICT'
            print 'probably a problem with missing columns in a data file :('

class emdata(analysis):
    def __init__(self,fstring):
        self.match_string = fstring
        self.testname='EM'
        self.fciflag=False
        self.datapath=PERdir+'EM/data/' # need to check what difference is b/w data and data2 directory

        if (fstring.find('S13') > -1) :
            self.read_predat()
            self.read_postdat()
            self.match_prepost_em()
        else:
            self.read_predatv0()
            self.read_postdatv0()
            self.match_prepost()
        self.get_aux_data()
        #self.cull_sample()
        self.gpflag=(self.predat_array[:,2] == '140')
        self.calculate_stuff()
    def read_predat(self):
        #match_this_pre = self.datapath+'*Pre'+self.match_string+'.tsv'
        #print 'Searching for files: ',match_this_pre
        #files_pre=glob.glob(match_this_pre)
        #print 'found these'
        match_this_S14 = self.datapath+'*Pre*.S14'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this_S14
        files=glob.glob(match_this_S14)
        #files = set(files_pre) & set(files_S14)
        print files
        print 'working on this'
        predatS14=[]
        for f in files:
            t=readtsv(f)
            print len(t),' students from file ',f
            predatS14=predatS14+t[1:] # omit header row
        #print predat
        self.predatS14=predatS14#indented here
        self.pre_darrayS14=make2darray(predatS14)
        self.flagS14=True
        print 'flagS14 is true!'
        self.predatS14_array=(predatS14)
        self.pre_binaryS14=transform_array(self.pre_darrayS14,flagS14=self.flagS14)
        self.pre_scoreS14=np.sum(self.pre_binaryS14,axis=1)


        
        match_this_S15 = self.datapath+'*Pre*.S15'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this_S15
        files=glob.glob(match_this_S15)
        #files = set(files_pre) & set(files_S15)
        print files
        print 'working on this'
        predatS15=[]
        for f in files:
            t=readtsv(f)
            print f
            predatS15=predatS15+t[1:] # omit header row
        self.predatS15=(predatS15) #indented here
        self.pre_darrayS15=make2darray(predatS15)
        self.flagS14=False
        print 'flagS14 is false!'
        self.predatS15_array=np.array(predatS15)
        self.pre_binaryS15=transform_array(self.pre_darrayS15,flagS14=self.flagS14)
        self.pre_scoreS15=np.sum(self.pre_binaryS15,axis=1)

        # stack arrays from S14 and S15
        self.predat = np.vstack((np.array(self.predatS14),np.array(self.predatS15)))
        #self.predat = predat
        self.pre_darray = np.vstack((self.pre_darrayS14,self.pre_darrayS15))
        self.predat_array = np.vstack((self.predatS14_array,self.predatS15_array))
        self.pre_binary = np.vstack((self.pre_binaryS14,self.pre_binaryS15))
        self.pre_score = np.array(self.pre_scoreS14.tolist()+self.pre_scoreS15.tolist())

        self.pre_dict = dict((a,b) for a,b in zip(self.predat_array[:,1],np.arange(len(self.predat_array[:,1]))))
    def read_predatv0(self):
        match_this = self.datapath+'*Pre'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this
        files=glob.glob(match_this)
        #print 'found these'
        #print files
        predat=[]
        for f in files:
            #print f
            t=readtsv(f)
            #print t
            predat=predat+t[1:] # omit header row
            test=np.array(predat)
            #print test[:,1]
        #print predat
        self.predat=predat
        if self.match_string.find('S14') > -1:

            self.flagS14=True
        else:

            self.flagS14=False
        self.pre_darray=make2darray(predat)
        self.predat_array=np.array(predat)
        print 'flagS14 = ',self.flagS14
        self.pre_binary=transform_array(self.pre_darray,flagS14=self.flagS14)
        self.pre_score=np.sum(self.pre_binary,axis=1)
        #print self.predat_array


            
        self.pre_dict = dict((a,b) for a,b in zip(self.predat_array[:,1],np.arange(len(self.predat_array[:,1]))))
        
    def read_postdatv0(self):
        files=glob.glob(self.datapath+'*Post-*'+self.match_string+'*.tsv')
        postdat=[]
        for f in files:
            print f
            t=readtsv(f)
            postdat=postdat+t[1:] # omit header row
        self.postdat=np.array(postdat)
        self.post_darray=make2darray(postdat)
        #print 'TEST'
        #print self.postdat
        print self.postdat.shape
        self.post_dict = dict((a,b) for a,b in zip(self.postdat[:,1],np.arange(len(self.postdat[:,1]))))
    def read_postdat(self):
        #match_this_pre = self.datapath+'*Pre'+self.match_string+'.tsv'
        #print 'Searching for files: ',match_this_pre
        #files_pre=glob.glob(match_this_pre)
        #print 'found these'
        match_this_S14 = self.datapath+'*Post*.S14'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this_S14
        files=glob.glob(match_this_S14)
        #files = set(files_pre) & set(files_S14)
        print files
        print 'working on this'
        postdatS14=[]
        for f in files:
            t=readtsv(f)
            print len(t),' students from file ',f
            postdatS14=postdatS14+t[1:] # omit header row
        #print predat
        self.postdatS14=postdatS14#indented here
        self.post_darrayS14=make2darray(postdatS14)
        self.flagS14=True
        print 'flagS14 is true!'
        self.postdatS14_array=np.array(postdatS14)
        self.post_binaryS14=transform_array(self.post_darrayS14,flagS14=self.flagS14)
        self.post_scoreS14=np.sum(self.post_binaryS14,axis=1)
        
        match_this_S15 = self.datapath+'*Post*.S15'+self.match_string+'.tsv'
        print 'Searching for files: ',match_this_S15
        files=glob.glob(match_this_S15)
        #files = set(files_pre) & set(files_S15)
        print files
        print 'working on this'
        postdatS15=[]
        for f in files:
            t=readtsv(f)
            print f
            postdatS15=postdatS15+t[1:] # omit header row
        self.postdatS15=(postdatS15) #indented here
        self.post_darrayS15=make2darray(postdatS15)
        self.flagS14=False
        print 'flagS14 is false!'
        self.postdatS15_array=np.array(postdatS15)
        self.post_binaryS15=transform_array(self.post_darrayS15,flagS14=self.flagS14)
        self.post_scoreS15=np.sum(self.post_binaryS15,axis=1)

        # stack arrays from S14 and S15
        self.postdat = np.vstack((np.array(self.postdatS14),np.array(self.postdatS15)))
        self.post_darray_temp = np.vstack((self.post_darrayS14,self.post_darrayS15))
        self.postdat_array_temp = np.vstack((self.postdatS14_array,self.postdatS15_array))
        self.post_binary_temp = np.vstack((self.post_binaryS14,self.post_binaryS15))
        #self.postscore = np.array([self.post_scoreS14.tolist()+self.post_scoreS15.tolist()])

        self.post_dict = dict((a,b) for a,b in zip(self.postdat_array_temp[:,1],np.arange(len(self.postdat_array_temp[:,1]))))
    def match_prepost_em(self):
        # find matches between pre and post data using student email id

        post_sid_dict=dict((a,b) for a,b in zip(self.postdat[:,1],np.arange(len(self.postdat[:,1]))))
        self.prepostmatch=np.zeros(len(self.predat),'bool')
        i=0
        self.postdatsort=np.zeros(self.predat_array.shape,dtype=self.predat_array.dtype)
        self.post_darray=np.zeros(self.pre_darray.shape,dtype=self.pre_darray.dtype)
        self.post_binary=np.zeros(self.pre_binary.shape,dtype=self.pre_binary.dtype)
        for name in self.predat_array[:,1]:
            try:
                j = self.post_dict[name]
                self.prepostmatch[i] = True
                #print self.postdat[j]
                #print self.postdatsort[j]
                self.postdatsort[i,:] = self.postdat[j]
                self.post_darray[i,:] = self.post_darray_temp[j]
                self.post_binary[i,:] = self.post_binary_temp[j]
            except KeyError:
                self.prepostmatch[i]=False
                print 'no post-test match for ',name
            i += 1

        self.post_score=np.sum(self.post_binary,axis=1)

    def match_em_fci(self,fci):
        # find matches between pre and post data using student email id

        fci_sid_dict=dict((a,b) for a,b in zip(fci.predat_array[:,1],np.arange(len(self.predat_array[:,1]))))
        self.fcimatch=np.zeros(len(self.predat),'bool')
        self.fcimatchindex=np.zeros(len(self.predat),'i')
        i=0
        for name in self.predat_array[:,1]:
            try:
                j = fci_sid_dict[name]
                self.fcimatch[i] = True
                self.fcimatchindex[i] = j
                #self.postdatsort[i,:] = self.postdat[j]
            except KeyError:
                self.fcimatch[i]=False
                print 'no fci match for ',name
            i += 1


        
if __name__ == "__main__":

    f15=fcidata('*F15*')
    f14=fcidata('*F14*')
    #f13=fcidata('*F13*')
    #gh = fcidata('*S16*')
    f=fcidata('*F*')
    #e=emdata('*')
    
    ##e14=emdata('*.S14*')
    e15=emdata('*.S15*')
    e16=emdata('*.S16*')
    e=emdata('*.S??-*')
    #f15=fcidata('*F15*')
    e15.match_em_fci(f14)
    e16.match_em_fci(f15)
    e.match_em_fci(f)
    #p14=emdata('*.S14*')
    print 'hey there!'



# plots for poster
# choice distribution for each question
# item difficulty versus question number
# point biserial coefficient vs question number

# table 

def compareEandF():
    '''
    plt.figure()
    plt.plot(f14.hake[e15.fcimatchindex[e15.fcimatch]],e15.hake[e15.fcimatch],'bo')
    plt.xlabel('FCI Hake Score')
    plt.ylabel('EM Hake Score')
    # plot pre-score vs pre-score and post-score vs post-score
    plt.figure() 
    plt.plot(f14.pre_score[e15.fcimatchindex[e15.fcimatch]],e15.pre_score[e15.fcimatch],'bo',label='Pre-test Score')
    plt.xlabel('FCI Pre-test Score')
    plt.ylabel('EM Pre-test Score')
    plt.figure() 
    plt.plot(f14.post_score[e15.fcimatchindex[e15.fcimatch]],e15.post_score[e15.fcimatch],'ko',label='Post-test Score')
    plt.xlabel('FCI Post-test Score')
    plt.ylabel('EM Post-test Score')
    '''
    plt.figure(figsize=(5,9))
    plt.subplots_adjust(hspace=.35,left=.15,right=.95,bottom=.1,top=.95)
    plt.subplot(3,1,3)
    fcipostmatchflag = f.prepostmatch[e.fcimatchindex]
    flag1 = e.fcimatch & e.prepostmatch
    flag2 = f.prepostmatch
    x = f.hake[e.fcimatchindex[flag1 & fcipostmatchflag]]
    y = e.hake[flag1 & fcipostmatchflag]
    print 'EMCA vs FCI Hake score'
    spearman(x,y)

    plt.plot(x,y,'ko')
    plt.xlabel('FCI Hake Score')
    plt.ylabel('EMCA Hake Score')
    # plot pre-score vs pre-score and post-score vs post-score
    #plt.figure()
    x = f.pre_score[e.fcimatchindex[flag1 & fcipostmatchflag]]
    y = e.pre_score[flag1 & fcipostmatchflag]
    print 'EMCA vs FCI Pre score'
    spearman(x,y)
    plt.subplot(3,1,1)
    plt.plot(x,y,'ko',label='Pre-test Score')
    plt.xlabel('FCI Pre-test Score')
    plt.ylabel('EMCA Pre-test Score')
    #plt.figure()
    plt.subplot(3,1,2)
    x = f.post_score[e.fcimatchindex[flag1 & fcipostmatchflag]]
    y = e.post_score[flag1 & fcipostmatchflag]
    print 'EMCA vs FCI Post score'
    spearman(x,y)
    plt.plot(x,y,'ko',label='Post-test Score')
    plt.xlabel('FCI Post-test Score')
    plt.ylabel('EMCA Post-test Score')
    plt.savefig(PERdir+'plots/EMCA_vs_FCI.png')

    
    
def makepaperplots():
    e.plot_hake_4panel(title='2x2',ymax=35)
    f.plot_hake_4panel(title='2x2',ymax=35)
    flag = e.gpflag & e.prepostmatch
    e.plot_choices(subsetflag=flag,title='140',normflag=True)
    # PHYS 120 Students
    flag = ~e.gpflag & e.prepostmatch
    e.plot_choices(subsetflag=flag,title='120',normflag=True)
