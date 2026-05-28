# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.flexserv.bd_run import bd_run
import pytest
import sys


class TestBDRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'bd_run_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_bd_run_docker(self):
        bd_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        assert fx.equal(self.paths['output_log_path'], self.paths['ref_output_log_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestBDRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'bd_run_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_bd_run_singularity(self):
        bd_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        assert fx.equal(self.paths['output_log_path'], self.paths['ref_output_log_path'])
