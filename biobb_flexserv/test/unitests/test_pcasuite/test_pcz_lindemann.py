# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_lindemann import pcz_lindemann


class TestPCZlindemann():
    def setup_class(self):
        fx.test_setup(self, 'pcz_lindemann')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pcz_lindemann(self):
        pcz_lindemann(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_json_path'])
        assert fx.equal(self.paths['output_json_path'], self.paths['ref_output_json_path'])
