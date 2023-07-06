import argparse
import os
import sys
from processing_support import Adoc


def parse_args(args):
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--adoc_dir',
    help='A directory containing the adocs to process'
  )

  parser.add_argument(
    '--partials_dir',
    help='Where to partial adocs are stored'
  )

  parser.add_argument(
    '--output_dir',
    help='Where to write the new docs'
  )

  return parser.parse_args(args)


def main(params=None):
  if params is None:
    params = sys.argv[1:]

  args = parse_args(params)

  if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

  for docDirFile in os.listdir(args.adoc_dir):
    if docDirFile.endswith(".adoc"):
      with open(os.path.join(args.adoc_dir, docDirFile), "r") as adocFile:
        adocLines = adocFile.readlines()

      Adoc.process_adoc(adocLines, args.partials_dir)

      with open(os.path.join(args.output_dir, docDirFile), "w") as processedAdocFile:
        processedAdocFile.writelines(line + '\n' for line in adocLines)

  return 0


if __name__ == '__main__':
  sys.exit(main())
