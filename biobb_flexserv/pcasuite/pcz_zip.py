#!/usr/bin/env python3

"""Module containing the PCAzip class and the command line interface."""
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher


class PCZzip(BiobbObject):
    """
    | biobb_flexserv PCZzip
    | Wrapper of the pcazip tool from the PCAsuite FlexServ module.
    | Compress Molecular Dynamics (MD) trajectories using Principal Component Analysis (PCA) algorithms.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/structure.ca.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_crd_path (str): Input Trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/traj.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        output_pcz_path (str): Output compressed trajectory. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pcazip") pcazip binary path to be used.
            * **neigenv** (*int*) - (0) Number of generated eigenvectors
            * **variance** (*int*) - (None) Percentage of variance captured by the final set of eigenvectors
            * **verbose** (*bool*) - (False) Make output verbose
            * **gauss_rmsd** (*bool*) - (False) Use a gaussian RMSd for fitting
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

            from biobb_flexserv.pcasuite.pcz_zip import pcz_zip
            prop = {
                'variance': 90
            }
            pcz_zip( input_pdb_path='/path/to/pcazip_input.pdb',
                    input_crd_path='/path/to/pcazip_input.crd',
                    output_pcz_path='/path/to/pcazip_traj.pcz',
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

    def __init__(self, input_pdb_path: str, input_crd_path: str,
                 output_pcz_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcazip module."""

        # Command line
        # pcazip -p structure.ca.pdb -i traj.crd -o pcazip.pcz [-v] [-g] [-e nev] [-q variance]
        self.cmd = [self.binary_path,
                    "-p", self.stage_io_dict["in"]["input_pdb_path"],
                    "-i", self.stage_io_dict["in"]["input_crd_path"],
                    "-o", self.stage_io_dict["out"]["output_pcz_path"]
                    ]

        if self.verbose:
            self.cmd.append('-v')

        if self.gauss_rmsd:
            self.cmd.append('-g')

        if self.neigenv:
            self.cmd.append('-e')
            self.cmd.append(str(self.neigenv))

        if self.variance:
            self.cmd.append('-q')
            self.cmd.append(str(self.variance))

        # Run Biobb block
        self.run_biobb()


pcz_zip = launcher(PCZzip)

if __name__ == '__main__':
    PCZzip.main()
