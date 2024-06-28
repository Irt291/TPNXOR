import httpx
import pathlib
import utils.models as models

class NHPClient:
    def __init__(self, sessionID: str, baseURL: str = "http://localhost"):
        self.httpClient = httpx.Client(
            timeout = None,
            base_url = baseURL,
            http2 = True,
            cookies = {
                "sessionid": sessionID
            }
        )
        self.httpClient.get(url="/api/profile") # get CSRF token
        csrfToken: str = self.httpClient.cookies.get("csrftoken", "") # type: ignore
        self.httpClient.headers.update(
            {
                "X-CSRFToken": csrfToken,
                # "Referer": "https://nhpoj.net/"
            }
        ) # Nam 2024 ma van con csrf sao ??? met
        isAuthenticated = self.httpClient.get(url="/api/profile").json()["data"]
        if isAuthenticated is None:
            print("\n=== Not Authenicated! ===\n")
            exit(1)
        else:
            print(f'=== Login as {isAuthenticated["user"]["username"]}. ===')
            
        
    def raiseError(self, response: dict):
        error = response["error"]
        if error is not None:
            raise Exception(error + " " + response["data"])
        else:
            return response["data"]
    
    
    def queryProblem(self, problemID: str):
        response = self.httpClient.get(
            url = "/api/admin/problem",
            params = {"problem_id": problemID,}
        ).json()["data"]
        return None if response == "Problem does not exist" else response["results"]
    
    
    def uploadTestCase(self, testCaseArchive: pathlib.Path):  
        response = self.httpClient.post(
            url = "/api/admin/test_case",
            headers = {
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "multipart/form-data; boundary=------WebKitFormBoundaryMrPDepTraiKhoaiTo" # wtf is it?
            },
            data = {"spj": False},
            files = {"file": testCaseArchive.open(mode="rb")}
        )
        return self.raiseError(response.json())
    
    
    def editProblem(self, metadata: models.Problem, edit: bool = False):
        data = metadata.model_dump()        
        data["_id"] = data["id"]        
        if edit:
            httpMethod = self.httpClient.put
            data["id"] = data["n_id"]
        else:
            httpMethod = self.httpClient.post
            del data["id"]
    
        del data["n_id"]
        
        response = httpMethod(
            url = "/api/admin/problem",
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8"
            },
            json = data
        )
        return self.raiseError(response.json())
        
    
    def deleteProblem(self, problemID: str):
        results = self.queryProblem(problemID)
        if results is None: return False
        
        for problem in results:
            print(f'Delete {problemID} id {problem["id"]}')
            response = self.httpClient.delete(
                url = "/api/admin/problem",
                params = {
                    "id": problem["id"]
                }
            )
            self.raiseError(response.json())
        
        return True

    
    def downloadExportedProblemArchive(self, problemID: int) -> bytes:
        response = self.httpClient.get(
            url = "api/admin/export_problem",
            params = {
                "problem_id": problemID
            }
        )
        return response.read()
        
        
    