vim9script

var plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('plugin_root_dir')
#python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, plugin_root_dir)
import FileSwitcher as fs
EOF

def g:CallFileSwitcher(): void
    py3 fs.switch_file()
enddef

nnoremap <leader>q :call CallFileSwitcher()<CR>
