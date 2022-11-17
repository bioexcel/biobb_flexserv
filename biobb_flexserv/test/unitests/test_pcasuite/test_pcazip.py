from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcazip import pcazip

class TestPCAzip():
    def setup_class(self):
        fx.test_setup(self, 'pcazip')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_pcazip(self):
        pcazip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pcz_path'])
        #assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
