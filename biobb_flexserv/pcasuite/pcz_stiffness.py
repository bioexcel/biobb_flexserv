#!/usr/bin/env python3

"""Module containing the PCZstiffness class and the command line interface."""
from typing import Optional
import json
import math
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger


class PCZstiffness(BiobbObject):
    """
    | biobb_flexserv PCZstiffness
    | Extract PCA stiffness from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Stiffness. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_stiffness.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (0) PCA mode (eigenvector) from which to extract stiffness.
            * **temperature** (*int*) - (300) Temperature with which compute the apparent stiffness.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('afandiadib/ambertools:serial') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_working_dir** (*str*) - (None) Container working directory definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcz_stiffness import pcz_stiffness

            prop = {
                'eigenvector': 1
            }

            pcz_stiffness( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/pcz_stiffness.json',
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
                 output_json_path: str, properties: Optional[dict] = None, **kwargs) -> None:

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
        self.eigenvector = properties.get('eigenvector', 0)
        self.temperature = properties.get('temperature', 300)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_stiffness module."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get("unique_dir", "")

        unique_dir = Path(self.stage_io_dict.get("unique_dir", ""))

        # Temporary output
        # temp_out = str(Path(self.stage_io_dict.get("unique_dir", "")).joinpath("output.dat"))
        temp_out = "output.dat"
        temp_out_path = unique_dir.joinpath(temp_out)
        staged_output_json_path = unique_dir.joinpath(Path(self.stage_io_dict["out"]["output_json_path"]).name)

        # Command line
        # pczdump -i structure.ca.std.pcz --stiffness -o pcz.stiffness
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out,
        #             "--stiffness={}".format(self.eigenvector),
        #             "--temperature={}".format(self.temperature)
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    "-i", PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
                    "-o", temp_out,
                    "--stiff={}".format(self.eigenvector),
                    "--temperature={}".format(self.temperature)
                    ]

        # Run Biobb block
        self.run_biobb()

        # Parse output stiffness
        info_dict = {}
        info_dict['stiffness'] = []
        info_dict['stiffness_log'] = []
        row = 0
        with open(temp_out_path, 'r') as file:
            for line in file:
                info = line.strip().split(',')
                line_array = []
                line_array_log = []
                for nums in info:
                    if nums:
                        line_array.append(float(nums))
                        if float(nums) != 0:
                            line_array_log.append(math.log10(float(nums)))
                        else:
                            line_array_log.append(float(nums))

                info_dict['stiffness'].append(line_array)
                info_dict['stiffness'][row][row] = float('inf')
                info_dict['stiffness_log'].append(line_array_log)
                info_dict['stiffness_log'][row][row] = float('inf')
                row += 1

        with open(staged_output_json_path, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))

        # Copy files to host
        self.copy_to_host()

        # Remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pcz_stiffness(input_pcz_path: str, output_json_path: str,
                  properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`PCZstiffness <flexserv.pcasuite.pcz_stiffness>`flexserv.pcasuite.PCZstiffness class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_stiffness.launch>` method"""
    return PCZstiffness(**dict(locals())).launch()


pcz_stiffness.__doc__ = PCZstiffness.__doc__
main = PCZstiffness.get_main(pcz_stiffness, "Extract PCA Stiffness from a compressed PCZ file.")

if __name__ == '__main__':
    main()
