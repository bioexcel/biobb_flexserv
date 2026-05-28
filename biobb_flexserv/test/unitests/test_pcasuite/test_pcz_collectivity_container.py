# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_collectivity import pcz_collectivity
import pytest
import sys


class TestPCZcollectivityDocker():
    def setup_class(self):
        fx.test_setup(self, 'pcz_collectivity_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_collectivity_docker(self):
        pcz_collectivity(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPCZcollectivitySingularity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_collectivity_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_collectivity_singularity(self):
        pcz_collectivity(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
