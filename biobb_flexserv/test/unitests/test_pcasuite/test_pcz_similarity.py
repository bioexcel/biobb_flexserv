from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_similarity import pcz_similarity

class TestPCZsimilarity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_similarity')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_pcz_similarity(self):
        pcz_similarity(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
