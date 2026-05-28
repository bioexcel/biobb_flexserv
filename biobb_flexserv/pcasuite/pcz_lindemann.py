#!/usr/bin/env python3

"""Module containing the PCZlindemann class and the command line interface."""
from typing import Optional
import json
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger


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
            * **mask** (*str*) - ("all atoms") Residue mask, in the format ":resnum1, resnum2, resnum3" (e.g. ":10,21,33"). See https://mmb.irbbarcelona.org/software/pcasuite/ for the complete format specification.
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
        self.mask = properties.get('mask', '')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_lindemann module."""

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
        # pczdump -i structure.ca.std.pcz --lindemann -M ":2-86" -o lindemann_report.txt
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out,
        #             "--lindemann"
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    "-i", PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
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

        # Copy files to host
        self.copy_to_host()

        # Remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pcz_lindemann(input_pcz_path: str, output_json_path: str,
                  properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`PCZlindemann <flexserv.pcasuite.pcz_lindemann>`flexserv.pcasuite.PCZlindemann class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_lindemann.launch>` method"""
    return PCZlindemann(**dict(locals())).launch()


pcz_lindemann.__doc__ = PCZlindemann.__doc__
main = PCZlindemann.get_main(pcz_lindemann, "Extract Lindemann coefficients from a compressed PCZ file.")

if __name__ == '__main__':
    main()
