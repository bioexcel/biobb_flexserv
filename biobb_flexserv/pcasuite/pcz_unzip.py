#!/usr/bin/env python3

"""Module containing the PCZunzip class and the command line interface."""
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger


class PCZunzip(BiobbObject):
    """
    | biobb_flexserv PCZunzip
    | Wrapper of the pcaunzip tool from the PCAsuite FlexServ module.
    | Uncompress Molecular Dynamics (MD) trajectories compressed using Principal Component Analysis (PCA) algorithms.

    Args:
        input_pcz_path (str): Input compressed trajectory. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_crd_path (str): Output uncompressed trajectory. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pcaunzip") pcaunzip binary path to be used.
            * **verbose** (*bool*) - (False) Make output verbose
            * **pdb** (*bool*) - (False) Use PDB format for output trajectory
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

            from biobb_flexserv.pcasuite.pcz_unzip import pcz_unzip
            prop = {
                'pdb': False
            }
            pcz_unzip( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_crd_path='/path/to/pcazip_traj.crd',
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
                 output_crd_path: str, properties: Optional[dict] = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pcz_path': input_pcz_path},
            'out': {'output_crd_path': output_crd_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pcaunzip')
        self.verbose = properties.get('verbose', False)
        self.pdb = properties.get('pdb', False)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcaunzip module."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get("unique_dir", "")

        # Command line
        # pcaunzip -i infile [-o outfile] [--pdb] [--verbose] [--help]
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", output_crd
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    "-i", PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
                    "-o", PurePath(self.stage_io_dict["out"]["output_crd_path"]).name
                    ]

        if self.verbose:
            self.cmd.append('-v')

        if self.pdb:
            self.cmd.append('--pdb')

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pcz_unzip(input_pcz_path: str,
              output_crd_path: str,
              properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`PCZunzip <flexserv.pcasuite.PCZunzip>`flexserv.pcasuite.PCZunzip class and
    execute :meth:`launch() <flexserv.pcasuite.PCZunzip.launch>` method"""
    return PCZunzip(**dict(locals())).launch()


pcz_unzip.__doc__ = PCZunzip.__doc__
main = PCZunzip.get_main(pcz_unzip, "Uncompress Molecular Dynamics (MD) compressed trajectories using Principal Component Analysis (PCA) algorithms.")

if __name__ == '__main__':
    main()
