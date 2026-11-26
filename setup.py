import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_flexserv",
    version="5.3.0",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="biobb_flexserv is a BioBB category for biomolecular flexibility studies on protein 3D structures.",
    long_description="biobb_flexserv allows the generation of protein conformational ensembles from 3D structures and the analysis of its molecular flexibility.",
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility Flexibility Ensembles Protein Structure",
    url="https://github.com/bioexcel/biobb_flexserv",
    project_urls={
        "Documentation": "http://biobb-flexserv.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    package_data={'biobb_flexserv': ['py.typed']},
    include_package_data=True,
    install_requires=['biobb_common==5.3.1'],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "bd_run = biobb_flexserv.flexserv.bd_run:BDRun.main",
            "dmd_run = biobb_flexserv.flexserv.dmd_run:DMDRun.main",
            "nma_run = biobb_flexserv.flexserv.nma_run:NMARun.main",
            "pcz_zip = biobb_flexserv.pcasuite.pcz_zip:PCZzip.main",
            "pcz_unzip = biobb_flexserv.pcasuite.pcz_unzip:PCZunzip.main",
            "pcz_animate = biobb_flexserv.pcasuite.pcz_animate:PCZanimate.main",
            "pcz_bfactor = biobb_flexserv.pcasuite.pcz_bfactor:PCZbfactor.main",
            "pcz_collectivity = biobb_flexserv.pcasuite.pcz_collectivity:PCZcollectivity.main",
            "pcz_evecs = biobb_flexserv.pcasuite.pcz_evecs:PCZevecs.main",
            "pcz_hinges = biobb_flexserv.pcasuite.pcz_hinges:PCZhinges.main",
            "pcz_info = biobb_flexserv.pcasuite.pcz_info:PCZinfo.main",
            "pcz_lindemann = biobb_flexserv.pcasuite.pcz_lindemann:PCZlindemann.main",
            "pcz_stiffness = biobb_flexserv.pcasuite.pcz_stiffness:PCZstiffness.main",
            "pcz_similarity = biobb_flexserv.pcasuite.pcz_similarity:PCZsimilarity.main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ],
)
