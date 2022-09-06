import os

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