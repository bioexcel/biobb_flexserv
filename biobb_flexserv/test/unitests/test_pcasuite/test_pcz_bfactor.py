from biobb_common.tools import test_fixtures as fx
from biobb_flexserv.pcasuite.pcz_bfactor import pcz_bfactor

class TestPCZbfactor():
    def setup_class(self):
        fx.test_setup(self, 'pcz_bfactor')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_pcz_bfactor(self):
        pcz_bfactor(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
