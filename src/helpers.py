import os
import shutil

from conversion import *


def generatePage(fromPath, templatePath, destPath):
    print(f'Generating page from {fromPath} to {destPath} using {templatePath}')
    fileMd = readFile(fromPath)
    templateFile = readFile(templatePath)
    htmlNode = md_to_HTMLNode(fileMd)
    title = extractTitle(fileMd)
    outfile = templateFile.replace('{{ Title }}', title)
    outfile = templateFile.replace('{{ Content }}', htmlNode.toHTML())
    writeFile(destPath, outfile)

def generatePagesR(dirPath, templatePath, destDirPath):
    lDir = os.listdir(dirPath)
    for path in lDir:
        p = os.path.join(dirPath, path)
        if os.path.isfile(p):
            generatePage(p, templatePath, os.path.join(destDirPath, path).replace(".md", '.html'))
        else:
            generatePagesR(p, templatePath, os.path.join(destDirPath, path))
    

def copyStatic(source, target):
    if not os.path.exists(target):
        os.mkdir(target)
    for item in os.listdir(source):
        sourceP = os.path.join(source, item)
        targetP = os.path.join(target, item)
        if not os.path.isfile(sourceP):
            copyStatic(sourceP, targetP)
        else:
            shutil.copy(sourceP, targetP)

    return

def readFile(path: str, mode: str = "r", encoding: str = "utf-8") -> str:
    with open(path, mode, encoding=encoding if "b" not in mode else None) as f:
        return f.read()


def writeFile(path: str, data: str, mode: str = "w", encoding: str = "utf-8") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding=encoding if "b" not in mode else None) as f:
        f.write(data)


def extractTitle(markdown):
    mdList = markdown.split("\n")
    for line in mdList:
        if line.startswith("# "):
            return line.replace("# ", "")
    raise ValueError("No title found")