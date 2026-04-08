import vim
import os

def exists(file):
    return os.path.exists(file)

def file_extension(path):
    return path.split('.')[-1]

def find_files_in_tags(file):
    if exists('tags'):
        filename = os.path.basename(file)
        files = []
        try:
            with open('tags') as file:
                for line in file:
                    #print("line: ", end="")
                    if line.find(filename) != -1:
                        txt = line.split()
                        files.append(txt[1])
                        break
                        #print(txt)
        except (IOError, UnicodeDecodeError) as e:
            pass
        
        return set(files)
    else:
        print("tags -file is not found")
    return []

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

if __name__ == "__main__":
    try:
        other_file = get_other_file(vim.current.buffer.name)
        if exists(other):
            open_file(other_file)
        else:
            files = find_files_in_tags(other_file)
            if 0 < len(files):
                open_file(list(files)[0])
            else:
                print("The file: " + filename + " is not found from tags")
    except NameError:
        print(f"Incompatible file: {vim.current.buffer.name}")
