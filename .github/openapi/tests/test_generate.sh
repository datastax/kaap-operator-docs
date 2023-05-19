#bin/bash

set -e

../openapi-generator-cli.sh generate \
  -g asciidoc \
  -o ./out/gen \
  -i ../../generator/tests/test_openapi.yaml \
  --additional-properties=legacyDiscriminatorBehavior=false,disallowAdditionalPropertiesIfNotPresent=false,sortModelPropertiesByRequiredFlag=true,sortParamsByRequiredFlag=true \
  --remove-operation-id-prefix \
  -t ../templates \
  --inline-schema-name-defaults arrayItemSuffix=,mapItemSuffix=

rm -rf ./out