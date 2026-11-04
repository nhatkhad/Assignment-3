import sys
from bs4 import BeautifulSoup

def read(file):
    fileList = []
    delimiters = set("_- \t\n.,*!?;:()[]/{}\"")
    
    with open(file, 'r') as f:
        for line in f:
            # start is the start of the word, for splicing later
            start = None
            line2 = line.casefold()
            #go line by line, andthen check characters in the line
            for i, ch in enumerate(line2):
                if ch not in delimiters and ch.isalnum() and ch.isascii():
                    if start is None:
                        # begins the start of the word
                        start = i
                else:
                    if start is not None:
                        # splice from start to the before the current character, that is now the word
                        fileList.append(line2[start:i])
                        start = None
            #adds the last word
            if start is not None:
                fileList.append(line2[start:])
    return fileList

def tokenize(path):
        fileList = []
        delimiters = set("_- \t\n.,*!?;:()[]/{}\"")
        
        with open(path, 'r') as f:
            for line in f:
                # start is the start of the word, for splicing later
                start = None
                line2 = line.casefold()
                #go line by line, andthen check characters in the line
                for i, ch in enumerate(line2):
                    if ch not in delimiters and ch.isalnum() and ch.isascii():
                        if start is None:
                            # begins the start of the word
                            start = i
                    else:
                        if start is not None:
                            # splice from start to the before the current character, that is now the word
                            fileList.append(line2[start:i])
                            start = None
                #adds the last word
                if start is not None:
                    fileList.append(line2[start:])
        return fileList
    return tokens

def updateIndex(tokens):

    return

def inverseIndex(folder):
    for files in folder:
        text = read(file)
        tokens = tokenize(text)
        updateIndex(tokens)
    return index