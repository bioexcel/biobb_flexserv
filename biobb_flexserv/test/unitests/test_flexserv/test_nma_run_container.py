# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.flexserv.nma_run import nma_run
import pytest
import sys


class TestNMARunDocker():
    def setup_class(self):
        fx.test_setup(self, 'nma_run_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_nma_run_docker(self):
        nma_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        # assert fx.equal(self.paths['output_log_path'], self.paths['ref_output_log_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestNMARunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'nma_run_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_nma_run_singularity(self):
        nma_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        # assert fx.equal(self.paths['output_log_path'], self.paths['ref_output_log_path'])
