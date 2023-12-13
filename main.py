import os, pandas

print("\nLooking for files...\n")

# returns a list of relative paths to all csv files in the given directory
def checkDirForCSV(dir_name = "", indent = 0):
    print("\t"*indent + "Files found in \"" + dir_name + "\" folder:")
    indent = indent + 1
    files = []
    for entry in os.listdir(dir_name):
        if ".csv" in entry: # for a csv file
            print("\t"*indent + dir_name + "\\" + entry)
            files.append(dir_name + "\\" + entry)
        elif "." not in entry: # for a subdirectory
            files.extend(checkDirForCSV(dir_name + "\\" + entry, indent))
    files.sort()
    return files

files = checkDirForCSV(".\\") # check for csv files

print("\nCombining files...\n")

complete_dataframe = pandas.DataFrame()
for file in files:
    print("Adding file \"" + file + "\"...")
    complete_dataframe = pandas.concat([complete_dataframe, pandas.read_csv(file, dtype='unicode')]).drop_duplicates()
complete_dataframe.sort_values('time')

print("\nfixing \"NaN\" values and removing empty columns")

complete_dataframe.replace("", float("NaN"), inplace=True)
complete_dataframe.dropna(how = 'all', axis = 1, inplace=True)

print("\nCreating file containing combined data")

complete_dataframe.to_csv(".\\0-data_processed.csv")

"""
print("\nCreating files for individual devices...\n")

unique_devices = []
this_row_device = []
temp_df = pandas.DataFrame()

print("Creating files for the following devices:\n")
print("{m:^19}|{i:^19}".format(m="model name", i="device id"))
print("---------------------------------------")

for model, id in zip(complete_dataframe['model'], complete_dataframe['id']):

    this_row_device = [model, id]

    if this_row_device not in unique_devices:

        unique_devices.append(this_row_device)

        print("|{model:^18}|{id:^18}|".format(model=this_row_device[0], id=this_row_device[1]))

        temp_df = complete_dataframe[complete_dataframe['id'] == this_row_device[1]]
        temp_df = temp_df[temp_df['model'] == this_row_device[0]]

        temp_df.dropna(how = 'all', axis = 1, inplace = True)

        temp_df.to_csv(".\\data_processed\\{model}_{id}.csv".format(model=this_row_device[0], id=this_row_device[1]))

print("---------------------------------------")
"""

print("\nData processing complete\n")
