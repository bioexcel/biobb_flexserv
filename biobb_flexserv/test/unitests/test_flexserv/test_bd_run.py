from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.flexserv.bd_run import bd_run

class TestBDRun():
    def setup_class(self):
        fx.test_setup(self, 'bd_run')

    def teardown_class(self):
        #fx.test_teardown(self)
        pass

    def test_bd_run(self):
        bd_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        #assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
