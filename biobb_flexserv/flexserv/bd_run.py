#!/usr/bin/env python3

"""Module containing the bd_run class and the command line interface."""
import argparse
import shutil, re, os
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.flexserv.bd_run as myself
from biobb_flexserv.flexserv.common import *

class BDRun(BiobbObject):
    """
    | biobb_flexserv BDRun
    | Wrapper of the Browian Dynamics tool from the FlexServ module.
    | Generates protein conformational structures using the Brownian Dynamics (BD) method.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_crd_path (str): Output ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("bd") BD binary path to be used.
            * **time** (*int*) - (1000000) Total simulation time (ps)
            * **dt** (*float*) - (1e-15) Integration time (ps)
            * **wfreq** (*int*) - (1000) Writing frequency (ps)
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.flexserv.bd_run import bd_run
            prop = {
                'binary_path': 'bd'
            }
            flexserv_run(input_pdb_path='/path/to/bd_input.pdb',
                         output_log_path='/path/to/bd_log.log',
                         output_crd_path='/path/to/bd_ensemble.crd',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: FlexServ Brownian Dynamics
            * version: >=1.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pdb_path: str, output_log_path: str,
    output_crd_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path },
            'out': {    'output_log_path': output_log_path,
                        'output_crd_path': output_crd_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'bd')
        self.time = properties.get('time', 1000000)
        self.dt = properties.get('dt', 1e-15)
        self.wfreq = properties.get('wfreq', 1000)

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, out_err):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_log_path"] = check_output_path(self.io_dict["out"]["output_log_path"],"output_log_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_crd_path"] = check_output_path(self.io_dict["out"]["output_crd_path"],"output_crd_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ BDRun module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        #self.tmp_folder = fu.create_unique_dir()
        #fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        #shutil.copy2(self.io_dict["in"]["input_pdb_path"], self.tmp_folder)

        # Command line
        # bd structure.ca.pdb 1000000 1e-15 1000 40 3.8 traj.crd > bd.log
        # itempsmax, dt, itsnap, const, r0
        self.cmd = [self.binary_path,
                PurePath(self.io_dict["in"]["input_pdb_path"]).name,
                str(self.time),
                str(self.dt),
                str(self.wfreq),
                "40", # Hardcoded "Const", see https://mmb.irbbarcelona.org/gitlab/adam/FlexServ/blob/master/bd/bd2.f#L51 
                "3.8", # Hardcoded "r0", see https://mmb.irbbarcelona.org/gitlab/adam/FlexServ/blob/master/bd/bd2.f#L52
                PurePath(self.io_dict["out"]["output_crd_path"]).name,
                '>', PurePath(self.io_dict["out"]["output_log_path"]).name
               ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            #self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def bd_run(input_pdb_path: str,
            output_log_path: str, output_crd_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`BDRun <flexserv.bd_run.BDRun>`flexserv.bd_run.BDRun class and
    execute :meth:`launch() <flexserv.bd_run.BDRun.launch>` method"""

    return BDRun( input_pdb_path=input_pdb_path,
                    output_log_path=output_log_path,
                    output_crd_path=output_crd_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generates protein conformational structures using the Brownian Dynamics method.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input PDB file. Accepted formats: pdb.')
    required_args.add_argument('--output_log_path', required=True, help='Output log file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_crd_path', required=True, help='Output ensemble file. Accepted formats: crd, mdcrd, inpcrd.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    bd_run(         input_pdb_path=args.input_pdb_path,
                    output_log_path=args.output_log_path,
                    output_crd_path=args.output_crd_path,
                    properties=properties)

if __name__ == '__main__':
    main()
