from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_evecs import pcz_evecs

class TestPCZevecs():
    def setup_class(self):
        fx.test_setup(self, 'pcz_evecs')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_pcz_evecs(self):
        pcz_evecs(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
