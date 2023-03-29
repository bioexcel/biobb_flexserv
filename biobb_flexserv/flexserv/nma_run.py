#!/usr/bin/env python3

"""Module containing the nma_run class and the command line interface."""
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class NMARun(BiobbObject):
    """
    | biobb_flexserv NMARun
    | Wrapper of the Normal Mode Analysis tool from the FlexServ module.
    | Generates protein conformational structures using the Normal Mode Analysis (NMA) method.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/nma_run_out.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_crd_path (str): Output ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/nma_run_out.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("bd") BD binary path to be used.
            * **frames** (*int*) - (1000) Number of frames in the final ensemble
            * **nvecs** (*int*) - (50) Number of vectors to take into account for the ensemble generation
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
        self.nvecs = properties.get('nvecs', 50)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ NMARun module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Internal file paths
        try:
            # Using rel paths to shorten the amount of characters due to fortran path length limitations
            input_pdb = str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd()))
            output_crd = str(Path(self.stage_io_dict["out"]["output_crd_path"]).relative_to(Path.cwd()))
            output_log = str(Path(self.stage_io_dict["out"]["output_log_path"]).relative_to(Path.cwd()))
        except ValueError:
            # Container or remote case
            input_pdb = self.stage_io_dict["in"]["input_pdb_path"]
            output_crd = self.stage_io_dict["out"]["output_crd_path"]
            output_log = self.stage_io_dict["out"]["output_log_path"]

        # Command line
        #nmanu.pl structure.ca.pdb hessian.dat 1 0 40
        #diaghess
        #mc-eigen.pl eigenvec.dat > file.proj
        #pca_anim_mc.pl -pdb structure.ca.pdb -evec eigenvec.dat -i file.proj -n 50 -pout traj.crd
        self.cmd = [ 
                "nmanu.pl ",
                input_pdb,
                "hessian.dat 1 0 40;",
                self.binary_path,
                "; mc-eigen-mdweb.pl eigenvec.dat ", str(self.frames), " > file.proj",
                "; pca_anim_mc.pl -pdb",
                input_pdb,
                " -evec eigenvec.dat -i file.proj -n ",
                str(self.nvecs),
                " -pout",  output_crd,
                '>', output_log
               ]

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
