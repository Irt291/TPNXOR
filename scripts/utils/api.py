import httpx
import pathlib
import utils.models as models

class NHPClient:
    def __init__(self, sessionID: str, baseURL: str = "http://localhost"):
        self.httpClient = httpx.Client(
            timeout = None,
            base_url = baseURL,
            cookies = {
                "sessionid": sessionID
            }
        )
        self.httpClient.get(url="/api/profile") # get CSRF token
        csrfToken: str = self.httpClient.cookies.get("csrftoken", "") # type: ignore
        self.httpClient.headers.update(
            {
                "X-CSRFToken": csrfToken
            }
        ) # Nam 2024 ma van con csrf sao ??? met
        
        # Check Auth
        isAuthenticated = self.httpClient.get(url="/api/profile").json()["data"]
        if isAuthenticated is None:
            print("Not Authenicated!")
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
        ).json()
        
        
        return self.raiseError(response)
    
    
    def editProblem(self, metadata: models.Problem, edit: bool = False):
        data = metadata.model_dump()        
        data["_id"] = data["id"]        
        if edit:
            method = self.httpClient.put
            data["id"] = data["n_id"]
        else:
            method = self.httpClient.post
            del data["id"]
    
        del data["n_id"]
        
        response = method(
            url = "/api/admin/problem",
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8"
            },
            json = data
        ).json()
        return self.raiseError(response)
        
    
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
            ).json()
            self.raiseError(response)
        
        return True

    
    def downloadExportedProblemArchive(self, problemID: int) -> bytes:
        response = self.httpClient.get(
            url = "api/admin/export_problem",
            params = {
                "problem_id": problemID
            }
        )
        return response.read()
        
        
    