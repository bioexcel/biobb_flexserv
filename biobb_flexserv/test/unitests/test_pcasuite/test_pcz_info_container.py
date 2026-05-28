# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_info import pcz_info
import pytest
import sys


class TestPCZinfoDocker():
    def setup_class(self):
        fx.test_setup(self, 'pcz_info_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_info_docker(self):
        pcz_info(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPCZinfoSingularity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_info_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_info_singularity(self):
        pcz_info(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
