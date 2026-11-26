#!/usr/bin/env python3

"""Module containing the PCZunzip class and the command line interface."""
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcaunzip module."""

        # Command line
        # pcaunzip -i infile [-o outfile] [--pdb] [--verbose] [--help]
        # self.cmd = [self.binary_path,
        #             "-i", input_pcz,
        #             "-o", output_crd
        #             ]

        self.cmd = [self.binary_path,
                    "-i", self.stage_io_dict["in"]["input_pcz_path"],
                    "-o", self.stage_io_dict["out"]["output_crd_path"]
                    ]

        if self.verbose:
            self.cmd.append('-v')

        if self.pdb:
            self.cmd.append('--pdb')

        # Run Biobb block
        self.run_biobb()


pcz_unzip = launcher(PCZunzip)

if __name__ == '__main__':
    PCZunzip.main()
