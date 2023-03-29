#!/usr/bin/env python3

"""Module containing the PCZstiffness class and the command line interface."""
import argparse
import json, math
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class PCZstiffness(BiobbObject):
    """
    | biobb_flexserv PCZstiffness
    | Extract PCA stiffness from a compressed PCZ file.
    | Wrapper of the pczdump tool from the PCAsuite FlexServ module.

    Args:
        input_pcz_path (str): Input compressed trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz>`_. Accepted formats: pcz (edam:format_3874).
        output_json_path (str): Output json file with PCA Stiffness. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_stiffness.json>`_. Accepted formats: json (edam:format_3464).
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
        self.eigenvector = properties.get('eigenvector', 0)
        self.temperature = properties.get('temperature', 300)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexServ pcz_stiffness module."""

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

        # Command line
        # pczdump -i structure.ca.std.pcz --stiffness -o pcz.stiffness
        self.cmd = [self.binary_path,
                "-i", input_pcz,
                "-o", temp_out,
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
        with open (temp_out,'r') as file:
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
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    pcz_stiffness(  input_pcz_path=args.input_pcz_path,
                    output_json_path=args.output_json_path,
                    properties=properties)

if __name__ == '__main__':
    main()
