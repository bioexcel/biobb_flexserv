# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_collectivity import pcz_collectivity


class TestPCZcollectivity():
    def setup_class(self):
        fx.test_setup(self, 'pcz_collectivity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_collectivity(self):
        pcz_collectivity(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
