import os
import yaml


class Adoc:

  @staticmethod
  def __calculate_new_model_name(splitModelName: list) -> str:
    return splitModelName[-1]

  @staticmethod
  def __find_partials_for_model(modelNamespace: str, partialsDir: str) -> list:
    partials = []

    for partial in os.listdir(partialsDir):
      with open(os.path.join(partialsDir, partial), "r") as partialFile:
        partialContents = partialFile.read()

      if partialContents.find(':crd-namespace: "' + modelNamespace + '"') > -1:
        partials.append(partial)

    return partials

  @staticmethod
  def __add_yaml_model_example(lines: list, kind: str, modelNames: list):

    baseYaml = {
      "apiVersion": "pulsar.oss.datastax.com/v1alpha1",
      "kind": kind.title(),
      "metadata": {
        "name": "example-pulsarcluster"
      },
      "spec": {}
    }

    current_dict = baseYaml["spec"]

    for modelName in modelNames[2:]:  # The first two are the kind and "spec"
      current_dict[modelName] = {}
      current_dict = current_dict[modelName]

    lines.append("Example use:")
    lines.append("")
    lines.append("[source,yaml]")
    lines.append("----")
    lines.extend(yaml.dump(baseYaml).split("\n"))
    lines.append("----")

  @staticmethod
  def process_adoc(adocLines: list, partialsDir: str = None):
    lines = adocLines.copy()
    kind = ""
    adocIdx = 0

    for linesIdx, line in enumerate(lines):
      if not line.startswith("=== "):
        adocIdx += 1
        continue

      newLines = []
      splitLine = line.replace("=== ", "").split(" ")
      modelName = splitLine[0].strip().lower()
      modelLink = splitLine[1].strip()
      splitModelNames = modelName.split("_")
      newModelName = Adoc.__calculate_new_model_name(splitModelNames)
      headerDepth = len(splitModelNames) + 1
      modelNamespace = ".".join(splitModelNames).title()

      if len(splitModelNames) == 1:
        kind = modelName

      if headerDepth > 4:
        headerDepth = 4

      newLines.append(('=' * headerDepth) + " " + newModelName.title() + " " + modelLink)
      newLines.append("")

      if partialsDir:
        for partial in Adoc.__find_partials_for_model(modelNamespace, partialsDir):
          newLines.append(partial + " \n")
          newLines.append("")

      if len(splitModelNames) > 1:
        newLines.append("Complete namespace: " + modelNamespace)
        newLines.append("")

      if len(splitModelNames) > 2:
        Adoc.__add_yaml_model_example(newLines, kind, splitModelNames)

      if len(newLines) > 0:
        adocLines.pop(adocIdx)  # remove old line
        for newLine in newLines:  # go through new lines
          adocLines.insert(adocIdx, newLine)  # insert new line
          adocIdx += 1
      else:
        adocIdx += 1  # no new lines, just increment

    return


class Crd:
  @staticmethod
  def convert_crd_to_openapi(crdSpec: yaml) -> yaml:
    crdKind = crdSpec["spec"]["names"]["kind"]

    apiSpec = """
      openapi: 3.0.0
      info:
        title: 
        version:
        description:
      paths: {}
      components:
        schemas:
      """

    apiYml = yaml.load(apiSpec, Loader=yaml.FullLoader)
    apiYml["info"]["title"] = crdKind
    apiYml["info"]["version"] = crdSpec["spec"]["versions"][0]["name"]
    apiYml["info"]["description"] = "Auto generated from CRD spec"
    apiYml["components"]["schemas"] = {
      crdKind:
        {
          "xml": {
            "name": crdSpec["spec"]["group"],
            "namespace": crdSpec["spec"]["versions"][0]["name"]
          },
          "title": crdKind,
          "type": "object",
          "properties": crdSpec["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]
        }
    }

    return apiYml


class OpenApi:
  @staticmethod
  def process_spec(spec: yaml):
    return
