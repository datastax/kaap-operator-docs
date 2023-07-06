import sys
import unittest

sys.path.append('..')
from processing_support import Adoc


class TestAdocPostProcessing(unittest.TestCase):

  def setUp(self):
    pass

  def test_process_adoc(self):
    adocLines = [
      '= PulsarCluster',
      ': numbered:',

      '=== PulsarCluster [[PulsarCluster]]',

      '=== PulsarCluster_spec [[PulsarCluster_spec]]',

      '=== PulsarCluster_spec_broker [[PulsarCluster_spec_broker]]',

      '=== PulsarCluster_spec_broker_autoscaler [[PulsarCluster_spec_broker_autoscaler]]'
    ]

    Adoc.process_adoc(adocLines)

    self.assertGreater(adocLines.index("== Pulsarcluster [[PulsarCluster]]"), -1)

    self.assertGreater(adocLines.index("=== Spec [[PulsarCluster_spec]]"), -1)

    self.assertGreater(adocLines.index("==== Broker [[PulsarCluster_spec_broker]]"), -1)

    self.assertGreater(adocLines.index("==== Autoscaler [[PulsarCluster_spec_broker_autoscaler]]"), -1)

    with open('test.adoc', "w") as processedAdocFile:
      processedAdocFile.writelines(line + '\n' for line in adocLines)
