#!/usr/bin/env python
import __builtin__
import os
from mod_submit_jobs import run_scripts

RUN_SCRIPT = 'bcl2fastq_test.sh'

def perform_basecalling():
#   w_shell_actions     = open( SHELL_ACTIONS, 'w' ) if not os.path.isfile( SHELL_ACTIONS ) else open( SHELL_ACTIONS, 'a' )
#   if not os.stat( SHELL_ACTIONS ).st_size: # if the shell actions file is a new one
#      w_shell_actions.write( '# Program Name: iPipe.py v{}\n'.format( VERSION ) )
#      w_shell_actions.write( '# Date: {}\n\n'.format( time.strftime( '%c' ) ) )
   print( '\nThis is just a DEBUGGING LINE in perform_basecalling() method.\n' )
   print( '\n\n########## TRANSCRIPT OF BASECALLING PROCESSES ##########\n\nSubmitting the base calling job for {}\n\n'.format( RUN_SCRIPT, ) )
   print( 'Script: {}\n'.format( RUN_SCRIPT, ) )
   return ( True if run_scripts( [ RUN_SCRIPT, ], job_name = 'Basecalling' ) else False )

if __name__ == '__main__': perform_basecalling()
