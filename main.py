import os, csv

# some parts of the script print formatted text to the console
spaces_in_indent = 4

# checks if a row of a parsed csv is empty. returns true if so.
def csvRowEmpty(row):
    isEmpty = True
    for entry in row:
        if entry != "":
            isEmpty = False
    return isEmpty

def csvColEmpty(array, col):
    isEmpty = True
    for entry in array:
        if entry[col] != "":
            isEmpty = False
    return isEmpty

# returns a list of relative paths to all csv files in the given directory
# defaults to directory outside of the directory the script is in
def find_csv_paths(dir_name = "..", num_indents = 0, skip_this = True):

    global spaces_in_indent

    print(" "*spaces_in_indent*num_indents + "in \"" + dir_name.split("\\")[-1] + "\":")
    num_indents = num_indents + 1
    files = []

    for entry in os.listdir(dir_name):

        if ".csv" in entry: # for a csv file

            print(" "*spaces_in_indent*num_indents + "-> " + entry)
            files.append(dir_name + "\\" + entry)

        elif "." not in entry: # for anything without a file extension

            new_dir_name = dir_name + "\\" + entry

            # check if we actually want to look at this directory
            if skip_this and ("python-csv" in new_dir_name):
                print(" "*spaces_in_indent*num_indents + "\nskipping \"python-csv\" directory!\n")
                continue

            try:
                os.listdir(new_dir_name)
                files.extend(find_csv_paths(new_dir_name, num_indents))
            except:
                pass

    if not files:
        print(" "*spaces_in_indent*num_indents + "no csv files found")

    return files

files = find_csv_paths(skip_this=True) # check for csv files, skipping this repo
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

# store the data as one giant table
allData = []
for file in files:
    open_file = open(file)
    print("Adding file \"" + file + "\"...")
    for row in csv.reader(open_file, delimiter = ','):
        if not csvRowEmpty(row) and row not in allData:
            allData.append(row)
    open_file.close
print()

# remove empty columns
def remove_empty_columns(array):
    num_columns_deleted = 0
    for column_index in range(len(array[0])):

        # check if the column is empty (aside from the header)
        is_empty = True
        for entry in array[1:]:
            if entry[column_index - num_columns_deleted] != "":
                is_empty = False
                break

        # if the column is empty, delete it
        if is_empty:
            for row in array:
                row.pop(column_index - num_columns_deleted)
            num_columns_deleted = num_columns_deleted + 1
    return array

allData = remove_empty_columns(allData)

### OUTPUT TABLE TO A FILE ###

finalFileName = "0-combined_data.csv"

try:
    outputFile = open(".\\output_data\\" + finalFileName, mode="w", newline="")
except:
    print("Error: could not create or write to output file.\nThis will throw if you have the file open.\n\nExiting...\n")
    exit()

csv.writer(outputFile).writerows(allData)

outputFile.close()

print("Combined csv entitled \"" + finalFileName + "\"\n\nExiting...\n")

### SEPARATE ROWS INTO SEPARATE FILES BY COLUMN VALUE ###

col_a = 1 # EDIT THESE FOR YOUR APPLICATION
col_b = 2 # EDIT THESE FOR YOUR APPLICATION

for event in allData[1:]:
    if event[2] == '84cdc981' or event[2] == '27043ba4' or event[2] == '0C490A1':
        print(event)

if (col_a != 'no column specified') or (col_b != 'no column specified'):

    unique_THINGs = []
    this_row_THING = []

    print("\nCreating files for individual THINGs by unique column values of {} and {}...\n".format(allData[0][col_a], allData[0][col_b]))

    print("Creating files for:\n")
    print("{a:^22}|{b:^22}".format(a = allData[0][col_a], b = allData[0][col_b]))
    print("---------------------------------------------")

    for row in allData[1:]:

        this_row_THING = [row[col_a], row[col_b]]

        if this_row_THING not in unique_THINGs:

            temp_data = []

            unique_THINGs.append(this_row_THING)

            print("|{a:^21}|{b:^21}|".format(a = this_row_THING[0], b = this_row_THING[1]))

            for event in allData[1:]:
                #print(event)
                try:
                    if event[col_b] == this_row_THING[1]:
                        if event[col_a] == this_row_THING[0]:
                            temp_data.append(event)
                            #print(event)
                except:
                    pass
                    #print("fail on: {}".format(event))
                    #exit()

            temp_data = remove_empty_columns(temp_data)

            try:
                outputFile = open(".\\output_data\\{a}_{b}.csv".format(a=this_row_THING[0], b=this_row_THING[1]), mode="w", newline="")
            except:
                print("Error: could not create or write to output file.\nExiting...\n")
                exit()

            csv.writer(outputFile).writerows(temp_data)

            outputFile.close()

    print("---------------------------------------------")

else:

    print("\nColumns not specified, so no extra files will be created.")
