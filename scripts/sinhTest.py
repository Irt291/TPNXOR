import os
import sys
import json
import time
import random
import pathlib
import hashlib
import multiprocessing
from utils.archive import zipDir
from utils.fileUtils import readFile


def writeTest(
    outputDir: str,
    testCount: int,
    inputContent: str,
    outputContent: str
):
    name = f"{outputDir}{os.sep}{testCount}"    
    
    with open(name + ".in",  "w") as inpBuff:
        inpBuff.write(inputContent)

    with open(name + ".out", "w") as outBuff:
        outBuff.write(outputContent) 

        
        
def ensurePrintableAns(i_xorKey: int, length: int):
    text, result = "", ""
    for _ in range(length):
        while True:
            inpChar = chr(random.randint(33, 126))
            outChar = chr(
                ord(inpChar) ^ i_xorKey
            )
            if (33 <= ord(outChar) <= 126) and inpChar.isprintable() and outChar.isprintable():
                text += inpChar
                result += outChar
                break
    
    return text, result
        
    

def generateTestCase(
    testCount: int,
    outputDir: str,
    minStringLength: int,
    maxStringLength: int,
    minQueries: int,
    maxQueries: int,
    score: int
):
    start = time.perf_counter()
    queryCount = random.randint(minQueries, maxQueries)
    queriesIN, queriesOUT = "", ""
    
    randomStrLength = lambda : random.randint(minStringLength, maxStringLength)
    
    i_xorKey = random.randint(33, 126)
    data, output = ensurePrintableAns(i_xorKey, randomStrLength())
    
    for _ in range(queryCount):
        text, result = ensurePrintableAns(i_xorKey, randomStrLength())
        queriesIN += (text + "\n")
        queriesOUT += (result + "\n")
    
    inputContent = f"{data} {output}\n{queryCount}\n{queriesIN}"
    outputContent = queriesOUT
    
    writeTest(
        outputDir = outputDir,
        testCount = testCount,
        inputContent = inputContent,
        outputContent = outputContent
    )
    
    stop = time.perf_counter()
    took = stop - start
    print(f"Test {testCount}: {queryCount} queries, took {took:.2f}s")
    
    outputMD5 = hashlib.md5(queriesOUT.strip().encode("utf-8")).hexdigest()
    return {
        "stripped_output_md5": outputMD5,
        "input_size": len(inputContent),
        "output_size": len(outputContent),
        "input_name": f"{testCount}.in",
        "output_name": f"{testCount}.out",
        "score": score
    }
    





def main():
# python -B scripts/sinhTest.py --amount 100 --minstrlen 100 --maxstrlen 1000 --minquery 100 --maxquery 1000
    OUTPUT_DIR = r"./build/testcase"
    START = 1
    AMOUNT = int(sys.argv[2])
    MAKE_ARCHIVE = True
    RANDSTR_MIN_LENGTH = int(sys.argv[4])
    RANDSTR_MAX_LENGTH = int(sys.argv[6])
    
    RANDOM_MIN_QUERIES =  int(sys.argv[8])
    RANDOM_MAX_QUERIES = int(sys.argv[10])

    TOTAL_SCORE: int = json.loads(readFile(r"./metadata.json"))["total_score"]
        
    SCORE_EACH_TEST, mod = divmod(TOTAL_SCORE, AMOUNT)

    if mod != 0:
        print("\n=== Error: Tong diem phai chia het cho so test! ===\n")
        exit(1)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Cho Doi La Vinh Quang!")    
            
    args = [
        (
            testCount,
            OUTPUT_DIR,
            RANDSTR_MIN_LENGTH,
            RANDSTR_MAX_LENGTH,
            RANDOM_MIN_QUERIES,
            RANDOM_MAX_QUERIES,
            SCORE_EACH_TEST
        )
        for testCount in range(START, AMOUNT+START)
    ]
    
    threads = multiprocessing.cpu_count()
    
    print(f"Using {threads} threads!")
    
    with multiprocessing.Pool(threads) as pl:
        results = pl.starmap(generateTestCase, args)
        
    with open(r"./build/testcase.json", "w") as fp:
        json.dump(results, fp, indent=4)
   
    
    if MAKE_ARCHIVE:
        zipDir(pathlib.Path(OUTPUT_DIR))    
    
    


if __name__ == "__main__":
    print("Sinh Test...")
    start = time.perf_counter()
    main()
    stop  = time.perf_counter()
    took = stop - start
    print(f"Sinh Test Xong! (mat tong cong {took:.2f} giay)")