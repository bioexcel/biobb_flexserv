#!/usr/bin/env python3

"""Module containing the PCZsimilarity class and the command line interface."""
from typing import Optional
import json
import numpy as np
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher


class PCZsimilarity(BiobbObject):
    """
    | biobb_flexserv PCZsimilarity
    | Compute PCA similarity between two given compressed PCZ files.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path1 (str): Input compressed trajectory file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        input_pcz_path2 (str): Input compressed trajectory file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Similarity results. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_similarity.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **amplifying_factor** (*float*) - (None) common displacement (dx) along the different eigenvectors. If 0, the result is the absolute similarity index (dot product).
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
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

            from biobb_flexserv.pcasuite.pcz_similarity import pcz_similarity

            pcz_similarity( input_pcz_path1='/path/to/pcazip_input1.pcz',
                    input_pcz_path2='/path/to/pcazip_input2.pcz',
                    output_json_path='/path/to/pcz_similarity.json',
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

    def __init__(self, input_pcz_path1: str, input_pcz_path2: str,
                 output_json_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexServ pcz_similarity module."""

        # pczdump writes its outputs in a temporary folder of the sandbox
        tmp_dir = self.create_tmp_dir()
        staged_dir = self.staged_path(tmp_dir)
        pczs = (self.stage_io_dict["in"]["input_pcz_path1"], self.stage_io_dict["in"]["input_pcz_path2"])

        # Command line 1: the eigenvalues of both files
        # pczdump -i structure.ca.std.pcz --evals -o evals.txt
        self.cmd = [self.binary_path, "-i", pczs[0], "-o", f"{staged_dir}/evals_1", "--evals", ";",
                    self.binary_path, "-i", pczs[1], "-o", f"{staged_dir}/evals_2", "--evals"]
        self.run_biobb()
        evals_1, evals_2 = ([float(v) for v in Path(tmp_dir, f"evals_{i}").read_text().split()] for i in (1, 2))
        n = min(len(evals_1), len(evals_2))

        # Command line 2: the first n eigenvectors of both files
        # pczdump -i structure.ca.std.pcz --evec=1 -o evecs_1_pc1
        self.cmd = []
        for pc in range(1, n + 1):
            for i, pcz in enumerate(pczs, 1):
                self.cmd += [self.binary_path, "-i", pcz, "-o", f"{staged_dir}/evecs_{i}_pc{pc}", f"--evec={pc}", ";"]
        self.run_biobb()
        evecs_1, evecs_2 = ({f"pc{pc}": [float(v) for v in Path(tmp_dir, f"evecs_{i}_pc{pc}").read_text().split()]
                             for pc in range(1, n + 1)} for i in (1, 2))

        vectors_1, vectors_2 = np.array(list(evecs_1.values())), np.array(list(evecs_2.values()))
        if vectors_1.shape[1] != vectors_2.shape[1]:
            raise ValueError(f"The eigenvectors of the two pcz files have different sizes ({vectors_1.shape[1]} and "
                             f"{vectors_2.shape[1]} values): the files must have the same atoms")
        values_1, values_2 = np.array(evals_1), np.array(evals_2)
        # Squared inner products of the eigenvectors of the two files
        squared_dots = np.square(vectors_1 @ vectors_2.T)

        # Weighted Cross Product (WCP), DF implementation of the index of: Exploring the Essential Dynamics of B-DNA;
        # Alberto Perez, Jose Ramon Blas, Manuel Rueda, Jose Maria Lopez-Bes, Xavier de la Cruz and Modesto Orozco.
        # J. Chem. Theory Comput. 2005, 1. Amplifying factor: the n-th eigenvalue of the first file by default.
        factor2 = (values_1[n - 1] if self.amplifying_factor is None else self.amplifying_factor) ** 2
        weights_1, weights_2 = np.exp(-factor2 / values_1), np.exp(-factor2 / values_2)
        denominator = sum(np.sum((np.exp(-2 * factor2 / values) / weights.sum() ** 2) ** 2)
                          for values, weights in ((values_1, weights_1), (values_2, weights_2)))
        cross_weights = np.outer(weights_1[:n], weights_2[:n]) / (weights_1.sum() * weights_2.sum())
        wcp = 2 * np.sum(squared_dots * np.square(cross_weights)) / denominator
        # Absolute similarity index (Hess 2000, 2002) and RMSip (Root Mean Square Inner Product)
        dotp = squared_dots.sum() / n
        rmsip = np.sqrt(dotp)
        # RWSIP, Root Weighted Square Inner Product: Edvin Fuglebakk and others, Measuring and comparing structural
        # fluctuation patterns in large protein datasets, Bioinformatics 28(19), 2012, https://doi.org/10.1093/bioinformatics/bts445
        rwsip = np.sqrt(np.sum(squared_dots * np.outer(values_1[:n], values_2[:n])) / np.sum(values_1[:n] * values_2[:n]))

        info_dict = {'evals_1': evals_1, 'evals_2': evals_2, 'num_evals_min': n, 'evecs_1': evecs_1, 'evecs_2': evecs_2}
        for name, index in (('WCP', wcp), ('rmsip', rmsip), ('rwsip', rwsip), ('dotp', dotp)):
            info_dict[f'similarityIndex_{name}'] = float(f"{index:.3f}")
        with open(self.sandbox_file("output_json_path"), 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))


pcz_similarity = launcher(PCZsimilarity)

if __name__ == '__main__':
    PCZsimilarity.main()
