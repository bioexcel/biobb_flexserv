# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_zip import pcz_zip


class TestPCZzip():
    def setup_class(self):
        fx.test_setup(self, 'pcz_zip')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pczzip(self):
        pcz_zip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pcz_path'])
        assert fx.equal(self.paths['output_pcz_path'], self.paths['ref_output_pcz_path'])
