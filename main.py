import os, csv
from custom_functions import *

print("\nFiles must be in the current folder or in subdirectories of the current folder.\n")

# list to store files
files = checkDirForCSV(".\\")

print()

for file in files:
    open_file = open(file)
    print(open_file.read())
    open_file.close
