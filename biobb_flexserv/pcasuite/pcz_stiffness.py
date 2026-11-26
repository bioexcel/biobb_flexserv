#!/usr/bin/env python3

"""Module containing the PCZstiffness class and the command line interface."""
from typing import Optional
import json
import math
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcz_stiffness module."""

        # Temporary output
        # temp_out = str(Path(self.stage_io_dict.get("unique_dir", "")).joinpath("output.dat"))
        temp_out_path = self.create_tmp_file("_output.dat")
        temp_out = self.staged_path(temp_out_path)
        staged_output_json_path = self.sandbox_file("output_json_path")

        # Command line
        # pczdump -i structure.ca.std.pcz --stiffness -o pcz.stiffness
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out,
        #             "--stiffness={}".format(self.eigenvector),
        #             "--temperature={}".format(self.temperature)
        #             ]

        self.cmd = [self.binary_path,
                    "-i", self.stage_io_dict["in"]["input_pcz_path"],
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
                info_dict['stiffness'][row][row] = None
                info_dict['stiffness_log'].append(line_array_log)
                info_dict['stiffness_log'][row][row] = None
                row += 1

        with open(staged_output_json_path, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))


pcz_stiffness = launcher(PCZstiffness)

if __name__ == '__main__':
    PCZstiffness.main()
