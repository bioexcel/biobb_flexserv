#!/usr/bin/env python3

"""Module containing the PCZlindemann class and the command line interface."""
from typing import Optional
import json
from biobb_common.generic.biobb_object import BiobbObject, launcher


class PCZlindemann(BiobbObject):
    """
    | biobb_flexserv PCZlindemann
    | Extract Lindemann coefficient (an estimate of the solid-liquid behaviour of a protein) from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Eigen Vectors. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_lindemann.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **mask** (*str*) - (None) Residue mask, in the format ":resnum1, resnum2, resnum3" (e.g. ":10,21,33"). See https://mmb.irbbarcelona.org/software/pcasuite/ for the complete format specification.
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

            from biobb_flexserv.pcasuite.pcz_lindemann import pcz_lindemann
            prop = {
                'mask': ':10,12,15'
            }
            pcz_lindemann( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/lindemann_report.json',
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

        # Properties specific for BB

    def run(self):
        """Launches the execution of the FlexServ pcz_lindemann module."""

        # Temporary output
        # temp_out = str(Path(self.stage_io_dict.get("unique_dir", "")).joinpath("output.dat"))
        temp_out_path = self.create_tmp_file("_output.dat")
        temp_out = self.staged_path(temp_out_path)
        staged_output_json_path = self.sandbox_file("output_json_path")

        # Command line
        # pczdump -i structure.ca.std.pcz --lindemann -M ":2-86" -o lindemann_report.txt
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out,
        #             "--lindemann"
        #             ]

        self.cmd = [self.binary_path,
                    "-i", self.stage_io_dict["in"]["input_pcz_path"],
                    "-o", temp_out,
                    "--lindemann"
                    ]

        if self.mask:
            self.cmd.extend(["-M", self.mask])

        # Run Biobb block
        self.run_biobb()

        # Parse output Lindemann
        #  0.132891
        info_dict = {}
        with open(temp_out_path, 'r') as file:
            for line in file:
                info = float(line.strip())
                info_dict['lindemann'] = info

        with open(staged_output_json_path, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))


pcz_lindemann = launcher(PCZlindemann)

if __name__ == '__main__':
    PCZlindemann.main()
