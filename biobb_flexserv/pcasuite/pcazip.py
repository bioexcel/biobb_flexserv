#!/usr/bin/env python3

"""Module containing the PCAzip class and the command line interface."""
import argparse
import shutil, re, os
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.pcasuite.pcazip as myself
from biobb_flexserv.pcasuite.common import *

class PCAzip(BiobbObject):
    """
    | biobb_flexserv PCAzip
    | Wrapper of the pcazip tool from the PCAsuite FlexServ module.
    | Compress Molecular Dynamics (MD) trajectories using Principal Component Analysis (PCA) algorithms.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_crd_path (str): Input Trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        output_pcz_path (str): Output compressed trajectory. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip.ref.pcz>`_. Accepted formats: pcz (edam:format_3874).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pcazip") pcazip binary path to be used.
            * **neigenv** (*int*) - (0) Number of generated eigenvectors
            * **variance** (*int*) - (90) Percentage of variance captured by the final set of eigenvectors
            * **verbose** (*bool*) - (False) Make output verbose
            * **gauss_rmsd** (*bool*) - (False) Use a gaussian RMSd for fitting
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcazip import pcazip
            prop = {
                'variance': 90
            }
            pcazip( input_pdb_path='/path/to/pcazip_input.pdb',
                    input_crd_path='/path/to/pcazip_input.crd',
                    output_pcz_path='/path/to/pcazip_traj.pcz',
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
    def __init__(self, input_pdb_path: str, input_crd_path: str, 
    output_pcz_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path,
                    'input_crd_path': input_crd_path
             },
            'out': {    
                    'output_pcz_path': output_pcz_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pcazip')
        self.neigenv = properties.get('neigenv', 0)
        self.variance = properties.get('variance', 90)
        self.verbose = properties.get('verbose', False)
        self.gauss_rmsd = properties.get('gauss_rmsd', False)

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, out_err):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_crd_path"] = check_input_path(self.io_dict["in"]["input_crd_path"], "input_crd_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pcz_path"] = check_output_path(self.io_dict["out"]["output_pcz_path"],"output_pcz_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcazip module."""

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
        shutil.copy2(self.io_dict["in"]["input_pdb_path"], self.tmp_folder)
        shutil.copy2(self.io_dict["in"]["input_crd_path"], self.tmp_folder)

        # Defining output files in temporary folder
        output_file_name = PurePath(self.io_dict["out"]["output_pcz_path"]).name
        output_file = str(PurePath(self.tmp_folder).joinpath(output_file_name))

        # Command line
        # pcazip -i infile -o outfile -n natoms
        # [-v] [--mask maskfile] [-e nev] [-q qual] [--pdb pdbfile]
        self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-p", str(PurePath(self.io_dict["in"]["input_pdb_path"])),
                "-i", str(PurePath(self.io_dict["in"]["input_crd_path"])),
                "-o", output_file_name
               ]
 
        if self.verbose:
            self.cmd.append('-v')

        if self.gauss_rmsd:
            self.cmd.append('-g')

        if self.neigenv:
            self.cmd.append('-e')
            self.cmd.append(str(self.neigenv))
 
        if self.variance:
            self.cmd.append('-q')
            self.cmd.append(str(self.variance))

        # Run Biobb block
        self.run_biobb()

        # Copy output trajectory
        shutil.copy2(output_file, PurePath(self.io_dict["out"]["output_pcz_path"]))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def pcazip(input_pdb_path: str, input_crd_path: str,
            output_pcz_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCAzip <flexserv.pcasuite.pcazip>`flexserv.pcasuite.PCAzip class and
    execute :meth:`launch() <flexserv.pcasuite.pcazip.launch>` method"""

    return PCAzip(  input_pdb_path=input_pdb_path,
                    input_crd_path=input_crd_path,
                    output_pcz_path=output_pcz_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Compress Molecular Dynamics (MD) trajectories using Principal Component Analysis (PCA) algorithms.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input PDB file. Accepted formats: pdb.')
    required_args.add_argument('--input_crd_path', required=True, help='Input trajectory file. Accepted formats: crd, mdcrd, inpcrd.')
    required_args.add_argument('--output_pcz_path', required=True, help='Output compressed trajectory file. Accepted formats: pcz.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcazip(         input_pdb_path=args.input_pdb_path,
                    input_crd_path=args.input_crd_path,
                    output_pcz_path=args.output_pcz_path,
                    properties=properties)

if __name__ == '__main__':
    main()
