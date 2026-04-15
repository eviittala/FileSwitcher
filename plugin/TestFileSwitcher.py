import unittest
from unittest.mock import patch
import os
import sys
sys.path.append('.')
import FileSwitcher as fs

# How to execute: py3f TestFileSwitcher.py

class TestFileSwitcher(unittest.TestCase):

    #def test_exists(self):
    #    with open('foo.cpp', 'w') as file:
    #        file.write('Hello World')
    #    self.assertTrue(fs.exists('foo.cpp'))
    #    os.remove('foo.cpp')
    #    self.assertFalse(fs.exists('foo.cpp'))
    def tearDown(self):
        if os.path.exists('tags'):
            os.remove('tags')

    def test_file_extension(self):
        self.assertEqual('cpp', fs.file_extension('foo.cpp'))
        self.assertEqual('hpp', fs.file_extension('foo.hpp'))

    def test_find_files_in_tags(self):
        self.assertEqual(set(), fs.find_files_in_tags('Foo.cpp'))
        self.assertTrue(0 == len(fs.find_files_in_tags('Foo.cpp')))

    def test_find_files_in_tags1(self):
        with open('tags', 'w') as file:
            file.write("Main software/bar/Foo.cpp class Foo")
        self.assertEqual({'software/bar/Foo.cpp'}, fs.find_files_in_tags('Foo.cpp'))

    def test_find_files_in_tags2(self):
        with open('tags', 'w') as file:
            file.write("Main    software/bar/TestFoo.cpp    class Foo\n")
            file.write("Main    software/bar/Foo.cpp    class Foo\n")
        self.assertEqual({'software/bar/Foo.cpp'}, fs.find_files_in_tags('software/foo/Foo.cpp'))

    def test_find_files_in_tags3(self):
        with open('tags', 'w') as file:
            file.write("Main    software/tmp/Foo.cpp    class Foo\n")
            file.write("Main    software/bar/TestFoo.cpp    class Foo\n")
            file.write("Main    software/bar/Foo.cpp    class Foo\n")
            file.write("Main    software/sys/Foo.cpp    class Foo\n")
        self.assertEqual({'software/tmp/Foo.cpp', 'software/bar/Foo.cpp', 'software/sys/Foo.cpp'}, fs.find_files_in_tags('software/foo/Foo.cpp'))

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
