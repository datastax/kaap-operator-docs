import argparse
import yaml
import os
import sys
from processing_support import OpenApi


def parse_args(args):
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--specs_dir',
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

  for specDirFile in os.listdir(args.specs_dir):
    if specDirFile.endswith(".yaml"):
      with open(os.path.join(args.specs_dir, specDirFile), "r") as specFile:
        spec = yaml.load(specFile, Loader=yaml.FullLoader)

      processedSpec = OpenApi.process_spec(spec)

      if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

      with open(os.path.join(args.output_dir, spec["info"]["title"] + ".openapi.processed.yaml"), "w") as processedSpecFile:
        yaml.dump(processedSpec, processedSpecFile)

  return 0


if __name__ == '__main__':
  sys.exit(main())
