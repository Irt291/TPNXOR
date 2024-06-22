# https://github.com/Harry-zklcdc/OnlineJudge/blob/186dad9341f6bf222f6cb4b0758335bb00173dfc/problem/views/admin.py#L4

# by Irt291

import typing
import pydantic


# class User(pydantic.BaseModel):
#     id: int
#     username: str
#     real_name: typing.Optional[str] = None



class Problem(pydantic.BaseModel):
    n_id: typing.Optional[int] = None
    id: str # display id eg: TPNXOR
    title: str # Long title eg: Thien Phuc Beo Va Xor
    visible: bool = False
    difficulty: typing.Literal["Low", "Mid", "High"] = "Low" # tim kiem nhi phan nhe
    tags: list[str]
    
    rule_type: typing.Literal["OI", "ACM"] = "OI"
    total_score: int = 100
    source: str = "Irt291"
    share_submission: bool = False
    
    
    # For Contest
    contest: typing.Optional[typing.Any] = None # luoi implement contest obj
    is_public: bool = True
    
    #HTML
    description: str
    input_description: str
    output_description: str
    hint: typing.Optional[str] = None # Optional
    
    #Test Case Stuff
    samples: list[dict] # "samples":[{"input":"mrp","output":"mrp"}
    test_case_id: str
    test_case_score: list[dict]  # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    
    
    # Language Stuff
    languages: typing.List[
        typing.Literal[
            "C",
            "C++",
            "C#",
            "Java",
            "Python3",
            "Python2",
            "Pascal",
            "Golang"
        ]
    ] = ["Python3", "Python2", "C", "C++", "C#", "Golang", "Java"]
    template: dict = {}
    
    # created_by: typing.Optional[User] = None
    
    # Judge
    time_limit: int = 1000  # ms
    memory_limit: int = 512  # MB
    io_mode: dict = {
        "io_mode": "Standard IO",
        "input": "input.txt",
        "output": "output.txt"
    }
    
    # Special Judge
    spj: bool = False
    spj_language: typing.Optional[str] = None
    spj_code: typing.Optional[str] = None
    spj_version: typing.Optional[str] = None
    spj_compile_ok: bool = False
    
    
    
    
    
    