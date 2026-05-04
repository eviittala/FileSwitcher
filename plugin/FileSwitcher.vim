vim9script

if !has("python3")
    echom "vim has to be compiled with +python3 to run this"
    finish
endif

if exists('fileSwitcherLoaded')
    finish
endif

var fileSwitcherLoaded = 1
var plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import FileSwitcher as fs
EOF

var files: list<string>

def OpenFile(file: string): void
    var txt: string = "Changing to " .. file
    echowindow txt
    execute "edit " .. file
enddef

def SelectFile(id: number, result: number): void
    echo result .. " " .. id
    OpenFile(files[result - 1])
enddef

def ShowDialog(file: string): void
    var txt: string = "Changing to " .. file
    popup_create(txt, {
        \ line: 1,
        \ col: 100,
        \ minwidth: 20,
        \ time: 3000,
        \ tabpage: -1,
        \ zindex: 300,
        \ drag: 1,
        \ highlight: 'WarningMsg',
        \ border: [],
        \ close: 'click',
        \ padding: [0, 1, 0, 1], } )
enddef


def g:CallFileSwitcher(): void
    var what: string = "My popup menu"
    #vim9cmd popup_notification("File changed",
    # \ { line: 15, col: 10, highlight: 'WildMenu', } )
    #call popup_menu(['red', 'green', 'blue'], {
    #    \ callback: 'SelectFile',
    #    \ })
    files = py3eval("fs.get_files()")
    echo files
    if 1 < len(files)
        popup_menu(files, {
            \ callback: 'SelectFile',
            \ })
    elseif 0 < len(files)
        OpenFile(files[0])
    endif
    #g:files = 'Foo.hpp'
    #echo g:files
    #echo files
    #ShowDialog(files[0])
enddef

nnoremap <leader>q :call CallFileSwitcher()<CR>
