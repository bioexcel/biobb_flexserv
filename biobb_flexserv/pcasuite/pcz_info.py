#!/usr/bin/env python3

"""Module containing the PCZinfo class and the command line interface."""
from typing import Optional
import json
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger


class PCZinfo(BiobbObject):
    """
    | biobb_flexserv PCZinfo
    | Extract PCA info (variance, Dimensionality) from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA info such as number of components, variance and dimensionality. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_info.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
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

            from biobb_flexserv.pcasuite.pcz_info import pcz_info

            pcz_info( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/pcz_info.json')

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

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_info module."""

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
        # temp_out_1 = str(Path(self.stage_io_dict.get("unique_dir", "")).joinpath("output1.dat"))
        # temp_out_2 = str(Path(self.stage_io_dict.get("unique_dir", "")).joinpath("output2.dat"))
        temp_out_1 = "output1.dat"
        temp_out_2 = "output2.dat"
        temp_out_1_path = unique_dir.joinpath(temp_out_1)
        temp_out_2_path = unique_dir.joinpath(temp_out_2)
        staged_output_json_path = unique_dir.joinpath(Path(self.stage_io_dict["out"]["output_json_path"]).name)

        # Command line
        # pczdump -i structure.ca.std.pcz --info -o pcz.info
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out_1,
        #             "--info", ';',
        #             self.binary_path,
        #             "-i", input_pcz,
        #             "-o", temp_out_2,
        #             "--evals"
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    "-i", PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
                    "-o", temp_out_1,
                    "--info", ';',
                    self.binary_path,
                    "-i", PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
                    "-o", temp_out_2,
                    "--evals"
                    ]

        # Run Biobb block
        self.run_biobb()

        # Parse output info
        # Title             : MC generated trajectory
        # Atoms             :       85
        # Vectors           :        4
        # Frames            :     1000
        # Total variance    :  1137.20
        # Explained variance:  1043.32
        # Quality           :    91.74%
        # Dimensionality    :       21
        # RMSd type         : Standard RMSd
        # Have atom names   : True
        info_dict = {}
        with open(temp_out_1_path, 'r') as file:
            for line in file:
                info = line.split(':')
                info_dict[info[0].strip().replace(' ', '_')] = info[1].strip()

        # Parse output evals
        # 744.201782
        # 170.061981
        # 89.214905
        # 39.836308
        info_dict['Eigen_Values'] = []
        info_dict['Eigen_Values_dimensionality_vs_total'] = []
        info_dict['Eigen_Values_dimensionality_vs_explained'] = []
        accum_tot = 0
        accum_exp = 0
        with open(temp_out_2_path, 'r') as file:
            for line in file:
                eval = float(line.strip())
                eval_var = (eval / float(info_dict['Total_variance']))*100
                accum_tot = accum_tot + eval_var
                eval_dim = (eval / float(info_dict['Explained_variance']))*100
                accum_exp = accum_exp + eval_dim
                info_dict['Eigen_Values'].append(eval)
                info_dict['Eigen_Values_dimensionality_vs_total'].append(accum_tot)
                info_dict['Eigen_Values_dimensionality_vs_explained'].append(accum_exp)

        with open(staged_output_json_path, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))

        # Copy files to host
        self.copy_to_host()

        # Remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pcz_info(input_pcz_path: str, output_json_path: str,
             properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`PCZinfo <flexserv.pcasuite.pcz_info>`flexserv.pcasuite.PCZinfo class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_info.launch>` method"""
    return PCZinfo(**dict(locals())).launch()


pcz_info.__doc__ = PCZinfo.__doc__
main = PCZinfo.get_main(pcz_info, "Extract PCA info from a compressed PCZ file.")

if __name__ == '__main__':
    main()
