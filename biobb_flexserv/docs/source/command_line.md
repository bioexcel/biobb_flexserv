# BioBB FLEXSERV Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Dmd_run
Wrapper of the Discrete Molecular Dynamics tool from the FlexServ module.
### Get help
Command:
```python
dmd_run -h
```
    /bin/sh: dmd_run: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb). Accepted formats: PDB
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (dmdgoopt) DMD binary path to be used..
* **dt** (*number*): (1e-12) Integration time (s).
* **temperature** (*integer*): (300) Simulation temperature (K).
* **frames** (*integer*): (1000) Number of frames in the final ensemble.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_dmd_run.yml)
```python
properties:
  frames: 100

```
#### Command line
```python
dmd_run --config config_dmd_run.yml --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_dmd_run.json)
```python
{
  "properties": {
    "frames": 100
  }
}
```
#### Command line
```python
dmd_run --config config_dmd_run.json --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```

## Nma_run
Wrapper of the Normal Mode Analysis tool from the FlexServ module.
### Get help
Command:
```python
nma_run -h
```
    /bin/sh: nma_run: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb). Accepted formats: PDB
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (bd) BD binary path to be used..
* **frames** (*integer*): (1000) Number of frames in the final ensemble.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_nma_run.yml)
```python
properties:
  frames: 100

```
#### Command line
```python
nma_run --config config_nma_run.yml --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_nma_run.json)
```python
{
  "properties": {
    "frames": 100
  }
}
```
#### Command line
```python
nma_run --config config_nma_run.json --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```

## Bd_run
Wrapper of the Browian Dynamics tool from the FlexServ module.
### Get help
Command:
```python
bd_run -h
```
    /bin/sh: bd_run: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/flexserv/structure.ca.pdb). Accepted formats: PDB
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/flexserv_bd.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/traj.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (bd) BD binary path to be used..
* **time** (*integer*): (1000000) Total simulation time (ps).
* **dt** (*number*): (1e-15) Integration time (ps).
* **wfreq** (*integer*): (1000) Writing frequency (ps).
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_bd_run.yml)
```python
properties:
  time: 10000
  wfreq: 100

```
#### Command line
```python
bd_run --config config_bd_run.yml --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_bd_run.json)
```python
{
  "properties": {
    "time": 10000,
    "wfreq": 100
  }
}
```
#### Command line
```python
bd_run --config config_bd_run.json --input_pdb_path structure.ca.pdb --output_log_path flexserv_bd.log --output_crd_path traj.crd
```
