import sys
import zipfile
import tempfile
from bs4 import BeautifulSoup
from pathlib import Path
from collections import Counter
import json


def read(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        soup = BeautifulSoup(data["content"], "lxml")
        return soup.get_text(" ")

    except Exception as e:
        print(f"Skipping problematic file: {file}")
        return ""

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
    
def updateIndex(index, freq, fId):
    for token, tf in freq.items():

        if token not in index:
            index[token] = []

        index[token].append((fId, tf))
    return

def inverseIndex(folder):
    index = {}
    fId = 0

    for files in folder:
        fId += 1
        text = read(files)
        tokens = tokenize(text)
        freq = Counter(tokens)
        updateIndex(index, freq, fId)
    return index

def create_txt(index, output_file):

    with open(output_file, "w", encoding="utf-8") as f:
        for word in sorted(index.keys()):
            f.write(f"{word}: ")

            postings = []
            for doc_id, frequency in index[word]:
                postings.append(
                    f"(dID{doc_id}, tf{frequency})"
                )

            f.write(", ".join(postings))
            f.write("\n")


def main():
    #zipfile
    zip_path = "developer.zip"

    #output file
    output_file = "inverted_index.txt"

    #temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        #zipfile
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        #find all json file
        json_files = list(Path(temp_dir).rglob("*.json"))

        print(f"Found {len(json_files)} JSON files.")

        #inverted index
        index = inverseIndex(json_files)

        # Write the index to a text file
        create_txt(index, output_file)

        num_documents = len(json_files)
        num_unique_words = len(index)
        index_size_kb = Path("inverted_index.txt").stat().st_size / 1024
    
    print(f"Inverted index saved to: {output_file}")

    print(f"Indexed Documents : {num_documents:,}")
    print(f"Unique Words      : {num_unique_words:,}")
    print(f"Index Size        : {index_size_kb:,.2f} KB")

if __name__ == "__main__":
    main()