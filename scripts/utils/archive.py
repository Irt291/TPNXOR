import os
import zipfile
import pathlib


def zipDir(folder: pathlib.Path):
    outputFile = folder.with_suffix(".zip")
    with zipfile.ZipFile(
        mode = "w",
        file = outputFile,
        allowZip64 = True, # deflate 64 chua dc implement tren server cay the nho
        compresslevel = 9,
        compression = zipfile.ZIP_BZIP2,
        strict_timestamps = True,
    ) as zipBuff:
        for file in folder.rglob("*"):
            arcname = os.sep.join(file.parts[len(folder.parts):])
            zipBuff.write(
                filename = file,
                arcname = arcname
            )
            print(f"Write: {arcname} -> {outputFile}")
    
    outputSize = os.path.getsize(outputFile) / (1024 ** 2) # MB
    print(f"Exported to {outputFile.name} ({outputSize:.2f} MB)")
    
