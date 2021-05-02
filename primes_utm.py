#!/usr/bin/env python3
import os
import os.path as path
import re
from urllib.request import urlretrieve
from zipfile import ZipFile

URLS = [(
    f"prime_db/primes{i}.zip",
    f"https://primes.utm.edu/lists/small/millions/primes{i}.zip",
    f"prime_db/primes{i}.txt"
) for i in range(1, 51)]
OUTPUT_FILE = "primes.json"
OUTPUT_ZIP_FILE = "primes.zip"
SEPERATOR = ",\n"
NUMBER_STRING = ""


def collate_primes():
    for file, url, text_file in URLS[0:-1]:
        if not path.exists(file):
            urlretrieve(url, filename=file)
        if not path.exists(text_file):
            with ZipFile(file, 'r') as zipfile:
                zipfile.extractall('prime_db/')

    file, url, text_file = URLS[-1]
    if path.exists(file):
        os.remove(file)
    if path.exists(text_file):
        os.remove(text_file)
    urlretrieve(url, filename=file)
    with ZipFile(file, 'r') as zipfile:
        zipfile.extractall('prime_db/')
    del file, url, text_file

    numbers = list()
    for file, url, text_file in URLS:
        with open(text_file, 'r') as text_file_text:
            text_file_text.readline()
            for line in text_file_text.readlines():
                if line.strip():
                    numbers.append(re.sub(" +", SEPERATOR, line.strip()))

    NUMBER_STRING = SEPERATOR.join(numbers)
    del numbers

    if path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    with open(OUTPUT_FILE, 'w') as output_file:
        output_file.write(f"""[
{NUMBER_STRING}
]""")
    if path.exists(OUTPUT_ZIP_FILE):
        os.remove(OUTPUT_ZIP_FILE)
    # Nah, Not working
    # with ZipFile(OUTPUT_ZIP_FILE, 'w', compression=ZipFile.ZIP_DEFLATED) as zipfile:
    #     zipfile.write(OUTPUT_FILE)
    #     zipfile.close()


if __name__ == '__main__':
    collate_primes()
