import sys
from bs4 import BeautifulSoup

def read(file):
    with open(file) as f:
        html = f.read
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    return text

def tokenize(text):
    fileList = []
    delimiters = set("_- \t\n.,*!?;:()[]/{}\"'")

    start = None
    text = text.casefold()

    for i, ch in enumerate(text):
        if ch not in delimiters and ch.isalnum() and ch.isascii():
            if start is None:
                start = i
        else:
            if start is not None:
                fileList.append(text[start:i])
                start = None

    if start is not None:
        fileList.append(text[start:])

    return fileList
    

def updateIndex(tokens):

    return

def inverseIndex(folder):
    index = {}
    fId = 0

    for files in folder:
        fId += 1
        text = read(files)
        tokens = tokenize(text)
        updateIndex(index, tokens, fId)
    return index