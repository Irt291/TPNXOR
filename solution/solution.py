xorChar = lambda a, b : chr(ord(a) ^ ord(b))


def xorFunc(xorKey, inputText):
    inputText = list(inputText)
    
    for i in range(len(inputText)):
        for j in range(len(xorKey)):
            inputText[i] = xorChar(inputText[i], xorKey[j])
            
    return inputText



if __name__ == "__main__":
    data, output = input().split()
    xorKey = xorChar(data[0], output[0])
    q = int(input())
    
    for _ in range(q):
        print(*xorFunc(xorKey, input()), sep="")