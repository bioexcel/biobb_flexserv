import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_flexserv",
    version="3.8.1",
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
    install_requires=['biobb_common==3.8.1'],
    python_requires='>=3.7.*',
    entry_points={
        "console_scripts": [
            "bd_run = biobb_flexserv.flexserv.flexserv_bdrun:main",
            "dmd_run = biobb_flexserv.flexserv.flexserv_dmdrun:main",
            "nma_run = biobb_flexserv.flexserv.flexserv_nmarun:main"
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
