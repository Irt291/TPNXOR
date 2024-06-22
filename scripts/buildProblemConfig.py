import json
from pathlib import Path
from utils.fileUtils import readFile
from utils.htmlParser import htmlParser

print("Build Problem Conf...")

descriptionHTML = htmlParser(readFile(r"./src/Description/ProblemDescription.md"))
inputDescriptionHTML = htmlParser(readFile(r"./src/Description/InputDescription.md"))
outputDescriptionHTML = htmlParser(readFile(r"./src/Description/OutputDescription.md"))
hintHTML = htmlParser(readFile(r"./src/Description/Hint.md"))


metadata = json.loads(readFile(r"./metadata.json"))

metadata["description"] = descriptionHTML
metadata["input_description"] = inputDescriptionHTML
metadata["output_description"] = outputDescriptionHTML
metadata["hint"] = hintHTML


samples = []
for inputFile in Path(r"./src/Description/samples").glob("*.in"):
    outputFile = inputFile.with_suffix(".out").open("r")
    inputFile = inputFile.open("r")
    inputContent = inputFile.read()
    outputContent = outputFile.read()
    inputFile.close()
    outputFile.close()
    samples.append(
        {
            "input": inputContent,
            "output": outputContent
        }
    )
metadata["samples"] = samples

metadata["test_case_score"] = json.loads(readFile(r"./build/testcase.json"))


with open(r"./build/problem.json", "w") as fp:
    json.dump(metadata, fp, indent=4)
    

print("Ok -> ./build/problem.json")