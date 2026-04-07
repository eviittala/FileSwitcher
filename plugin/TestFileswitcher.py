import unittest
from unittest.mock import patch
import os
import sys
sys.path.append('.')
import Fileswitcher as fs

class Foo:
    name = 'Foo.cpp'

class TestFileswitcher(unittest.TestCase):

    def test_exists(self):
        with open('foo.cpp', 'w') as file:
            file.write('Hello World')
        self.assertTrue(fs.exists('foo.cpp'))
        os.remove('foo.cpp')
        self.assertFalse(fs.exists('foo.cpp'))

    def test_file_extension(self):
        self.assertEqual('cpp', fs.file_extension('foo.cpp'))
        self.assertEqual('hpp', fs.file_extension('foo.hpp'))

    @patch('vim.command')
    def test_open_file(self, mock_method):
        fs.open_file('stub/foo.cpp')
        mock_method.assert_called_with('edit stub/foo.cpp')

    #@patch('vim.current.buffer.name')
    def test_get_other_file(self):
        #mock_method.return_value = 'Foo.cpp'
        #self.assertEqual('Foo.hpp', fs.get_other_file())
        pass


unittest.main()
