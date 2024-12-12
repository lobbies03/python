# from asyncio.format_helpers import extract_stack
from itertools import count
from lib2to3.pytree import convert
import os
import re
from typing import Concatenate
from PyPDF2 import PdfFileReader
from datetime import datetime


def GetPdfFileNames(path):
    searchString = ".pdf"
    files = []
    dirs = os.listdir(path)

    for file in dirs:
        if searchString in file.lower():
            files.append(path + "/" + file)

    return files


def ExtractDatesFromPdf(file):
    dates = []
    reader = PdfFileReader(file)
    page = reader.pages[0]
    # print(page.extractText())
    txt = page.extractText()
    # print(txt)

    # 01.01.2022
    match_str = re.findall(r'\d{2}[- /.]\d{2}[- /.]\d{4}', txt)
    # match_str = re.findall(r'\d{2}.\d{2}.\d{4}', txt)

    # 01 November 2020

    mylist = list(dict.fromkeys(match_str))  # remove duplicates
    # print(mylist)
    return mylist


def SelectDateFromList(dates):
    for i in range(len(dates)):
        print(f"[{i}] {dates[i]}")

    selectedDate = int(input("Bitte Datum wählen: "))
    return dates[selectedDate]


def ConvertDate(date):
    convertedDate = datetime.strptime(date, '%d.%m.%Y')
    # print( convertedDate.date())
    return convertedDate.date()


def RenameFile(file, date):
    f1 = os.path.basename(file)
    f2 = str(date) + "_" + f1
    print(f2)
    path = os.path.dirname(file)
    # print(path)
    inpString = "Rename File from " + f1 + " to " + f2 + "? [y/n] "
    res = input(inpString)
    # exit()
    if (str(res) == "y"):
        os.rename(path + "/" + f1, path + "/" + f2)


path = "/Users/mh/Documents/Programming/Repos/python/pdfFiles"
path = "/Users/mh/Documents/Steuer/2022 Steuer/2022 Belege"
pdfFiles = GetPdfFileNames(path)


for file in pdfFiles:
    pdfDates = ExtractDatesFromPdf(file)
    if (pdfDates == []):
        print(file, "none")
        continue
    print(file)
    selectedDate = SelectDateFromList(pdfDates)
    convertedDate = ConvertDate(selectedDate)
    RenameFile(file, convertedDate)
