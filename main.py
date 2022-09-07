import os, csv

### FUNCTIONS ###

# returns a list of relative paths to all csv files in the working folder
def checkDirForCSV(dir_name = "", indent = 0):
    print("\t"*indent + "Files found in \"" + dir_name + "\" folder:")
    indent += 1
    files = []
    for entry in os.listdir(dir_name):
        if ".csv" in entry: # for a csv file
            print("\t"*indent + dir_name + "\\" + entry)
            files.append(dir_name + "\\" + entry)
        elif "." not in entry: # for a subfolder
            files.extend(checkDirForCSV(dir_name + "\\" + entry, indent))
    return files

# checks if a row of a parsed csv is empty. returns true if so.
def csvRowEmpty(row):
    isEmpty = True
    for entry in row:
        if entry != "": isEmpty = False
    return isEmpty

### END FUNCTIONS ###

print("\nFiles must be in the current folder or in subdirectories of the current folder.")
print("All files must have the same headers. note that including a previous output of this file is fine.\n")

# list to store files
files = checkDirForCSV(".\\") # check for csv files in the current directory
files.sort()
print()

# this block confirms which files should be used. any entry throws error, do not use.
"""
allFilesInput = input("all of these files will be combined. is this correct? (y/n):")
print(allFilesInput)

if allFilesInput.lower == "n": 
    for file in files:
        use = input("Use file \"" + file + "\"? (y/n):")
        if use.lower == "y": continue
        elif use.lower != "n":
            print("Error: invalid input.\nPlease enter y or n next time.\n\nExiting...\n")
            exit()
        else: files.remove(file)
elif allFilesInput.lower != "y":
    print("Error: invalid input.\nPlease enter y or n next time.\n\nExiting...\n")
    exit()
"""

allData = [] # will store the data as one giant table
for file in files:
    open_file = open(file)
    print("Adding file \"" + file + "\"...")
    for row in csv.reader(open_file, delimiter = ','):
        if not csvRowEmpty(row) and row not in allData: allData.append(row)
    open_file.close
print()

### DATA LOADED INTO A SINGLE TABLE ###

# manipulate data here.

### OUTPUT TABLE AS A FILE ###

finalFileName = "FINAL.csv"

try: 
    outputFile = open(".\\" + finalFileName, mode="w", newline="")
except: 
    print("Error: could not create or write to output file.\nThis will throw if you have the file open.\n\nExiting...\n")
    exit()

print("Combining...\n")
csv.writer(outputFile).writerows(allData)

outputFile.close()

print("Combined csv entitled \"" + finalFileName + "\"\n\nExiting...\n")