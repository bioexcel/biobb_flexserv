#!/usr/bin/env python3

"""Module containing the PCZevecs class and the command line interface."""
import argparse
import shutil
import json
import math
from pathlib import PurePath
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger


class PCZevecs(BiobbObject):
    """
    | biobb_flexserv PCZevecs
    | Extract PCA Eigen Vectors from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Eigen Vectors. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_evecs.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (1) PCA mode (eigenvector) from which to extract eigen vectors.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcz_evecs import pcz_evecs

            prop = {
                'eigenvector': 1
            }

            pcz_evecs( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/pcz_evecs.json',
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
                 output_json_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pcz_path': input_pcz_path},
            'out': {'output_json_path': output_json_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pczdump')
        self.eigenvector = properties.get('eigenvector', 1)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_evecs module."""

        # Setup Biobb
        if self.check_restart():
            return 0
        # self.stage_files()

        # Internal file paths
        # try:
        #     # Using rel paths to shorten the amount of characters due to fortran path length limitations
        #     input_pcz = str(Path(self.stage_io_dict["in"]["input_pcz_path"]).relative_to(Path.cwd()))
        #     output_json = str(Path(self.stage_io_dict["out"]["output_json_path"]).relative_to(Path.cwd()))
        # except ValueError:
        #     # Container or remote case
        #     input_pcz = self.stage_io_dict["in"]["input_pcz_path"]
        #     output_json = self.stage_io_dict["out"]["output_json_path"]

        # Manually creating a Sandbox to avoid issues with input parameters buffer overflow:
        #   Long strings defining a file path makes Fortran or C compiled programs crash if the string
        #   declared is shorter than the input parameter path (string) length.
        #   Generating a temporary folder and working inside this folder (sandbox) fixes this problem.
        #   The problem was found in Galaxy executions, launching Singularity containers (May 2023).

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        shutil.copy2(self.io_dict["in"]["input_pcz_path"], self.tmp_folder)

        # Temporary output
        # temp_out = str(Path(self.stage_io_dict.get("unique_dir")).joinpath("output.dat"))
        temp_out = "output.dat"
        temp_json = "output.json"

        # Command line
        # pczdump -i structure.ca.std.pcz --evecs -o pcz.evecs
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out,
        #             "--evec={}".format(self.eigenvector)
        #             ]

        self.cmd = ['cd', self.tmp_folder, ';',
                    self.binary_path,
                    '-i', PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                    '-o', temp_out,
                    "--evec={}".format(self.eigenvector)
                    ]

        # Run Biobb block
        self.run_biobb()

        # Parse output evecs
        #  0.180  -0.069   0.168   0.204  -0.054   0.235   0.145  -0.001   0.260   0.183
        # -0.041   0.231   0.174  -0.077   0.144   0.097  -0.022   0.143   0.069   0.008

        info_dict = {}
        info_dict['evecs'] = []
        with open(PurePath(self.tmp_folder).joinpath(temp_out), 'r') as file:
            for line in file:
                info = line.strip().split(' ')
                for nums in info:
                    if nums:
                        info_dict['evecs'].append(nums)

        # Computing Projections
        info_dict['projs'] = []
        module = 1
        proj = 0
        for num in info_dict['evecs']:
            val = float(num) * float(num)
            proj = proj + val
            if module % 3 == 0:
                proj = math.sqrt(proj)
                module = 1
                info_dict['projs'].append(float("{:.4f}".format(proj)))
                proj = 0
            else:
                module = module + 1

        with open(PurePath(self.tmp_folder).joinpath(temp_json), 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))

        # Copy outputs from temporary folder to output path
        shutil.copy2(PurePath(self.tmp_folder).joinpath(temp_json), PurePath(self.io_dict["out"]["output_json_path"]))

        # Copy files to host
        # self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            # self.stage_io_dict.get("unique_dir"),
            self.tmp_folder
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pcz_evecs(input_pcz_path: str, output_json_path: str,
              properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZevecs <flexserv.pcasuite.pcz_evecs>`flexserv.pcasuite.PCZevecs class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_evecs.launch>` method"""

    return PCZevecs(input_pcz_path=input_pcz_path,
                    output_json_path=output_json_path,
                    properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Extract PCA Eigen Vectors from a compressed PCZ file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_json_path', required=True, help='Output json file with PCA evecs. Accepted formats: json.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_evecs(input_pcz_path=args.input_pcz_path,
              output_json_path=args.output_json_path,
              properties=properties)


if __name__ == '__main__':
    main()
