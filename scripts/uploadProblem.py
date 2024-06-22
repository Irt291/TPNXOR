import sys
import json
from pathlib import Path
from utils.api import NHPClient
from utils.models import Problem
from utils.fileUtils import readFile


# python -B scripts/uploadProblem.py --sessionid 62ndognbaboude5pxruc2cbk2fbslo3o --url http://localhost
client = NHPClient(sessionID=sys.argv[2], baseURL=sys.argv[4])


print("Upload TestCase...")  
testCaseID = client.uploadTestCase(Path(r"./build/testcase.zip"))["id"]
print("Ok!")


metadata = json.loads(readFile(r"./build/problem.json"))
metadata["test_case_id"] = testCaseID


EDIT = False
old = client.queryProblem(metadata["id"])


if (old is not None) and len(old) != 0:
    metadata["n_id"] = old[0]["id"]
    print()
    print(f'=== Edit mode for current problem. Dont forget to delete old testcase under /data/backend/test_case/{old[0]["test_case_id"]} ===')
    print()
    EDIT = True
else:
    print("Creating problem...")


problem = Problem.model_validate(metadata)

print(problem)

response = client.editProblem(problem, edit=EDIT)
print(response) # None = ok
print("Ok!")


newProblem = client.queryProblem(metadata["id"])

if newProblem:
    print()
    print("Download problem export archive...")
    prbID = int(newProblem[0]["id"])
    with open(f"./build/problem-export.zip", "wb") as fp:
        fp.write(client.downloadExportedProblemArchive(problemID=prbID))
    print("Done -> build/problem-export.zip")