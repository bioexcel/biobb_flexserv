from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_animate import pcz_animate

class TestPCZanimate():
    def setup_class(self):
        fx.test_setup(self, 'pcz_animate')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_pcz_animate(self):
        pcz_animate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
