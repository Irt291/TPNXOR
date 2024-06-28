import base64
xorChar = lambda a, b : chr(ord(a) ^ ord(b))
def xorFunc(key, data):
    data = list(data)
    
    for i in range(len(data)):
        for j in range(len(key)):
            data[i] = xorChar(data[i], key[j])
            
    return "".join(data)

secretKey = "nhphu87"
def checkContestPassword(contestID: int, contestPassword: str):
    return contestPassword

def decodeB(base32: str):
    return base64.b32decode(base32 + "======").decode("utf-8")
    
    


contestID = 69
contestPassword = "111222333"



result = checkContestPassword(
    contestID = contestID,
    contestPassword = xorFunc(
        key = "nhpoj",
        data = decodeB(
            xorFunc(
                key = secretKey,
                data = ",1Q7#-&3#!"
            )
        )
    ) + contestPassword
)


print(xorFunc(key=secretKey, data="%V"))
print(xorFunc(key="nghoangphudeptrai123", data=")64"))
print(xorFunc(key="nghoangphudeptrai123", data="',1=!*(v0"))
# print(result)






#print(xorFunc(key="nghoangphudeptrai123", data="',1=!*(00")) # 2 so 0 lo roi