import argparse
import os
import sys
import yaml
from processing_support import Crd


def parse_args(args):
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--crds_dir',
    help='A directory containing the CRDs to convert to OpenAPI'
  )

  parser.add_argument(
    '--output_dir',
    help='Where to write the new specs'
  )

  return parser.parse_args(args)


def main(params=None):
  if params is None:
    params = sys.argv[1:]

  args = parse_args(params)

  for crdSpec in os.listdir(args.crds_dir):
    if crdSpec.endswith(".yaml") | crdSpec.endswith(".yml"):
      with open(os.path.join(args.crds_dir, crdSpec), "r") as crdYaml:
        crdSpec = yaml.load(crdYaml, Loader=yaml.FullLoader)

      yamlSpec = Crd.convert_crd_to_openapi(crdSpec)

      if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

      with open(os.path.join(args.output_dir, crdSpec["spec"]["names"]["kind"] + ".openapi.yaml"), "x") as f:
        yaml.dump(yamlSpec, f)

  return 0


if __name__ == '__main__':
  sys.exit(main())
