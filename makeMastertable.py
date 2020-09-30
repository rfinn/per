#!/usr/bin/env python

'''
GOAL:
- create master table with combined FCI & EM results

CONTENTS OF FILE:
email address (from FCI)
course (from FCI)
fci-pre (from FCI)
fci-post (from FCI)
fci-postpost (from FCI)
fci-gains for post (from FCI)
fci-gains for postpost (from FCI)
level of math in hs (from FCI)
took physics in hs? (from FCI)
what type of physics? (from FCI)
e&m (from EM)
CTSR ((from CTSR)
instructor (separate data file)
class year -frosh - senior (separate data file)
gender (separate data file)
year/semester took course (separate data file)
SAT (separate data file)
HS GPA (separate data file)
teaching method (separate data file)
 level of math just prior to taking phys1 (phys2 for e&m?) (separate data file)
took a final? (separate data file)
Course sections arranged as CA and UP by numbers (separate data file)
book used (still getting this data)


'''

import numpy as np
import pylab as pl
from em_parse_spreadsheet import *
from astropy.table import Table
class fullsample():
    def __init__(self):
        # read in all fci
        self.fci = fcidata('*F*') # just fall course (ignoring off-sequence classes for now)
        # read in all em
        self.em = emdata('*')
        # make master set of all students in either em or fci files
        all_emails=self.fci.predat_array[:,1].tolist()+self.fci.postdat[:,1].tolist()+self.fci.predat_array[:,1].tolist() + self.fci.postdat[:,1].tolist()
        self.allemail_set=set(all_emails)
        self.allemail=list(set(all_emails))
        self.allemail.sort()
        self.allemail_dict=dict((a,b) for a,b in zip(self.allemail,np.arange(len(self.allemail))))
        self.get_aux_data()
    def get_aux_data(self):
        print 'working on this'
        auxpath=PERdir+'Other/'
        
        # gender
        infile=auxpath+'gender.tsv'
        self.gender,self.gender_matchflag=self.match_aux(infile)


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

    def match_aux(self,infile):
        t=readauxtsv(infile)
        t=np.array(t)
        emails=t[:,0]
        dat=t[:,1]
        matchedarray=np.zeros(len(self.allemail),dtype='S12')
        matchedflag=np.zeros(len(self.allemail),dtype='bool')
        for i in range(len(emails)):
            try:
                matchindex=self.allemail_dict[emails[i]]
                matchedarray[matchindex]=dat[i]
                matchedflag[matchindex]=True
                if dat[i].find('z') > -1:
                    matchedarray[matchindex]='-99'

            except KeyError:
                print 'no match to auxiliary data for ',emails[i], infile
        matchedarray[~matchedflag]=np.array([-99*np.ones(sum(~matchedflag),'i')],'S3')
        return matchedarray,matchedflag


    def write_table(self):
        # match emails to fci and em email lists
        #
        self.fci_match=np.zeros(len(self.allemail),'bool')
        self.fci_index=np.zeros(len(self.allemail),'i')
        self.em_match=np.zeros(len(self.allemail),'bool')
        #self.em_post_match=np.zeros(len(self.allemail),'bool')
        self.em_index=np.zeros(len(self.allemail),'i')
        #self.aux_match=np.zeros(len(self.allemail),'bool')
        for i in range(len(self.allemail)):
            try:
                j=self.fci.pre_dict[self.allemail[i]]
                self.fci_match[i]=True
                self.fci_index[i]=j
            except KeyError:
                print 'no fci match for ',self.allemail[i]
                continue
        for i in range(len(self.allemail)):
            try:
                j=self.em.pre_dict[self.allemail[i]]
                self.em_match[i]=True
                self.em_index[i]=j
            except KeyError:
                print 'no em match for ',self.allemail[i]
                continue
        # initialize arrays
        # 
        # email address (from FCI)
        # course (from FCI)
        # self.section = np.zeros(len(self.allemail),dtype='S5')
        # fci-pre (from FCI)
        self.fci_pre_score=-99.*np.ones(len(self.allemail),'f')
        self.fci_pre_score[self.fci_match]=self.fci.pre_score[self.fci_index[self.fci_match]]

        # fci-post (from FCI)
        self.fci_post_score=-99.*np.ones(len(self.allemail),'f')
        self.fci_post_match=np.zeros(len(self.allemail),'bool')
        self.fci_post_match[self.fci_match] = self.fci.prepostmatch[self.fci_index[self.fci_match]]
        self.fci_post_score[self.fci_match & self.fci_post_match]=self.fci.post_score[self.fci_index[self.fci_match & self.fci_post_match]]


        # fci-gains for post (from FCI)
        self.fci_hake=-99.*np.ones(len(self.allemail),'f')
        self.fci_hake[self.fci_match & self.fci_post_match]=self.fci.hake[self.fci_index[self.fci_match & self.fci_post_match]]


        # fci-postpost (from FCI)
        self.fci_postpost_score=-99.*np.ones(len(self.allemail),'f')
        self.fci_postpost_match=np.zeros(len(self.allemail),'bool')
        self.fci_postpost_match[self.fci_match] = self.fci.prepostpostmatch[self.fci_index[self.fci_match]]
        self.fci_postpost_score[self.fci_match & self.fci_postpost_match]=self.fci.postpost_score[self.fci_index[self.fci_match & self.fci_postpost_match]]
        
        # fci-gains for postpost (from FCI)
        self.fci_pre_postpost_hake=-99.*np.ones(len(self.allemail),'f')        
        self.fci_pre_postpost_hake[self.fci_match & self.fci_postpost_match]=self.fci.pre_postpost_hake[self.fci_index[self.fci_match & self.fci_postpost_match]]

        # e&m (from EM)
        self.em_pre_score=-99.*np.ones(len(self.allemail),'f')
        self.em_pre_score[self.em_match]=self.em.pre_score[self.em_index[self.em_match]]

        self.em_post_score=-99.*np.ones(len(self.allemail),'f')
        self.em_post_match=np.zeros(len(self.allemail),'bool')
        self.em_post_match[self.em_match] = self.em.prepostmatch[self.em_index[self.em_match]]
        self.em_post_score[self.em_match & self.em_post_match]=self.em.post_score[self.em_index[self.em_match & self.em_post_match]]

        self.em_hake=-99.*np.ones(len(self.allemail),'f')
        self.em_hake[self.em_match & self.em_post_match]=self.em.hake[self.em_index[self.em_match & self.em_post_match]]

        # group columns to write as table
        self.columns=[
            self.allemail,
            np.array(self.fci_match,'i'),
            self.fci_pre_score,
            np.array(self.fci_post_match,'i'),
            self.fci_post_score,
            self.fci_hake, 
            np.array(self.fci_postpost_match, 'i'),
            self.fci_postpost_score, 
            self.fci_pre_postpost_hake, 
            np.array(self.em_match,'i'),
            self.em_pre_score,
            np.array(self.em_post_match,'i'),
            self.em_post_score,
            self.em_hake,
            np.array(self.gender_matchflag,'i'),
            #self.self_math,
            #self.took_hsphysics,
            #self.hsphysics,
            self.lawson,
            self.instructor,
            self.gradyear,
            self.gender,
            self.sat,
            self.hsgpa,
            self.semester,
            self.sienamath,
            self.final,
            self.section,
            self.book]
        self.names=[
            'email',
            'fci_match',
            'fci_pre_score',
            'fci_post_match',
            'fci_post_score',
            'fci_hake', 
            'fci_postpost_match', 
            'fci_postpost_score', 
            'fci_pre_postpost_hake', 
            'em_match',
            'em_pre_score',
            'em_post_match',
            'em_post_score',
            'em_hake',
            'aux_match',
            #'self_math',
            #'took_hsphysics',
            #'hsphysics',
            'lawson',
            'instructor',
            'gradyear',
            'gender',
            'SAT',
            'HS_GPA',
            'semester',
            'sienamath',
            'final',
            'section',
            'book']
        self.t=Table(self.columns,names=self.names,masked=True)
        self.t.write(PERdir+'master_table/PER_mastertable.txt',format='ascii',formats={'fci_hake':'%5.3f','fci_pre_postpost_hake':'%5.3f','em_hake':'%5.3f'})
        
    def read_table(self):
        self.mt=Table.read(PERdir+'master_table/PER_mastertable.txt',format='ascii')


if __name__ == '__main__':
    a=fullsample()

