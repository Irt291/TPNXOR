import io
import base64
import markdown
from PIL import Image
from pathlib import Path
from bs4 import BeautifulSoup
from utils.fileUtils import readFile



def convertImageToBase64(html):
    cook = BeautifulSoup(html, "html.parser")
    for imageTag in cook.find_all("img"):
        url = imageTag["src"]
        if "data:" in url: continue
        imagePath = (r"./src/Assets" / Path(url)).resolve()
        if imagePath.suffix in [".png", ".jpg", ".webp"]:
            with Image.open(imagePath.open("rb")) as img:
                imgBuffer = io.BytesIO()
                img.save(
                    fp = imgBuffer,
                    format = "WEBP",
                    lossless = True,
                    quality = 100,
                    method = 6,
                    exact = True
                )
                b64 = base64.b64encode(imgBuffer.getvalue()).decode("utf-8")
                imageTag["src"] = f"data:image/webp;base64,{b64}"
        
    return cook.decode()


def parseCSSFile(content: str):
    return content \
        .replace("ngu {", "") \
        .replace("}", "") \
        .replace(" ", "") \
        .replace("\n", "")
        

# <img src="/api/logout"> troll viet nam XSS :))
def usingCustomCSS(html: str, customCSS: str):
    return f"""
<div style='{customCSS}'>
    {html}
</div>
"""


def htmlParser(markdownContent: str):
    html = markdown.markdown(markdownContent)
    html = convertImageToBase64(html)
    customCSS = parseCSSFile(readFile(r"./src/Description/custom.css"))
    html = usingCustomCSS(html, customCSS)
    return html
