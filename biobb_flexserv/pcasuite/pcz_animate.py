#!/usr/bin/env python3

"""Module containing the PCZanimate class and the command line interface."""
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject, launcher


class PCZanimate(BiobbObject):
    """
    | biobb_flexserv PCZanimate
    | Extract PCA animations from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_crd_path (str): Output PCA animated trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip_anim1.pdb>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (1) Eigenvector to be used for the animation
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

            from biobb_flexserv.pcasuite.pcz_animate import pcz_animate
            prop = {
                'eigenvector': 1,
                'pdb': True
            }
            pcz_animate( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_crd_path='/path/to/animated_traj.pdb',
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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcz_animate module."""

        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get("unique_dir", "")

        # Command line
        # pczdump -i structure.ca.std.pcz --anim=1 --pdb -o anim_1.pdb
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", output_crd,
        #             "--anim={}".format(self.eigenvector)
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    '-i', PurePath(self.stage_io_dict["in"]["input_pcz_path"]).name,
                    '-o', PurePath(self.stage_io_dict["out"]["output_crd_path"]).name,
                    "--anim={}".format(self.eigenvector)
                    ]

        if self.pdb:
            self.cmd.append('--pdb')

        # Run Biobb block
        self.run_biobb()


pcz_animate = launcher(PCZanimate)

if __name__ == '__main__':
    PCZanimate.main()
