#!/usr/bin/env python3

"""Module containing the PCZsimilarity class and the command line interface."""
import argparse
import json
import numpy as np
from pathlib import Path
from math import exp
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

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
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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
    output_json_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 
                'input_pcz_path1': input_pcz_path1,
                'input_pcz_path2': input_pcz_path2
             },
            'out': {    
                'output_json_path': output_json_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pczdump')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    # Check two eigenvectors to be compatible for dot product
    # i.e. same number of vectors and values per vector
    def are_compatible (self,eigenvectors_1, eigenvectors_2): 
        # Check the number of eigenvectors and the number of values in both eigenvectors to match
        if len(eigenvectors_1) != len(eigenvectors_2):
            print('WARNING: Number of eigenvectors does not match')
            return False
        if len(eigenvectors_1[0]) != len(eigenvectors_2[0]):
            print('WARNING: Number of values in eigenvectors does not match')
            return False
        return True

    # Get the weighted cross product between eigenvectors
    # This is meant to compare PCA results for molecular dynamics structural conformations
    # The number of eigenvectors to be compared may be specified. All (0) by default
    # DISCLAIMER: This code has been translated from a perl script signed by Alberto Perez (13/09/04)
    def get_similarity_index (self, 
        eigenvalues_1, eigenvectors_1, 
        eigenvalues_2, eigenvectors_2):

        amplifying_factor = 0

        # Check the number of eigenvectors and the number of values in both eigenvectors to match
        if not self.are_compatible(eigenvectors_1, eigenvectors_2):
            raise SystemExit('Eigenvectors are not compatible')
        
        # Find out the total number of eigenvectors
        # Set the number of eigenvectors to be analyzed in case it is not set or it exceeds the total
        eigenvectors_number = min(len(eigenvectors_1),len(eigenvectors_2))

        # Find out the number of atoms in the structure
        # Eigenvectors are atom coordinates and each atom has 3 coordinates (x, y, z)
        if len(eigenvectors_1[0]) % 3 != 0:
            raise SystemExit('Something is wrong with eigenvectors since number of values is not divisor of 3')
        atom_number = int( len(eigenvectors_1[0]) / 3 )

        # Get the denominator
        cte1 = part1 = cte2 = part2 = 0
        for eigenvalue in eigenvalues_1:
            cte1 += exp(-1 / eigenvalue * amplifying_factor)
            part1 += exp(-2 / eigenvalue * amplifying_factor) ** 2
        for eigenvalue in eigenvalues_2:
            cte2 += exp(-1 / eigenvalue * amplifying_factor)
            part2 += exp(-2 / eigenvalue * amplifying_factor) ** 2
        denominator = part1 * cte2 * cte2 / cte1 / cte1 + part2 * cte1 * cte1 / cte2 / cte2

        # Get all eigenvector values together
        eigenvector_values_1 = [ v for ev in eigenvectors_1 for v in ev ]
        eigenvector_values_2 = [ v for ev in eigenvectors_2 for v in ev ]

        # IDK what it is doing now
        total_summatory = 0
        for i in range(eigenvectors_number):
            for j in range(eigenvectors_number):
                #Array has vectors in increasing order of vap, get last one first
                a = (eigenvectors_number - 1 - i) * atom_number * 3
                b = (eigenvectors_number - i) * atom_number * 3 - 1
                c = (eigenvectors_number - 1 - j) * atom_number * 3
                d = (eigenvectors_number - j) * atom_number * 3 - 1
                temp1 = eigenvector_values_1[a:b]
                temp2 = eigenvector_values_2[c:d]
                if len(temp1) != len(temp2):
                    raise ValueError("Projection of vectors of different size!!")
                # Project the two vectors
                add = 0
                for k, value_1 in enumerate(temp1):
                    value_2 = temp2[k]
                    add += value_1 * value_2
                add = add * exp(-1 / eigenvalues_1[i] * amplifying_factor - 1 / eigenvalues_2[j] * amplifying_factor)
                add2 = add ** 2
                total_summatory += add2
        
        similarity_index = total_summatory * 2 / denominator
        return similarity_index

    # Get the dot product matrix of two eigenvectors
    def dot_product (self, eigenvectors_1, eigenvectors_2):
        # Check the number of eigenvectors and the number of values in both eigenvectors to match
        if not self.are_compatible(eigenvectors_1, eigenvectors_2):
            raise SystemExit('Eigenvectors are not compatible')
        # Get the number of eigenvectors
        n_components = len(eigenvectors_1)
        # Get the dot product
        dpm = np.dot(eigenvectors_1, np.transpose(eigenvectors_2))
        return dpm

    # Get the subspace overlap
    # DANI: Es como el similarity index pero sin utilizar los eigenvalues y sin toda la parte de los weights, creo
    def get_subspace_overlap (self, eigenvectors_1, eigenvectors_2):
        # Get the number of eigenvectors
        n_components = len(eigenvectors_1)
        # Get the dot product
        dpm = self.dot_product(eigenvectors_1, eigenvectors_2)
        print(dpm)
        sso = np.sqrt((dpm * dpm).sum() / n_components)
        #sso = (dpm * dpm).sum() / n_components
        return sso

    def get_rwsip (self, 
        eigenvalues_1, eigenvectors_1, 
        eigenvalues_2, eigenvectors_2):

        # Get the number of eigenvectors
        n_components = len(eigenvectors_1)

        accum = 0
        norm = 0
        for pc in range(0,n_components):
            dpm = np.dot(eigenvectors_1[pc], np.transpose(eigenvectors_2[pc]))
            val = dpm * dpm * eigenvalues_1[pc] * eigenvalues_2[pc]
            norm = norm + eigenvalues_1[pc] * eigenvalues_2[pc]
            accum = accum + val

        sso = np.sqrt(accum / norm)
        #sso = (dpm * dpm).sum() / n_components
        return sso


    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_similarity module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Internal file paths
        try:
            # Using rel paths to shorten the amount of characters due to fortran path length limitations
            input_pcz_1 = str(Path(self.stage_io_dict["in"]["input_pcz_path1"]).relative_to(Path.cwd()))
            input_pcz_2 = str(Path(self.stage_io_dict["in"]["input_pcz_path2"]).relative_to(Path.cwd()))
            output_json = str(Path(self.stage_io_dict["out"]["output_json_path"]).relative_to(Path.cwd()))
        except ValueError:
            # Container or remote case
            input_pcz = self.stage_io_dict["in"]["input_pcz_path"]
            output_json = self.stage_io_dict["out"]["output_json_path"]

        # Temporary output
        temp_out_1 = str(Path(self.stage_io_dict.get("unique_dir")).joinpath("output_1.dat"))
        temp_out_2 = str(Path(self.stage_io_dict.get("unique_dir")).joinpath("output_2.dat"))

        # Command line 1
        # pczdump -i structure.ca.std.pcz --evals -o evals.txt
        self.cmd = [
                # Evals pcz 1 
                self.binary_path,
                "-i", input_pcz_1,
                "-o", temp_out_1,
                "--evals", ';',
                # Evals pcz 2
                self.binary_path,
                "-i", input_pcz_2,
                "-o", temp_out_2,
                "--evals"
        ]
 
        # Run Biobb block 1
        self.run_biobb()

        # Parse output evals
        info_dict = {}
        info_dict['evals_1'] = []
        info_dict['evals_2'] = []

        row = 0
        with open (temp_out_1,'r') as file:
            for line in file:
                info = float(line.strip())
                info_dict['evals_1'].append(info)

        with open (temp_out_2,'r') as file:
            for line in file:
                info = float(line.strip())
                info_dict['evals_2'].append(info)       
       
        num_evals_1 = len(info_dict['evals_1'])
        num_evals_2 = len(info_dict['evals_2'])
        num_evals_min = min(num_evals_1,num_evals_2)
        info_dict['num_evals_min'] = num_evals_min

        # Command line 2
        # pczdump -i structure.ca.std.pcz --evals -o evals.txt
        self.cmd = []
        for pc in (range(1,num_evals_min+1)):
            # Evecs pcz 1 
            self.cmd.append(self.binary_path)
            self.cmd.append("-i")
            self.cmd.append(input_pcz_1)
            #self.cmd.append("-o evecs_1_pc{}".format(pc))
            self.cmd.append("-o")
            self.cmd.append(str(Path(self.stage_io_dict.get("unique_dir")).joinpath("evecs_1_pc{}".format(pc))))
            self.cmd.append("--evec={}".format(pc))
            self.cmd.append(";")
            # Evals pcz 2
            self.cmd.append(self.binary_path)
            self.cmd.append("-i")
            self.cmd.append(input_pcz_2)
            #self.cmd.append("-o evecs_2_pc{}".format(pc))
            self.cmd.append("-o")
            self.cmd.append(str(Path(self.stage_io_dict.get("unique_dir")).joinpath("evecs_2_pc{}".format(pc))))
            self.cmd.append("--evec={}".format(pc))
            self.cmd.append(";")

        # Run Biobb block 2
        self.run_biobb()

        # Parse output evecs
        info_dict['evecs_1'] = {}
        info_dict['evecs_2'] = {}
        eigenvectors_1 = []
        eigenvectors_2 = []
        for pc in (range(1,num_evals_min+1)):
            pc_id = "pc{}".format(pc)
            info_dict['evecs_1'][pc_id] = []
            info_dict['evecs_2'][pc_id] = []
            with open (str(Path(self.stage_io_dict.get("unique_dir")).joinpath("evecs_1_pc{}".format(pc))),'r') as file:
                list_evecs = []
                for line in file:
                    info = line.strip().split(' ')
                    for nums in info:
                        if nums:
                            list_evecs.append(float(nums))
                info_dict['evecs_1'][pc_id] = list_evecs
                eigenvectors_1.append(list_evecs)

            with open (str(Path(self.stage_io_dict.get("unique_dir")).joinpath("evecs_2_pc{}".format(pc))),'r') as file:
                list_evecs = []
                for line in file:
                    info = line.strip().split(' ')
                    for nums in info:
                        if nums:
                            list_evecs.append(float(nums))
                info_dict['evecs_2'][pc_id] = list_evecs
                eigenvectors_2.append(list_evecs)
        
        simIndex = self.get_similarity_index(info_dict['evals_1'], eigenvectors_1, info_dict['evals_2'], eigenvectors_2)
        info_dict['similarityIndex'] = float("{:.3f}".format(simIndex))
        dotProduct = self.get_subspace_overlap(eigenvectors_1, eigenvectors_2)
        #info_dict['similarityIndex_dotProduct'] = float("{:.3f}".format(dotProduct))
        info_dict['similarityIndex_rmsip'] = float("{:.3f}".format(dotProduct))
        rwsip = self.get_rwsip(info_dict['evals_1'], eigenvectors_1, info_dict['evals_2'], eigenvectors_2)
        info_dict['similarityIndex_rwsip'] = float("{:.3f}".format(rwsip))

        # convert into JSON:
        y = json.dumps(info_dict)

        ## the result is a JSON string:
        print(json.dumps(info_dict, indent=4))

        with open (output_json, 'w') as out_file:
            out_file.write(json.dumps(info_dict, indent=4))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def pcz_similarity(input_pcz_path1: str, input_pcz_path2: str, output_json_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZsimilarity <flexserv.pcasuite.pcz_similarity>`flexserv.pcasuite.PCZsimilarity class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_similarity.launch>` method"""

    return PCZsimilarity(  
                    input_pcz_path1=input_pcz_path1,
                    input_pcz_path2=input_pcz_path2,
                    output_json_path=output_json_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Compute PCA Similarity from a given pair of compressed PCZ files.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path1', required=True, help='Input compressed trajectory file 1. Accepted formats: pcz.')
    required_args.add_argument('--input_pcz_path2', required=True, help='Input compressed trajectory file 2. Accepted formats: pcz.')
    required_args.add_argument('--output_json_path', required=True, help='Output json file with PCA similarity. Accepted formats: json.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_similarity( input_pcz_path1=args.input_pcz_path1,
                    input_pcz_path2=args.input_pcz_path2,
                    output_json_path=args.output_json_path,
                    properties=properties)

if __name__ == '__main__':
    main()
