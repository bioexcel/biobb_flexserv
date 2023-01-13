#!/usr/bin/env python3

"""Module containing the PCZstiffness class and the command line interface."""
import argparse
import shutil, re, os
import json, math
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.pcasuite.pcz_stiffness as myself
from biobb_flexserv.pcasuite.common import *

class PCZstiffness(BiobbObject):
    """
    | biobb_flexserv PCZstiffness
    | Extract PCA stiffness from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Stiffness. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pca_stiffness.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **eigenvector** (*int*) - (0) PCA mode (eigenvector) from which to extract stiffness.
            * **temperature** (*int*) - (300) Temperature with which compute the apparent stiffness.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexserv.pcasuite.pcz_stiffness import pcz_stiffness

            prop = {
                'eigenvector': 1
            }

            pcz_stiffness( input_pcz_path='/path/to/pcazip_input.pcz',
                    output_json_path='/path/to/pcz_stiffness.json',
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
    output_json_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

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
        self.eigenvector = properties.get('eigenvector', 0)
        self.temperature = properties.get('temperature', 300)

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, out_err):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pcz_path"] = check_input_path(self.io_dict["in"]["input_pcz_path"], "input_pcz_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_json_path"] = check_output_path(self.io_dict["out"]["output_json_path"],"output_json_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_stiffness module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        # These BBs need a temporary folder as pcasuite does not allow for long input paths
        # e.g. pczaunzip -i /Users/user/BioBB/Dev/biobb_flexserv/biobb_flexserv/test/data/pcasuite/pcazip.pcz
        #      gives --> "Illegal instruction: 4"
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Copying input files to temporary folder
        shutil.copy2(self.io_dict["in"]["input_pcz_path"], self.tmp_folder)

        # Defining output files in temporary folder
        #output_file_name = PurePath(self.io_dict["out"]["output_crd_path"]).name
        output_file_name = "pcz_stiffness.txt"
        output_file = str(PurePath(self.tmp_folder).joinpath(output_file_name))

        # Command line
        # pczdump -i structure.ca.std.pcz --stiffness -o pcz.stiffness
        self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_file_name,
                "--stiff={}".format(self.eigenvector),
                "--temperature={}".format(self.temperature)
               ]
 
        # Run Biobb block
        self.run_biobb()

        # Parse output stiffness
        info_dict = {}
        info_dict['stiffness'] = []
        info_dict['stiffness_log'] = []
        row = 0
        with open (output_file,'r') as file:
            for line in file:
                info = line.strip().split(',')
                line_array = []
                line_array_log = []
                for nums in info:
                    if nums:
                        line_array.append(float(nums))
                        if float(nums) != 0:
                            line_array_log.append(math.log10(float(nums)))
                        else:
                            line_array_log.append(float(nums))
                                
                info_dict['stiffness'].append(line_array)
                info_dict['stiffness'][row][row] = float('inf')
                info_dict['stiffness_log'].append(line_array_log)
                info_dict['stiffness_log'][row][row] = float('inf')
                row += 1
       
        # convert into JSON:
        y = json.dumps(info_dict)

        ## the result is a JSON string:
        print(json.dumps(info_dict, indent=4))

        with open (PurePath(self.io_dict["out"]["output_json_path"]),'w') as out_file:
            #out_file.write(out_data)
            out_file.write(json.dumps(info_dict, indent=4))

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def pcz_stiffness(input_pcz_path: str, output_json_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZstiffness <flexserv.pcasuite.pcz_stiffness>`flexserv.pcasuite.PCZstiffness class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_stiffness.launch>` method"""

    return PCZstiffness(  
                    input_pcz_path=input_pcz_path,
                    output_json_path=output_json_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Extract PCA Stiffness from a compressed PCZ file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_json_path', required=True, help='Output json file with PCA stiffness. Accepted formats: json.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_stiffness(      input_pcz_path=args.input_pcz_path,
                    output_json_path=args.output_json_path,
                    properties=properties)

if __name__ == '__main__':
    main()
