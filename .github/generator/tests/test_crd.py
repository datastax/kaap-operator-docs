import os
import sys
import unittest

sys.path.append('..')
import yaml
from processing_support import Crd


class TestCRDConversion(unittest.TestCase):
  def setUp(self):
    pass

  def test_yaml_conversion(self):
    with open("test_crd.yml", "r") as crdFile:
      crdYaml = yaml.load(crdFile, Loader=yaml.FullLoader)

    specKind = crdYaml["spec"]["names"]["kind"]

    openApiSpec = Crd.convert_crd_to_openapi(crdYaml)

    self.assertEqual(openApiSpec["openapi"], "3.0.0")
    self.assertEqual(openApiSpec["info"]["title"], specKind)
    self.assertEqual(openApiSpec["info"]["version"], "v1alpha1")
    self.assertEqual(openApiSpec["components"]["schemas"]["Test"]["title"], specKind)
    self.assertEqual(openApiSpec["components"]["schemas"]["Test"]["type"], "object")
    self.assertEqual(openApiSpec["components"]["schemas"]["Test"]["xml"], {"name": "test.oss.datastax.com", "namespace": "v1alpha1"})
    self.assertEqual(openApiSpec["components"]["schemas"]["Test"]["properties"], crdYaml["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"])

