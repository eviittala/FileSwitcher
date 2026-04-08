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

    #TODO Eero: finalize this
    def test_find_files_in_tags(self):
        self.assertEqual([], fs.find_files_in_tags('Foo.cpp'))

    @patch('vim.command')
    def test_open_file(self, mock_method):
        fs.open_file('stub/foo.cpp')
        mock_method.assert_called_with('edit stub/foo.cpp')

    def test_get_other_file(self):
        self.assertEqual('Foo.hpp', fs.get_other_file('Foo.cpp'))
        self.assertEqual('Foo.cpp', fs.get_other_file('Foo.hpp'))
        self.assertEqual('Foo.h', fs.get_other_file('Foo.c'))
        self.assertEqual('Foo.c', fs.get_other_file('Foo.h'))
        self.assertEqual('/tmp/bar/Foo.h', fs.get_other_file('/tmp/bar/Foo.c'))
        self.assertEqual('/tmp/bar/Foo.hpp', fs.get_other_file('/tmp/bar/Foo.cpp'))
        with self.assertRaises(NameError):
            fs.get_other_file('/tmp/bar/Foo.py')

unittest.main()
