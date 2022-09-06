import os, csv

### FUNCTIONS ###

# returns a list of relative paths to all csv files in the working folder
def checkDirForCSV(dir_name = "", indent = 0):
    
    if len(dir_name) < 3: print("\t"*indent + "Files found in " + dir_name[3:] + "folder:")
    else: print("\t"*indent + "Files found in \"" + dir_name[3:] + "\" folder:")
    
    files = []
    for entry in os.listdir(dir_name):
        if ".csv" in entry:
            print("\t"*indent + dir_name + "\\" + entry)
            files.append(dir_name + "\\" + entry)
        elif "." not in entry:
            files.extend(checkDirForCSV(dir_name + "\\" + entry, indent + 1))
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
print()

allData = [] # will store the data as one giant table
for file in files:
    open_file = open(file)
    for row in csv.reader(open_file, delimiter = ','):
        if not csvRowEmpty(row) and row not in allData: allData.append(row)
    open_file.close

### DATA LOADED INTO A SINGLE TABLE ###

# manipulate data here

### OUTPUT TABLE AS A FILE ###

try: 
    outputFile = open(".\\FINAL.csv", mode="w", newline="")
except: 
    print("Error: could not create or write to output file.\nThis could be caused by having the file open.\n\nExiting...\n")
    exit()

csv.writer(outputFile).writerows(allData)

outputFile.close()