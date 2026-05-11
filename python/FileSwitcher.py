import vim
import os

def file_extension(path):
    return path.split('.')[-1]

def printError(errStr):
    cmd = f"echomsg \"{errStr}\""
    vim.command(cmd)

def find_files_in_tags(file):
    if os.path.exists('tags'):
        filename = os.path.basename(file)
        files = []
        try:
            with open('tags') as file:
                for line in file:
                    #print("line: ", end="")
                    if line.find(filename) != -1:
                        txt = line.split()
                        if os.path.basename(txt[1]) == filename:
                            #print(f"Append {txt[1]}")
                            files.append(txt[1])
        except (IOError, UnicodeDecodeError) as e:
            pass
        
        return set(files)
    else:
        printError("tags -file is not found")
        #print("tags -file is not found s")
    return set()

def open_file(path):
    cmd = 'edit ' + path
    vim.command(cmd)

def get_other_file(filename):
    if file_extension(filename) == 'cpp':
        return filename[0:-3] + 'hpp'
    elif file_extension(filename) == 'hpp': 
        return filename[0:-3] + 'cpp'
    elif file_extension(filename) == 'c': 
        return filename[0:-1] + 'h'
    elif file_extension(filename) == 'h': 
        return filename[0:-1] + 'c'
    raise NameError

# def switch_file():
#     try:
#         other_file = get_other_file(vim.current.buffer.name)
#         if os.path.exists(other_file):
#             open_file(other_file)
#         else:
#             files = find_files_in_tags(other_file)
#             if 0 < len(files):
#                 open_file(list(files)[0])
#             else:
#                 errStr =  f"\"The file: {filename} is not found from tags\""
#                 errStrCmd = 'echomsg ' + errStr 
#                 vim.command(errStrCmd)
#                 print("The file: " + filename + " is not found from tags")
#     except NameError:
#         print(f"Incompatible file: {vim.current.buffer.name}")

def get_files():
    try:
        other_file = get_other_file(vim.current.buffer.name)
        if os.path.exists(other_file):
            #print(other_file)
            #vim.command("g:files = '%s'"% other_file)
            #vim.command("let g:files = 'Foo_bar.cpp'")
            return [other_file]
        else:
            files = find_files_in_tags(other_file)
            lfiles = list(files)
            return lfiles
    except NameError:
        print(f"Incompatible file: {vim.current.buffer.name}")
    return []
