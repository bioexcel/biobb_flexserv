#!/usr/bin/env python3

"""Module containing the nma_run class and the command line interface."""
import argparse
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

class NMARun(BiobbObject):
    """
    | biobb_flexserv NMARun
    | Wrapper of the Normal Mode Analysis tool from the FlexServ module.
    | Generates protein conformational structures using the Normal Mode Analysis (NMA) method.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_crd_path (str): Output ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("bd") BD binary path to be used.
            * **frames** (*int*) - (1000) Number of frames in the final ensemble
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.flexserv.bd_run import bd_run
            prop = {
                'binary_path': 'diaghess'
            }
            flexserv_run(input_pdb_path='/path/to/nma_input.pdb',
                         output_log_path='/path/to/nma_log.log',
                         output_crd_path='/path/to/nma_ensemble.crd',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: FlexServ Normal Mode Analysis
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
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path },
            'out': {    'output_log_path': output_log_path,
                        'output_crd_path': output_crd_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'diaghess')
        self.frames = properties.get('frames', 1000)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ NMARun module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
        output_file = str(PurePath(self.tmp_folder).joinpath("snapshots.crd"))
        output_log_file = str(PurePath(self.tmp_folder).joinpath("snapshots.log"))

        shutil.copy2(self.io_dict["in"]["input_pdb_path"], self.tmp_folder)

        # Command line
        #nmanu.pl structure.ca.pdb hessian.dat 1 0 40
        #diaghess
        #mc-eigen.pl eigenvec.dat > file.proj
        #pca_anim_mc.pl -pdb structure.ca.pdb -evec eigenvec.dat -i file.proj -n 50 -pout traj.crd
        self.cmd = ['cd', self.tmp_folder, ';', 
                "nmanu.pl ",
                PurePath(self.io_dict["in"]["input_pdb_path"]).name,
                "hessian.dat 1 0 40;",
                self.binary_path,
                "; mc-eigen.pl eigenvec.dat > file.proj",
                "; pca_anim_mc.pl -pdb",
                PurePath(self.io_dict["in"]["input_pdb_path"]).name,
                " -evec eigenvec.dat -i file.proj -n ",
                str(self.frames),
                " -pout",  "snapshots.crd",
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
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            self.tmp_folder
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def nma_run(input_pdb_path: str,
            output_log_path: str, output_crd_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`NMARun <flexserv.nma_run.NMARun>`flexserv.nma_run.NMARun class and
    execute :meth:`launch() <flexserv.nma_run.NMARun.launch>` method"""

    return NMARun( input_pdb_path=input_pdb_path,
                    output_log_path=output_log_path,
                    output_crd_path=output_crd_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generates protein conformational structures using the Normal Mode Analysis method.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input PDB file. Accepted formats: pdb.')
    required_args.add_argument('--output_log_path', required=True, help='Output log file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_crd_path', required=True, help='Output ensemble file. Accepted formats: crd, mdcrd, inpcrd.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    nma_run(        input_pdb_path=args.input_pdb_path,
                    output_log_path=args.output_log_path,
                    output_crd_path=args.output_crd_path,
                    properties=properties)

if __name__ == '__main__':
    main()
