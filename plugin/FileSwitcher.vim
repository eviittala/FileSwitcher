vim9script

def g:SayHello()
    echo 'Hello World'
enddef

command! Hello call SayHello()
nnoremap Q :Hello<CR>
