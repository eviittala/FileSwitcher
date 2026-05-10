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
    #echomsg txt
    execute "edit " .. file
    files = []
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

def IsValidFile(file: string): bool
    var ext: string = expand('%:e')
    if ext =~ '\v(c|cpp|h|hpp)\c'
        return true
    endif
    return false
enddef

def g:CallFileSwitcher(): void
    var filename: string = expand('%')
    if IsValidFile(filename)
        files = py3eval("fs.get_files()")
        #echo files
        if 1 < len(files)
            files->popup_menu({ callback: 'SelectFile' })
            #var pos = getpos('.')
            #popup_menu(files, {
            #    \ callback: 'SelectFile',
            #    \ })
        elseif 0 < len(files)
            OpenFile(files[0])
        elseif 0 == len(files)
            echomsg "Cannot find switchable file for " .. filename
        endif
    else
        echomsg "Not valid file: " .. filename
    endif
enddef

nnoremap <leader>q :call CallFileSwitcher()<CR>
