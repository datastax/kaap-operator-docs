import os
import sys
import unittest

import yaml

sys.path.append('..')
from processing_support import OpenApi


class TestOpenApiPreProcessing(unittest.TestCase):

  def setUp(self):
    pass

  def test_process_spec(self):
    with open("test_openapi.yaml", "r") as ymlFile:
      yamlSpec = yaml.load(ymlFile, Loader=yaml.FullLoader)

    OpenApi.process_spec(yamlSpec)

    self.assertEqual(yamlSpec["openapi"], "3.0.0")
