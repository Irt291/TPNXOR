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
        imagePath = (r"./src/Assets" / Path(imageTag["src"])).resolve()
        with Image.open(imagePath.open("rb")) as img:
            pngImage = io.BytesIO()
            img.save(fp=pngImage, format="PNG")
            b64 = base64.b64encode(pngImage.getvalue()).decode("utf-8")
            imageTag["src"] = f"data:image/png;base64,{b64}"
        
    return cook.decode()


def parseCSSFile(content: str):
    return content \
        .replace("ngu {", "") \
        .replace("}", "") \
        .replace(" ", "") \
        .replace("\n", "")
        
        
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
