#!/usr/bin/env python3

"""Module containing the dmd_run class and the command line interface."""
import argparse
import shutil, re, os
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.flexserv.bd_run as myself
from biobb_flexserv.flexserv.common import *

class DMDRun(BiobbObject):
    """
    | biobb_flexserv DMDRun
    | Wrapper of the Discrete Molecular Dynamics tool from the FlexServ module.
    | Generates protein conformational structures using the Discrete Molecular Dynamics (DMD) method.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_crd_path (str): Output ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("dmdgoopt") DMD binary path to be used.
            * **dt** (*float*) - (1e-12) Integration time (s)
            * **temperature** (*int*) - (300) Simulation temperature (K)
            * **frames** (*int*) - (1000) Number of frames in the final ensemble
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.flexserv.dmd_run import dmd_run
            prop = {
                'binary_path': 'dmdgoopt'
            }
            flexserv_run(input_pdb_path='/path/to/dmd_input.pdb',
                         output_log_path='/path/to/dmd_log.log',
                         output_crd_path='/path/to/dmd_ensemble.crd',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: FlexServ Discrete Molecular Dynamics
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
        self.binary_path = properties.get('binary_path', 'dmdgoopt')
        #self.dt = properties.get('dt', 1.D-12)
        self.dt = properties.get('dt', 1e-12)
        self.temperature = properties.get('temperature', 300)
        self.frames = properties.get('frames', 1000)

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
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
        instructions_file = str(PurePath(self.tmp_folder).joinpath("dmd.in"))
        output_file = str(PurePath(self.tmp_folder).joinpath("snapshots.crd"))
        output_log_file = str(PurePath(self.tmp_folder).joinpath("snapshots.log"))

        shutil.copy2(self.io_dict["in"]["input_pdb_path"], self.tmp_folder)

        with open(instructions_file, 'w') as dmdin:

            dmdin.write("&INPUT\n")
            dmdin.write("  FILE9='{}',\n".format(PurePath(self.io_dict["in"]["input_pdb_path"]).name))
            dmdin.write("  TSNAP={},\n".format(self.dt))
            dmdin.write("  NBLOC={},\n".format(self.frames))
            dmdin.write("  TEMP={},\n".format(self.temperature))
            dmdin.write("  RCUTGO=8,\n")
            dmdin.write("  RCA=0.5,\n")
            dmdin.write("  SIGMA=0.05,\n")
            dmdin.write("  SIGMAGO=0.1,\n")
            dmdin.write("  KKK=2839\n")
            dmdin.write("&END\n")

        # Command line
        # dmdgoopt < dmd.in > dmd.log
        self.cmd = ['cd', self.tmp_folder, ';', 
                self.binary_path,
                '<', "dmd.in",
                '>', "snapshots.log"
               ]

        # Run Biobb block
        self.run_biobb()

        # Copy output ensemble
        shutil.copy2(output_file, PurePath(self.io_dict["out"]["output_crd_path"]))
        shutil.copy2(output_log_file, PurePath(self.io_dict["out"]["output_log_path"]))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def dmd_run(input_pdb_path: str,
            output_log_path: str, output_crd_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`DMDRun <flexserv.dmd_run.DMDRun>`flexserv.dmd_run.DMDRun class and
    execute :meth:`launch() <flexserv.dmd_run.DMDRun.launch>` method"""

    return DMDRun( input_pdb_path=input_pdb_path,
                    output_log_path=output_log_path,
                    output_crd_path=output_crd_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generates protein conformational structures using the Discrete Molecular Dynamics method.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
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
