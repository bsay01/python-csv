import os, pandas

# some parts of the script print formatted text to the console
spaces_in_indent = 4

print("\nLooking for files...\n")

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

print("\nFile search complete\n")

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

print("Compiling files...\n")

complete_dataframe = pandas.DataFrame()
for file in files:
    print("Adding file \"" + file + "\"...")
    complete_dataframe = pandas.concat([complete_dataframe, pandas.read_csv(file, dtype='unicode')]).drop_duplicates()
complete_dataframe.sort_values('time')

print("\nFile compilation complete\n")

print("Fixing \"NaN\" values and removing empty columns")

complete_dataframe.replace("", float("NaN"), inplace=True)
complete_dataframe.dropna(how = 'all', axis = 1, inplace=True)

print("\nCreating file containing combined data")

complete_dataframe.to_csv(".\\output_data\\0-combined_data.csv")

### SEPARATE ROWS INTO SEPARATE FILES BY COLUMN VALUE ###

col_a = 'no column specified' # EDIT THESE FOR YOUR APPLICATION
col_b = 'no column specified' # EDIT THESE FOR YOUR APPLICATION

if (col_a != 'no column specified') or (col_b != 'no column specified'):

    unique_THINGs = []
    this_row_THING = []
    temp_df = pandas.DataFrame()

    complete_dataframe.sort_values(by = [col_a, col_b], inplace = True)

    print("\nCreating files for individual THINGs by unique column values in column {} and column {}...\n".format(col_a, col_b))

    print("Creating files for:\n")
    print("{a:^22}|{b:^22}".format(a = col_a, b = col_b))
    print("---------------------------------------------")

    for a, b in zip(complete_dataframe[col_a], complete_dataframe[col_b]):

        this_row_THING = [a, b]

        if this_row_THING not in unique_THINGs:

            unique_THINGs.append(this_row_THING)

            print("|{a:^21}|{b:^21}|".format(a = this_row_THING[0], b = this_row_THING[1]))

            temp_df = complete_dataframe[complete_dataframe[col_a] == this_row_THING[0]]
            temp_df = temp_df[temp_df[col_b] == this_row_THING[1]]

            temp_df.dropna(how = 'all', axis = 1, inplace = True)

            temp_df.to_csv(".\\output_data\\{a}_{b}.csv".format(a=this_row_THING[0], b=this_row_THING[1]))

    print("---------------------------------------------")

else:

    print("\nColumns not specified, so no extra files will be created.")

print("\nData processing complete!\n")
