#!/usr/bin/env python3

"""Module containing the PCAzip class and the command line interface."""
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class PCZzip(BiobbObject):
    """
    | biobb_flexserv PCZzip
    | Wrapper of the pcazip tool from the PCAsuite FlexServ module.
    | Compress Molecular Dynamics (MD) trajectories using Principal Component Analysis (PCA) algorithms.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_crd_path (str): Input Trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        output_pcz_path (str): Output compressed trajectory. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
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

            from biobb_flexserv.pcasuite.pcz_zip import pcz_zip
            prop = {
                'variance': 90
            }
            pcz_zip( input_pdb_path='/path/to/pcazip_input.pdb',
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
        self.locals_var_dict = locals().copy()

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
        #self.variance = properties.get('variance', 90)
        self.variance = properties.get('variance')
        self.verbose = properties.get('verbose', False)
        self.gauss_rmsd = properties.get('gauss_rmsd', False)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcazip module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        try:
            # Using rel paths to shorten the amount of characters due to fortran path length limitations
            input_pdb = str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd()))
            input_crd = str(Path(self.stage_io_dict["in"]["input_crd_path"]).relative_to(Path.cwd()))
            output_pcz = str(Path(self.stage_io_dict["out"]["output_pcz_path"]).relative_to(Path.cwd()))
        except ValueError:
            # Container or remote case
            input_pdb = self.stage_io_dict["in"]["input_pdb_path"]
            input_crd = self.stage_io_dict["in"]["input_crd_path"]
            output_pcz = self.stage_io_dict["out"]["output_pcz_path"]

        # Command line
        # pcazip -i infile -o outfile -n natoms
        # [-v] [--mask maskfile] [-e nev] [-q qual] [--pdb pdbfile]
        self.cmd = [self.binary_path,
                "-p", input_pdb,
                "-i", input_crd,
                "-o", output_pcz
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

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def pcz_zip(input_pdb_path: str, input_crd_path: str,
            output_pcz_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZzip <flexserv.pcasuite.PCZzip>`flexserv.pcasuite.PCZzip class and
    execute :meth:`launch() <flexserv.pcasuite.PCZzip.launch>` method"""

    return PCZzip(  input_pdb_path=input_pdb_path,
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
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_zip(         input_pdb_path=args.input_pdb_path,
                    input_crd_path=args.input_crd_path,
                    output_pcz_path=args.output_pcz_path,
                    properties=properties)

if __name__ == '__main__':
    main()
