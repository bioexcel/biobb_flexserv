# BioBB FLEXSERV Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Pcz_animate
Extract PCA animations from a compressed PCZ file.
### Get help
Command:
```python
pcz_animate -h
```
    /bin/sh: pcz_animate: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_crd_path** (*string*): Output PCA animated trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip_anim1.pdb). Accepted formats: CRD, MDCRD, INPCRD, PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **eigenvector** (*integer*): (1) Eigenvector to be used for the animation.
* **pdb** (*boolean*): (False) Use PDB format for output trajectory.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_animate.yml)
```python
properties:
  eigenvector: 1
  pdb: true

```
#### Command line
```python
pcz_animate --config config_pcz_animate.yml --input_pcz_path pcazip.pcz --output_crd_path pcazip_anim1.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_animate.json)
```python
{
  "properties": {
    "eigenvector": 1,
    "pdb": true
  }
}
```
#### Command line
```python
pcz_animate --config config_pcz_animate.json --input_pcz_path pcazip.pcz --output_crd_path pcazip_anim1.pdb
```

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
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/dmd_run_out.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/dmd_run_out.crd). Accepted formats: CRD, MDCRD, INPCRD
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
dmd_run --config config_dmd_run.yml --input_pdb_path structure.ca.pdb --output_log_path dmd_run_out.log --output_crd_path dmd_run_out.crd
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
dmd_run --config config_dmd_run.json --input_pdb_path structure.ca.pdb --output_log_path dmd_run_out.log --output_crd_path dmd_run_out.crd
```

## Pcz_evecs
Extract PCA Eigen Vectors from a compressed PCZ file.
### Get help
Command:
```python
pcz_evecs -h
```
    /bin/sh: pcz_evecs: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA Eigen Vectors. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_evecs.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **eigenvector** (*integer*): (1) PCA mode (eigenvector) from which to extract eigen vectors..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_evecs.yml)
```python
properties:
  eigenvector: 1

```
#### Command line
```python
pcz_evecs --config config_pcz_evecs.yml --input_pcz_path pcazip.pcz --output_json_path pcz_evecs.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_evecs.json)
```python
{
  "properties": {
    "eigenvector": 1
  }
}
```
#### Command line
```python
pcz_evecs --config config_pcz_evecs.json --input_pcz_path pcazip.pcz --output_json_path pcz_evecs.json
```

## Pcz_similarity
Compute PCA similarity between two given compressed PCZ files.
### Get help
Command:
```python
pcz_similarity -h
```
    /bin/sh: pcz_similarity: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path1** (*string*): Input compressed trajectory file 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **input_pcz_path2** (*string*): Input compressed trajectory file 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA Similarity results. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_similarity.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
### JSON

## Pcz_bfactor
Extract residue bfactors x PCA mode from a compressed PCZ file.
### Get help
Command:
```python
pcz_bfactor -h
```
    /bin/sh: pcz_bfactor: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_dat_path** (*string*): Output Bfactor x residue x PCA mode file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/bfactors.dat). Accepted formats: DAT, TXT, CSV
* **output_pdb_path** (*string*): Output PDB with Bfactor x residue x PCA mode file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/bfactors.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **eigenvector** (*integer*): (0) PCA mode (eigenvector) from which to extract bfactor values per residue (0 means average over all modes)..
* **pdb** (*boolean*): (False) Generate a PDB file with the computed bfactors (to be easily represented with colour scale).
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_bfactor.yml)
```python
properties:
  eigenvector: 1
  pdb: true

```
#### Command line
```python
pcz_bfactor --config config_pcz_bfactor.yml --input_pcz_path pcazip.pcz --output_dat_path bfactors.dat --output_pdb_path bfactors.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_bfactor.json)
```python
{
  "properties": {
    "eigenvector": 1,
    "pdb": true
  }
}
```
#### Command line
```python
pcz_bfactor --config config_pcz_bfactor.json --input_pcz_path pcazip.pcz --output_dat_path bfactors.dat --output_pdb_path bfactors.pdb
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
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/nma_run_out.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/nma_run_out.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (diaghess) NMA binary path to be used..
* **frames** (*integer*): (1000) Number of frames in the final ensemble.
* **nvecs** (*integer*): (50) Number of vectors to take into account for the ensemble generation.
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
nma_run --config config_nma_run.yml --input_pdb_path structure.ca.pdb --output_log_path nma_run_out.log --output_crd_path nma_run_out.crd
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
nma_run --config config_nma_run.json --input_pdb_path structure.ca.pdb --output_log_path nma_run_out.log --output_crd_path nma_run_out.crd
```

## Pcz_lindemann
Extract Lindemann coefficient (an estimate of the solid-liquid behaviour of a protein) from a compressed PCZ file.
### Get help
Command:
```python
pcz_lindemann -h
```
    /bin/sh: pcz_lindemann: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA Eigen Vectors. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_lindemann.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **mask** (*string*): (all atoms) Residue mask, in the format ":resnum1, resnum2, resnum3" (e.g. ":10,21,33"). See https://mmb.irbbarcelona.org/software/pcasuite/ for the complete format specification..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
### JSON

## Pcz_stiffness
Extract PCA stiffness from a compressed PCZ file.
### Get help
Command:
```python
pcz_stiffness -h
```
    /bin/sh: pcz_stiffness: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA Stiffness. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_stiffness.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **eigenvector** (*integer*): (0) PCA mode (eigenvector) from which to extract stiffness..
* **temperature** (*integer*): (300) Temperature with which compute the apparent stiffness..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_stiffness.yml)
```python
properties:
  eigenvector: 0

```
#### Command line
```python
pcz_stiffness --config config_pcz_stiffness.yml --input_pcz_path pcazip.pcz --output_json_path pcz_stiffness.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_stiffness.json)
```python
{
  "properties": {
    "eigenvector": 0
  }
}
```
#### Command line
```python
pcz_stiffness --config config_pcz_stiffness.json --input_pcz_path pcazip.pcz --output_json_path pcz_stiffness.json
```

## Pcz_collectivity
Extract PCA collectivity (numerical measure of how many atoms are affected by a given mode) from a compressed PCZ file.
### Get help
Command:
```python
pcz_collectivity -h
```
    /bin/sh: pcz_collectivity: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA Collectivity indexes per mode. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_collectivity.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **eigenvector** (*integer*): (0) PCA mode (eigenvector) from which to extract stiffness..
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_collectivity.yml)
```python
properties:
  eigenvector: 0

```
#### Command line
```python
pcz_collectivity --config config_pcz_collectivity.yml --input_pcz_path pcazip.pcz --output_json_path pcz_collectivity.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_collectivity.json)
```python
{
  "properties": {
    "eigenvector": 0
  }
}
```
#### Command line
```python
pcz_collectivity --config config_pcz_collectivity.json --input_pcz_path pcazip.pcz --output_json_path pcz_collectivity.json
```

## Pcz_zip
Wrapper of the pcazip tool from the PCAsuite FlexServ module.
### Get help
Command:
```python
pcz_zip -h
```
    /bin/sh: pcz_zip: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/structure.ca.pdb). Accepted formats: PDB
* **input_crd_path** (*string*): Input Trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/traj.crd). Accepted formats: CRD, MDCRD, INPCRD
* **output_pcz_path** (*string*): Output compressed trajectory. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcazip.pcz). Accepted formats: PCZ
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pcazip) pcazip binary path to be used..
* **neigenv** (*integer*): (0) Number of generated eigenvectors.
* **variance** (*integer*): (90) Percentage of variance captured by the final set of eigenvectors.
* **verbose** (*boolean*): (False) Make output verbose.
* **gauss_rmsd** (*boolean*): (False) Use a gaussian RMSd for fitting.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_zip.yml)
```python
properties:
  variance: 90

```
#### Command line
```python
pcz_zip --config config_pcz_zip.yml --input_pdb_path structure.ca.pdb --input_crd_path traj.crd --output_pcz_path pcazip.pcz
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_zip.json)
```python
{
  "properties": {
    "variance": 90
  }
}
```
#### Command line
```python
pcz_zip --config config_pcz_zip.json --input_pdb_path structure.ca.pdb --input_crd_path traj.crd --output_pcz_path pcazip.pcz
```

## Pcz_hinges
Compute possible hinge regions (residues around which large protein movements are organized) of a molecule from a compressed PCZ file.
### Get help
Command:
```python
pcz_hinges -h
```
    /bin/sh: pcz_hinges: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output hinge regions x PCA mode file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/hinges.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **eigenvector** (*integer*): (0) PCA mode (eigenvector) from which to extract bfactor values per residue (0 means average over all modes)..
* **method** (*string*): (Dynamic_domain) Method to compute the hinge regions (Options: Bfactor_slope, Force_constant, Dynamic_domain).
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_hinges.yml)
```python
properties:
  eigenvector: 0
  method: Bfactor_slope

```
#### Command line
```python
pcz_hinges --config config_pcz_hinges.yml --input_pcz_path pcazip.pcz --output_json_path hinges.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_hinges.json)
```python
{
  "properties": {
    "eigenvector": 0,
    "method": "Bfactor_slope"
  }
}
```
#### Command line
```python
pcz_hinges --config config_pcz_hinges.json --input_pcz_path pcazip.pcz --output_json_path hinges.json
```

## Pcz_info
Extract PCA info (variance, Dimensionality) from a compressed PCZ file.
### Get help
Command:
```python
pcz_info -h
```
    /bin/sh: pcz_info: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_json_path** (*string*): Output json file with PCA info such as number of components, variance and dimensionality. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_info.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pczdump) pczdump binary path to be used..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
### JSON

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
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/bd_run_out.log). Accepted formats: LOG, OUT, TXT, O
* **output_crd_path** (*string*): Output ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/flexserv/bd_run_out.crd). Accepted formats: CRD, MDCRD, INPCRD
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
bd_run --config config_bd_run.yml --input_pdb_path structure.ca.pdb --output_log_path bd_run_out.log --output_crd_path bd_run_out.crd
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
bd_run --config config_bd_run.json --input_pdb_path structure.ca.pdb --output_log_path bd_run_out.log --output_crd_path bd_run_out.crd
```

## Pcz_unzip
Wrapper of the pcaunzip tool from the PCAsuite FlexServ module.
### Get help
Command:
```python
pcz_unzip -h
```
    /bin/sh: pcz_unzip: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pcz_path** (*string*): Input compressed trajectory. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz). Accepted formats: PCZ
* **output_crd_path** (*string*): Output uncompressed trajectory. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/traj.crd). Accepted formats: CRD, MDCRD, INPCRD, PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (pcaunzip) pcaunzip binary path to be used..
* **verbose** (*boolean*): (False) Make output verbose.
* **pdb** (*boolean*): (False) Use PDB format for output trajectory.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_unzip.yml)
```python
properties:
  pdb: false

```
#### Command line
```python
pcz_unzip --config config_pcz_unzip.yml --input_pcz_path pcazip.pcz --output_crd_path traj.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexserv/blob/master/biobb_flexserv/test/data/config/config_pcz_unzip.json)
```python
{
  "properties": {
    "pdb": false
  }
}
```
#### Command line
```python
pcz_unzip --config config_pcz_unzip.json --input_pcz_path pcazip.pcz --output_crd_path traj.crd
```
