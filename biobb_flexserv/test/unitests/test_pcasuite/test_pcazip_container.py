# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_zip import pcz_zip
import pytest
import sys


class TestPCZzipDocker():
    def setup_class(self):
        fx.test_setup(self, 'pcz_zip_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pczzip_docker(self):
        pcz_zip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pcz_path'])
        assert fx.equal(self.paths['output_pcz_path'], self.paths['ref_output_pcz_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPCZzipSingularity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_zip_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pczzip_singularity(self):
        pcz_zip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pcz_path'])
        assert fx.equal(self.paths['output_pcz_path'], self.paths['ref_output_pcz_path'])
