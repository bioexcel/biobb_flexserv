#!/usr/bin/env python3

"""Module containing the PCZevecs class and the command line interface."""
from typing import Optional
import json
import math
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('afandiadib/ambertools:serial') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

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
                 output_json_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcz_evecs module."""

        # Temporary output
        temp_out_path = self.create_tmp_file("_output.dat")
        temp_out = self.staged_path(temp_out_path)
        staged_output_json_path = self.sandbox_file("output_json_path")

        # Command line
        # pczdump -i structure.ca.std.pcz --evec=1 -o pcz.evecs
        self.cmd = [self.binary_path,
                    '-i', self.stage_io_dict["in"]["input_pcz_path"],
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
        with open(temp_out_path, 'r') as file:
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

        with open(staged_output_json_path, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))


pcz_evecs = launcher(PCZevecs)

if __name__ == '__main__':
    PCZevecs.main()
