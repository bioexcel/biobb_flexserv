# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_unzip import pcz_unzip
import pytest
import sys


class TestPCZunzipDocker():
    def setup_class(self):
        fx.test_setup(self, 'pcz_unzip_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pczunzip_docker(self):
        pcz_unzip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPCZunzipSingularity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_unzip_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pczunzip_singularity(self):
        pcz_unzip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
