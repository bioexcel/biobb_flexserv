#!/usr/bin/env python3

"""Module containing the PCZbfactor class and the command line interface."""
import argparse
import shutil, re, os
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.pcasuite.pcz_bfactor as myself
from biobb_flexserv.pcasuite.common import *

class PCZbfactor(BiobbObject):
    """
    | biobb_flexserv PCZbfactor
    | Extract residue bfactors x PCA mode from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_dat_path (str): Output Bfactor x residue x PCA mode file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/bfactors.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330), csv (edam:format_3752).
        output_pdb_path (str) (Optional): Output PDB with Bfactor x residue x PCA mode file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/bfactors.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (0) PCA mode (eigenvector) from which to extract bfactor values per residue (0 means average over all modes).
            * **pdb** (*bool*) - (False) Generate a PDB file with the computed bfactors (to be easily represented with colour scale) 
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcz_bfactor import pcz_bfactor
            prop = {
                'eigenvector': 1,
                'pdb': True
            }
            pcz_bfactor( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_dat_path='/path/to/bfactors_mode1.dat',
                    output_pdb_path='/path/to/bfactors_mode1.pdb',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: FlexServ PCAsuite
            * version: >=1.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pcz_path: str, output_dat_path: str,
    output_pdb_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': { 
                'input_pcz_path': input_pcz_path
             },
            'out': {    
                'output_dat_path': output_dat_path,
                'output_pdb_path': output_pdb_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pczdump')
        self.eigenvector = properties.get('eigenvector', 1)
        self.pdb = properties.get('pdb', False)

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, out_err):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pcz_path"] = check_input_path(self.io_dict["in"]["input_pcz_path"], "input_pcz_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_dat_path"] = check_output_path(self.io_dict["out"]["output_dat_path"],"output_dat_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", True, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_bfactor module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        # These BBs need a temporary folder as pcasuite does not allow for long input paths
        # e.g. pczaunzip -i /Users/user/BioBB/Dev/biobb_flexserv/biobb_flexserv/test/data/pcasuite/pcazip.pcz
        #      gives --> "Illegal instruction: 4"
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Copying input files to temporary folder
        shutil.copy2(self.io_dict["in"]["input_pcz_path"], self.tmp_folder)

        # Defining output files in temporary folder
        output_dat_file_name = PurePath(self.io_dict["out"]["output_dat_path"]).name
        output_dat_file = str(PurePath(self.tmp_folder).joinpath(output_dat_file_name))
        output_pdb_file_name = PurePath(self.io_dict["out"]["output_pdb_path"]).name
        output_pdb_file = str(PurePath(self.tmp_folder).joinpath(output_pdb_file_name))

        # Command line (1: dat file)
        # pczdump -i structure.ca.std.pcz --fluc=1 -o bfactor_1.dat
        self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_dat_file_name,
                "--bfactor",
                "--fluc={}".format(self.eigenvector)
               ]
  
        # Run Biobb block
        self.run_biobb()

        if self.pdb:
            # Command line (2: pdb file)
            # pczdump -i structure.ca.std.pcz --fluc=1 --pdb -o bfactor_1.pdb
            self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_pdb_file_name,
                "--bfactor",
                "--fluc={}".format(self.eigenvector),
                "--pdb"
               ]

            # Run Biobb block
            self.run_biobb()

        # Copy output trajectory
        shutil.copy2(output_dat_file, PurePath(self.io_dict["out"]["output_dat_path"]))

        if self.pdb:
            shutil.copy2(output_pdb_file, PurePath(self.io_dict["out"]["output_pdb_path"]))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def pcz_bfactor(input_pcz_path: str, output_dat_path: str, output_pdb_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZbfactor <flexserv.pcasuite.pcz_bfactor>`flexserv.pcasuite.PCZbfactor class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_bfactor.launch>` method"""

    return PCZbfactor(  
                    input_pcz_path=input_pcz_path,
                    output_dat_path=output_dat_path,
                    output_pdb_path=output_pdb_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Extract residue bfactors x PCA mode from a compressed PCZ file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_dat_path', required=True, help='Output Bfactor x residue x PCA mode file. Accepted formats: dat, txt, csv.')
    required_args.add_argument('--output_pdb_path', required=False, help='Output PDB with Bfactor x residue x PCA mode file. Accepted formats: pdb.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_bfactor(         input_pcz_path=args.input_pcz_path,
                    output_dat_path=args.output_dat_path,
                    output_pdb_path=args.output_pdb_path,
                    properties=properties)

if __name__ == '__main__':
    main()
