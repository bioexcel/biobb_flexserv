#!/usr/bin/env python3

"""Module containing the dmd_run class and the command line interface."""
import argparse
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class DMDRun(BiobbObject):
    """
    | biobb_flexserv DMDRun
    | Wrapper of the Discrete Molecular Dynamics tool from the FlexServ module.
    | Generates protein conformational structures using the Discrete Molecular Dynamics (DMD) method.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/dmd_run_out.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_crd_path (str): Output ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/dmd_run_out.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
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
        self.binary_path = properties.get('binary_path', 'dmdgoopt')
        #self.dt = properties.get('dt', 1.D-12)
        self.dt = properties.get('dt', 1e-12)
        self.temperature = properties.get('temperature', 300)
        self.frames = properties.get('frames', 1000)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ BDRun module."""

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

        # Config file
        instructions_file = str(Path(self.stage_io_dict.get("unique_dir")).joinpath("dmd.in"))
        with open(instructions_file, 'w') as dmdin:

            dmdin.write("&INPUT\n")
            dmdin.write("  FILE9='{}',\n".format(input_pdb))
            dmdin.write("  FILE21='{}',\n".format(output_crd))
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
        self.cmd = [ 
                self.binary_path,
                '<', instructions_file,
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

def dmd_run(input_pdb_path: str,
            output_log_path: str, output_crd_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`DMDRun <flexserv.dmd_run.DMDRun>`flexserv.dmd_run.DMDRun class and
    execute :meth:`launch() <flexserv.dmd_run.DMDRun.launch>` method"""

    return DMDRun(  input_pdb_path=input_pdb_path,
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
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    dmd_run(        input_pdb_path=args.input_pdb_path,
                    output_log_path=args.output_log_path,
                    output_crd_path=args.output_crd_path,
                    properties=properties)

if __name__ == '__main__':
    main()
