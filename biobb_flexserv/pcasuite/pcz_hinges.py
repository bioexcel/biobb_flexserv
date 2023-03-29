#!/usr/bin/env python3

"""Module containing the PCZhinges class and the command line interface."""
import argparse
import json, re
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class PCZhinges(BiobbObject):
    """
    | biobb_flexserv PCZhinges
    | Compute possible hinge regions (residues around which large protein movements are organized) of a molecule from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output hinge regions x PCA mode file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/hinges.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (0) PCA mode (eigenvector) from which to extract bfactor values per residue (0 means average over all modes).
            * **method** (*str*) - ("Dynamic_domain") Method to compute the hinge regions (Options: Bfactor_slope, Force_constant, Dynamic_domain) 
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcz_hinges import pcz_hinges
            prop = {
                'eigenvector': 1,
                'pdb': True
            }
            pcz_hinges( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/hinges.json',
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
    def __init__(self, input_pcz_path: str, output_json_path: str,
    properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 
                'input_pcz_path': input_pcz_path
             },
            'out': {    
                'output_json_path': output_json_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'pczdump')
        self.eigenvector = properties.get('eigenvector', 1)
        self.method = properties.get('method', "Bfactor_slope")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def parse_output(self,output_file):
        """ Parses FlexServ hinges methods output file report """

        method = ''
        if self.method == "Bfactor_slope":
            method = "#### Distance variation method"
        elif self.method == "Force_constant":
            method = "#### Force constant"
        elif self.method == "Dynamic_domain":
            method = "#### Lavery method"
        else:
            print("Method not recognised ({}), please check it and try again. ".format(self.method))

        start = False
        out_data = ''
        with open (output_file,'r') as file:
            for line in file:
                if method in line: 
                    start = True
                elif "####" in line:
                    start = False
                if start:
                    out_data += line

        dict_out = {}
        dict_out["method"] = self.method
        if self.method == "Force_constant":
            dict_out["values_per_residue"] = []
            for line in out_data.split("\n"):
                print ("Force_constant: -" + str(line) + "-")
                if line and "#" not in line:
                    dict_out["values_per_residue"].append(float(line.strip()))
                if "possible hinge" in line: # Peak constant (possible hinge): residue 64 (16.740)
                    residue = int(line.split(' ')[6])
                    dict_out["hinge_residues"] = residue
        elif self.method == "Bfactor_slope":
            dict_out["hinge_residues"] = []
            for line in out_data.split("\n"):
                print ("Bfactor_slope: -" + str(line) + "-")
                if "Window" in line:  # Window 28: residue  54 seems a downhill hinge point
                    residue = int(re.split(r'\s+',line)[3])
                    dict_out["hinge_residues"].append(residue)
                if "Consensus" in line: # Consensus Downhill hinge point :  23.7 (  64.965)
                    hinge_point = float(line.split(':')[1].split('(')[0])
                    dict_out["consensus_hinge"] = hinge_point
        elif self.method == "Dynamic_domain":
            start = 0
            dict_out["clusters"] = []
            for line in out_data.split("\n"):
                print ("Dynamic_domain: -" + str(line) + "-")
                if not "threshold" in line and "nClusters" in line:  # nClusters: 2
                    nclusters = int(line.split(':')[1])
                    dict_out["nClusters"] = nclusters
                if "Threshold" in line:  # *** Threshold defined: 0.300000
                    threshold = float(line.split(':')[1])
                    dict_out["threshold"] = threshold
                if "Min. drij" in line:  # *** Min. drij: 0.000322
                    minValue = float(line.split(':')[1])
                    dict_out["minValue"] = minValue
                if "Max. drij" in line:  # *** Max. drij: 6.385425
                    maxValue = float(line.split(':')[1])
                    dict_out["maxValue"] = maxValue
                if "threshold" in line:  # nClusters: 2 threshold: 3.192873
                    final_threshold = float(line.split(':')[2])
                    dict_out["final_threshold"] = final_threshold
                if "Cluster" in line and "elements" in line: # Cluster 0 (74 elements)
                    clusterLine = line.split()
                    clusterNum = int(clusterLine[1])
                    clusterElems = int(clusterLine[2].replace('(',''))
                    cluster = {"clusterNum" : clusterNum, "clusterElems" : clusterElems}
                    dict_out["clusters"].append(cluster)
                    start = start + 1
                if start and "[" in line:
                    #dict_out["clusters"][start-1]["residues"] = list(map(int,list(line.replace(", ]", "").replace("  [","").split(', '))))
                    dict_out["clusters"][start-1]["residues"] = eval(line)
                #Interacting regions: 13 14 30 31 69 70 84 85 112 113 114 115 116 166 167 199 200
                if "Interacting regions" in line:
                    nums = line.split(':')[1]
                    dict_out["interacting_regions"] = list(map(int,nums.split()))
                #Hinge residues: 13 14 30 31 69 70 84 85 112 113 114 115 116 166 167 199 200
                if "Hinge residues" in line:  
                    nums = line.split(':')[1]
                    dict_out["hinge_residues"] = list(map(int,nums.split()))

        return dict_out

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_hinges module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Internal file paths
        try:
            # Using rel paths to shorten the amount of characters due to fortran path length limitations
            input_pcz = str(Path(self.stage_io_dict["in"]["input_pcz_path"]).relative_to(Path.cwd()))
            output_json = str(Path(self.stage_io_dict["out"]["output_json_path"]).relative_to(Path.cwd()))
        except ValueError:
            # Container or remote case
            input_pcz = self.stage_io_dict["in"]["input_pcz_path"]
            output_json = self.stage_io_dict["out"]["output_json_path"]

        # Temporary output
        temp_out = str(Path(self.stage_io_dict.get("unique_dir")).joinpath("output.dat"))

        # Command line (1: dat file)
        # pczdump -i structure.ca.std.pcz --fluc=1 -o bfactor_1.dat
        self.cmd = [self.binary_path,
                "-i", input_pcz,
                "-o", temp_out,
                "-t", "0.3",
                "--hinge={}".format(self.eigenvector),
                ">&", "pcz_dump.hinges.log"
               ]
  
        # Run Biobb block
        self.run_biobb()

        # Parsing output file and extracting results for the given method 
        dict_out = self.parse_output(temp_out)

        # convert into JSON:
        y = json.dumps(dict_out)

        ## the result is a JSON string:
        print(json.dumps(dict_out, indent=4))

        with open (output_json, 'w') as out_file:
            out_file.write(json.dumps(dict_out, indent=4))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def pcz_hinges(input_pcz_path: str, output_json_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZhinges <flexserv.pcasuite.pcz_hinges>`flexserv.pcasuite.PCZhinges class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_hinges.launch>` method"""

    return PCZhinges(  
                    input_pcz_path=input_pcz_path,
                    output_json_path=output_json_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Compute possible hinge regions (residues around which large protein movements are organized) of a molecule from a compressed PCZ file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_json_path', required=True, help='Output hinge regions x PCA mode file. Accepted formats: json.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_hinges(     input_pcz_path=args.input_pcz_path,
                    output_json_path=args.output_json_path,
                    properties=properties)

if __name__ == '__main__':
    main()
