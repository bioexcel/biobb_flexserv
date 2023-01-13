#!/usr/bin/env python3

"""Module containing the PCZinfo class and the command line interface."""
import argparse
import shutil, re, os
import json
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
import biobb_flexserv.pcasuite.pcz_info as myself
from biobb_flexserv.pcasuite.common import *

class PCZinfo(BiobbObject):
    """
    | biobb_flexserv PCZinfo
    | Extract PCA info (variance, Dimensionality) from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA info such as number of components, variance and dimensionality. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pca_info.json>`_. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("pczdump") pczdump binary path to be used.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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
        """Launches the execution of the FlexServ pcz_info module."""

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
        output_file_name = "pcz_info.txt"
        output_file = str(PurePath(self.tmp_folder).joinpath(output_file_name))
        output_file_name2 = "pcz_evals.txt"
        output_file2 = str(PurePath(self.tmp_folder).joinpath(output_file_name2))

        # Command line
        # pczdump -i structure.ca.std.pcz --info -o pcz.info
        self.cmd = ['cd', self.tmp_folder, ';', self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_file_name,
                "--info", ';',
                self.binary_path,
                "-i", PurePath(self.io_dict["in"]["input_pcz_path"]).name,
                "-o", output_file_name2,
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
        with open (output_file,'r') as file:
            for line in file:
                info = line.split(':')
                info_dict[info[0].strip().replace(' ','_')] = info[1].strip()

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
        with open (output_file2,'r') as file:
            for line in file:
                eval = float(line.strip())
                eval_var = (eval / float(info_dict['Total_variance']))*100
                accum_tot = accum_tot + eval_var
                eval_dim = (eval / float(info_dict['Explained_variance']))*100
                accum_exp = accum_exp + eval_dim
                info_dict['Eigen_Values'].append(eval)
                info_dict['Eigen_Values_dimensionality_vs_total'].append(accum_tot)
                info_dict['Eigen_Values_dimensionality_vs_explained'].append(accum_exp)
       
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

def pcz_info(input_pcz_path: str, output_json_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PCZinfo <flexserv.pcasuite.pcz_info>`flexserv.pcasuite.PCZinfo class and
    execute :meth:`launch() <flexserv.pcasuite.pcz_info.launch>` method"""

    return PCZinfo(  
                    input_pcz_path=input_pcz_path,
                    output_json_path=output_json_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Extract PCA info from a compressed PCZ file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pcz_path', required=True, help='Input compressed trajectory file. Accepted formats: pcz.')
    required_args.add_argument('--output_json_path', required=True, help='Output json file with PCA info such as number of components, variance and dimensionality. Accepted formats: json.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_info(       input_pcz_path=args.input_pcz_path,
                    output_json_path=args.output_json_path,
                    properties=properties)

if __name__ == '__main__':
    main()
