import sys
import unittest

sys.path.append('..')
import crds_to_openapi
import preprocess_specs
import postprocess_adoc


class TestArgs(unittest.TestCase):
  def setUp(self):
    pass

  def test_crds_args_parse(self):
    parser = crds_to_openapi.parse_args(['--crds_dir', 'asdf', '--output_dir', 'asdf'])
    self.assertEqual(parser.crds_dir, 'asdf')
    self.assertEqual(parser.output_dir, 'asdf')


  def test_openapi_args_parse(self):
    parser = preprocess_specs.parse_args(['--specs_dir', 'asdf', '--output_dir', 'asdf'])
    self.assertEqual(parser.specs_dir, 'asdf')
    self.assertEqual(parser.output_dir, 'asdf')

  def test_adoc_args_parse(self):
    parser = postprocess_adoc.parse_args(['--adoc_dir', 'asdf', '--output_dir', 'asdf'])
    self.assertEqual(parser.adoc_dir, 'asdf')
    self.assertEqual(parser.output_dir, 'asdf')
