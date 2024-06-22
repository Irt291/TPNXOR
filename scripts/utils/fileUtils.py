def readFile(filename: str):
    with open(file=filename, mode="r", encoding="utf-8") as io:
        return io.read()