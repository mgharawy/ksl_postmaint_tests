#!/usr/bin/env python
# Filename: CopyOf_myDrmaa.py
import sys, time, drmaa
version = '1.0'
print( 'DRMAA VERSION: {}'.format( drmaa.__version__ ) )
class myDrmaa(object):

   """
   ACKNOWLEDGEMENTS: Gratefully thank the following sources for their code. 

   1. This module, mod_CopyOf_myDrmaa is mild modification from myDrmaa (Nicole). Thanks Nicole. 
   2. Code for decodestatus data structure from: http://drmaa-python.readthedocs.io/en/latest/tutorials.html#getting-job-status
   Acknowledged with thanks. 

   """

   def __init__(self):
      self.initDrmaa()

   def initDrmaa(self):
      # drmaa session and job template
      self.drm_session              = drmaa.Session()
      self.drm_session.initialize()
      self.drm_jt                   = self.drm_session.createJobTemplate()
      self.drm_jobs                 = []

   #def runJob(self, command, args, nativeSpec='--time=00:02:00 --partition=interactive'):   ### CHANGE_BACK_AFTER_OUTAGE
   def runJob(self, command, args, nativeSpec='--time=00:02:00 --partition=batch'):          ### DELETE_THIS_AFTER_OUTAGE
      # nativeSpec defaults to run for 2 min in interactive partition for quick testing
      self.drm_jt.nativeSpecification = nativeSpec   
      self.drm_jt.remoteCommand       = command
      self.drm_jt.args                = args
      jid = self.drm_session.runJob(self.drm_jt)
      self.drm_jobs.append(jid)
      return jid

   def syncJobs(self):
#      if not self.drm_jobs: return # THINK ABOUT THIS LINE. 
      sys.stderr.write('Start time : %s\n' % time.asctime( time.localtime(time.time()) ))

#      self.drm_session.synchronize(self.drm_jobs, drmaa.Session.TIMEOUT_WAIT_FOREVER, False) ## OLD-CODE
#     Based on John's advice, following exception is caught-wait_till_success-then_continue (2017-03-01)
      wait_time    = 30
      num_attempts = 1
      while True: 
         try: self.drm_session.synchronize(self.drm_jobs, drmaa.Session.TIMEOUT_WAIT_FOREVER, False)
         except drmaa.errors.InternalException:
            print( 'Oops! Caught drmaa.errors.InternalException: Waiting for {} seconds. Attempt #{}'.format( wait_time, num_attempts ) )
            num_attempts += 1
            time.sleep( wait_time )
            continue
         except: print( 'Some drmaa exception other than InternalException' )
         else: break

      for jid in self.drm_jobs:
         info = self.drm_session.wait(jid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
      sys.stderr.write('End time   : %s\n' % time.asctime( time.localtime(time.time()) ))

      self.drm_jobs = []

   def quit(self):
      self.drm_session.deleteJobTemplate(self.drm_jt)
      self.drm_session.exit()

   def jobState(self, job_id): return self.drm_session.jobStatus(job_id)

   def decodeStatus(self, job_status):
      """decodestatus data structure code from: 
      http://drmaa-python.readthedocs.io/en/latest/tutorials.html#getting-job-status
      I thankfully acknowledge the source. 
      """
      decodestatus = { drmaa.JobState.UNDETERMINED: 'process status cannot be determined',
                      drmaa.JobState.QUEUED_ACTIVE: 'job is queued and active',
                     drmaa.JobState.SYSTEM_ON_HOLD: 'job is queued and in system hold',
                       drmaa.JobState.USER_ON_HOLD: 'job is queued and in user hold',
                drmaa.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
                            drmaa.JobState.RUNNING: 'job is running',
                   drmaa.JobState.SYSTEM_SUSPENDED: 'job is system suspended',
                     drmaa.JobState.USER_SUSPENDED: 'job is user suspended',
                               drmaa.JobState.DONE: 'job finished normally',
                             drmaa.JobState.FAILED: 'job finished, but failed' }
      return decodestatus[ job_status ]

