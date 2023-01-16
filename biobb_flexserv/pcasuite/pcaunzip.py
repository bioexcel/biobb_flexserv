#!/usr/bin/env python3

"""Module containing the PCAunzip class and the command line interface."""
import argparse
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

class PCAunzip(BiobbObject):
    """
    | biobb_flexserv PCAunzip
    | Wrapper of the pcaunzip tool from the PCAsuite FlexServ module.
    | Uncompress Molecular Dynamics (MD) trajectories compressed using Principal Component Analysis (PCA) algorithms.

    Args:
        input_pcz_path (str): Input compressed trajectory. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_crd_path (str): Output uncompressed trajectory. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pcaunzip") pcaunzip binary path to be used.
            * **verbose** (*bool*) - (False) Make output verbose
            * **pdb** (*bool*) - (False) Use PDB format for output trajectory
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcaunzip import pcaunzip
            prop = {
                'pdb': False
            }
            pcaunzip( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_crd_path='/path/to/pcazip_traj.crd',
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
    def __init__(self, input_pcz_path: str, 
    output_crd_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pcz_path': input_pcz_path,
             },
            'out': {    
                    'output_crd_path': output_crd_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pcaunzip')
        self.verbose = properties.get('verbose', False)
        self.pdb = properties.get('pdb', False)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcaunzip module."""

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
        output_file_name = PurePath(self.io_dict["out"]["output_crd_path"]).name
        output_file = str(PurePath(self.tmp_folder).joinpath(output_file_name))

        # Command line
        # pcaunzip -i infile [-o outfile] [--pdb] [--verbose] [--help]
        self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_file_name 
               ]
 
        if self.verbose:
            self.cmd.append('-v')

        if self.pdb:
            self.cmd.append('--pdb')

        # Run Biobb block
        self.run_biobb()

        # Copy output trajectory
        shutil.copy2(output_file, PurePath(self.io_dict["out"]["output_crd_path"]))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            self.tmp_folder
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def pcaunzip(input_pcz_path: str, 
            output_crd_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCAunzip <flexserv.pcasuite.pcaunzip>`flexserv.pcasuite.PCAunzip class and
    execute :meth:`launch() <flexserv.pcasuite.pcaunzip.launch>` method"""

    return PCAunzip(  input_pcz_path=input_pcz_path,
                    output_crd_path=output_crd_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Uncompress Molecular Dynamics (MD) compressed trajectories using Principal Component Analysis (PCA) algorithms.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_crd_path', required=True, help='Output trajectory file. Accepted formats: crd, mdcrd, inpcrd, pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcaunzip(       input_pcz_path=args.input_pcz_path,
                    output_crd_path=args.output_crd_path,
                    properties=properties)

if __name__ == '__main__':
    main()
