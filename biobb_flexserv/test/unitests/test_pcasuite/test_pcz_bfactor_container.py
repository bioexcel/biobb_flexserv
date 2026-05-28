# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_bfactor import pcz_bfactor
import pytest
import sys


class TestPCZbfactorDocker():
    def setup_class(self):
        fx.test_setup(self, 'pcz_bfactor_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_bfactor_docker(self):
        pcz_bfactor(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPCZbfactorSingularity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_bfactor_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_bfactor_singularity(self):
        pcz_bfactor(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
