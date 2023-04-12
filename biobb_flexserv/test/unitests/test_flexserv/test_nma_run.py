from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.flexserv.nma_run import nma_run


class TestNMARun():
    def setup_class(self):
        fx.test_setup(self, 'nma_run')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_nma_run(self):
        nma_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        # assert fx.equal(self.paths['output_log_path'], self.paths['ref_output_log_path'])
