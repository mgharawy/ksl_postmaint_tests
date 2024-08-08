import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_drmaa(rfm.RunOnlyRegressionTest):
      @run_after('init')
      def setting_variables(self):
        self.descr = 'SLURM DRMAA check'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir= '../src/slurm_drmaa'
        self.time_limit = '3m'
        self.prerun_cmds = ['./runme.sh']
        self.executable='cat out_log_bcl2fastq_test.txt'
        self.sanity_patterns =sn.assert_found(r'Hello!',self.stdout)
        self.maintainers = ['ahmed.khatab@kaust.edu.sa']
        self.tags = {'slurm','drmaa','acceptance','cpu'}
































