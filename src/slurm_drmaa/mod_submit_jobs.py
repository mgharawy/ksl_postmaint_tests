#!/usr/bin/env python
import __builtin__
import os
from   random import randint, choice
from mod_CopyOf_myDrmaa import myDrmaa
from               time import sleep

LOGS_PATH = '.'

MIN_DELAY = 30
MAX_DELAY = 40

def run_scripts( job_scripts = [], logfile_prefix = '', job_name = '' ):
 
   if not job_scripts:
      __builtin__.ERR_MESG = 'run_scripts() method in mod_submit_jobs called without a script!'
      return False

   # initialize drmma object
   drm = myDrmaa()
   # request entire node for 3 day (slurm-drmaa cannot handle time given in days)
   #nativeSpec = '--time=12:00:00 --reservation=BioCoreLab --exclusive --mem=0'
   #reservation = 'BioCoreLab' if job_name == 'Basecalling' else '' ### CHANGE_BACK_AFTER_OUTAGE
   #reservation = ''                                                 ### DELETE_THIS_AFTER_OUTAGE
   #nativeSpec = '--time=72:00:00 --reservation=' + reservation + ' --ntasks=1 --nodes=1 --mincpus=8 --mem=30000'
   
   partition  = 'batch' # on 22nd of Oct, reserved nodes were moved to a partition.
   #group_qos  = ' --qos=group-bcl ' # accepted values: normal / group-bcl
   group_qos  = ' --reservation=MAINTENANCE' # accepted values: normal / group-bcl
   mem_size   = 131072 if job_name == 'Basecalling' else 30000 # This was introduced on 2021-06-02 following an actual out of memory for the bcl2fastq step. 
   #nativeSpec = '--time=72:00:00 --partition=' + partition + group_qos + ' --ntasks=1 --nodes=1 --mincpus=8 --mem={}'.format( mem_size )
   nativeSpec = '--time=2:00:00 --partition=' + partition + ' --ntasks=1 --nodes=1 --mincpus=8 --mem={}'.format( mem_size )

   jids = []
   for job_script in job_scripts:
      # submit job to cluster
      logfile_suffix        = 'log_' + os.path.basename( job_script ).split('.')[0] + '.txt'
      logFile               = '_'.join( [ logfile_prefix, logfile_suffix ] ) if logfile_prefix else logfile_suffix
      out_logFile           = 'out_' + logFile
      err_logFile           = 'err_' + logFile
      drm.drm_jt.outputPath = ':%s' % os.path.join( LOGS_PATH, out_logFile )
      drm.drm_jt.errorPath  = ':%s' % os.path.join( LOGS_PATH, err_logFile )
      drm.drm_jt.jobName    = job_name if job_name else 'iPipeTest'
      args                  = [ job_script, ]

#      print '%s %s %s %s\n%s\n%s\n%s\n%s' % ( logfile_suffix, logFile, out_logFile, err_logFile, drm.drm_jt.outputPath, drm.drm_jt.errorPath, drm.drm_jt.jobName, args )	# testing
#      return False		# testing

      # introducing delay, following John's advice
      delay = randint( MIN_DELAY, MAX_DELAY )
      sleep( delay )
      # run / submit job after a short random delay
      print('bash args = {} nativespec = {}'.format( args, nativeSpec )) # for_testing
      jids.append( drm.runJob( 'bash', args, nativeSpec = nativeSpec ) )
      print 'Your job script %s has been submitted with job id: %d' % ( args[0], int( jids[-1] ) )

   # wait for jobs to finish and then kill drmaa object
   drm.syncJobs()

   finished_with_error = 0
   for jid in jids:
      mesg = drm.decodeStatus( drm.jobState( jid ) )
      if mesg == 'job finished normally': pass
      else: 
         __builtin__.ERR_MESG = str( 'Slurm Error: ' + mesg + ' ' + str( jid ) )
         finished_with_error = 1
   drm.quit()
   return ( True if not finished_with_error else False )

if __name__ == '__main__': pass
