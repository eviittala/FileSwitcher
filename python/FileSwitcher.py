import vim
import os

def file_extension(path):
    return path.split('.')[-1]

def print_error(errStr):
    cmd = f"echomsg \"{errStr}\""
    vim.command(cmd)

def find_files_in_tags(file):
    if os.path.exists('tags'):
        filename = os.path.basename(file)
        files = set([])
        try:
            with open('tags') as file:
                for line in file:
                    if line.find(filename) != -1:
                        txt = line.split()
                        if os.path.basename(txt[1]) == filename:
                            files.add(txt[1])
        except (IOError, UnicodeDecodeError) as e:
            pass
        
        return list(files)
    else:
        print_error("tags -file is not found")
    return list()

def open_file(path):
    cmd = 'edit ' + path
    vim.command(cmd)

def get_other_file(file):
    if file_extension(file) == 'cpp':
        return file[0:-3] + 'hpp'
    elif file_extension(file) == 'hpp': 
        return file[0:-3] + 'cpp'
    elif file_extension(file) == 'c': 
        return file[0:-1] + 'h'
    elif file_extension(file) == 'h': 
        return file[0:-1] + 'c'
    return None

def get_current_buffer_name():
    return vim.current.buffer.name

def get_files():
    current_buffer_name = get_current_buffer_name()
    other_file = get_other_file(current_buffer_name)
    if os.path.exists(other_file):
        return [other_file]
    else:
        return find_files_in_tags(other_file)
    return []
