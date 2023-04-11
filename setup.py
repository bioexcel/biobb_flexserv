import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_flexserv",
    version="4.0.0",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="biobb_flexserv is a BioBB category for biomolecular flexibility studies on protein 3D structures.",
    long_description="biobb_flexserv allows the generation of protein conformational ensembles from 3D structures and the analysis of its molecular flexibility.",
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility Flexibility Ensembles Protein Structure",
    url="https://github.com/bioexcel/biobb_flexserv",
    project_urls={
        "Documentation": "http://biobb_flexserv.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    include_package_data=True,
    install_requires=['biobb_common==4.0.0'],
    python_requires='>=3.7,<3.10',
    entry_points={
        "console_scripts": [
            "bd_run = biobb_flexserv.flexserv.bd_run:main",
            "dmd_run = biobb_flexserv.flexserv.dmd_run:main",
            "nma_run = biobb_flexserv.flexserv.nma_run:main",
            "pcz_zip = biobb_flexserv.pcasuite.pcz_zip:main",
            "pcz_unzip = biobb_flexserv.pcasuite.pcz_unzip:main",
            "pcz_animate = biobb_flexserv.pcasuite.pcz_animate:main",
            "pcz_bfactor = biobb_flexserv.pcasuite.pcz_bfactor:main",
            "pcz_collectivity = biobb_flexserv.pcasuite.pcz_collectivity:main",
            "pcz_evecs = biobb_flexserv.pcasuite.pcz_evecs:main",
            "pcz_hinges = biobb_flexserv.pcasuite.pcz_hinges:main",
            "pcz_info = biobb_flexserv.pcasuite.pcz_info:main",
            "pcz_lindemann = biobb_flexserv.pcasuite.pcz_lindemann:main",
            "pcz_stiffness = biobb_flexserv.pcasuite.pcz_stiffness:main",
            "pcz_similarity = biobb_flexserv.pcasuite.pcz_similarity:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
