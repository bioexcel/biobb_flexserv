# Biobb FlexServ changelog

## [Unreleased]

## What's new in version [5.4.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v5.4.0)?

### Changes

* [UPDATE] Update to biobb_common 5.4.0.
* [FIX] `pcz_similarity`: two pcz files with different atoms stop with an error that gives the sizes of their eigenvectors, instead of a numpy error.
* [FIX] `pcz_hinges`: an unknown `method` raises a `ValueError`; it printed a message and went on. The residue lists of the pczdump output are read with `ast.literal_eval` instead of `eval`.
* [FIX] `pcz_bfactor`: `pdb` set to True without an `output_pdb_path` no longer fails with a `KeyError`.
* [FIX] `nma_run`: the FlexServ scripts are found in the Python environment when `CONDA_PREFIX` is not set.
* [CHANGE] `pcz_stiffness`: the diagonal of the `stiffness` and `stiffness_log` matrices of the JSON output is `null` instead of `Infinity`, which is not valid JSON.
* [CHANGE] `nma_run`: the intermediate files of the FlexServ tools (`hessian.dat`, `eigenvec.dat`, `file.proj`) are written in a temporary folder of their own.
* [DOCS] `pcz_bfactor`, `pcz_hinges`, `pcz_lindemann`, `pcz_similarity` and `pcz_zip`: the documented defaults are the values the blocks use (`eigenvector` 1, `method` `Bfactor_slope`, and None for `mask`, `amplifying_factor` and `variance`).
* [UPDATE] Python 3.11 to 3.13.

## What's new in version [5.3.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.0)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1

## What's new in version [5.2.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.1)?

### Changes

* [UPDATE] Update to biobb_common 5.2.2

## What's new in version [5.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.0)?

### Changes

* [UPDATE] Update to biobb_common 5.2.0

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v5.1.0)?

### Changes

* [UPDATE] Update to biobb_common 5.1.0


## What's new in version [5.0.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v5.0.0)?

### Changes

* [FEATURE] New sandbox_path property

## What's new in version [4.2.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.2.0)?
In version 4.2.0 the dependency biobb_common has been updated to 4.2.0 version.

### New features

* Update to biobb_common 4.2.0 (general)

## What's new in version [4.1.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.1.0)?
In version 4.1.0 the dependency biobb_common has been updated to 4.1.0 version.

### New features

* Update to biobb_common 4.1.0 (general)

## What's new in version [4.0.3](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.0.3)?
In version 4.0.3 the module pcz_similarity has been fixed.

### New features

* Fixes in pcz_similarity

## What's new in version [4.0.2](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.0.2)?
The version 4.0.2 fixes a some bugs bug in Python code.

### New features

* Bug fixes

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.0.1)?
The version 4.0.1 fixes a some bugs bug in Python code.

### New features

* Bug fixes

## What's new in version [4.0.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v4.0.0)?
In version 4.0.0 the dependency biobb_common has been updated to 4.0.0 version.

### New features

* Update to biobb_common 4.0.0 (general)

## What's new in version [3.9.1](https://github.com/bioexcel/biobb_flexserv/releases/tag/v3.9.1)?
The version 3.9.1 fixes a bug in Python dependencies.

### New features

* Bug fixes

## What's new in version [3.9.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v3.9.0)?
The version 3.9.0 is the first release of the biobb_flexserv module available in BioConda as a Conda package.

### New features

* BioBB_flexserv BioConda package

## What's new in version [3.8.1](https://github.com/bioexcel/biobb_flexserv/releases/tag/v3.8.1)?
The version 3.8.1 adds PCAsuite tools into the biobb_flexserv module. There have been added the pcz_zip, pcz_unzip, pcz_hinges, pcz_info, pcz_lindemann, pcz_evecs, pcz_collectivity and pcz_animate tools.

### New features

* PCA suite tool: pcz_zip, pcz_unzip, pcz_hinges, pcz_info, pcz_lindemann, pcz_evecs, pcz_collectivity and pcz_animate tools

## What's new in version [3.8.0](https://github.com/bioexcel/biobb_flexserv/releases/tag/v3.8.0)?
The version 3.8.0 is the first release of biobb_flexserv. There have been added the run_bd, run_dmd and run_nma tools.

### New features

* First release
* FlexServ module: bd_run, dmd_run and nma_run tools