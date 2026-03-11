import unittest
import importlib
import subprocess

# Library we want to unit test
list_files_in_space=importlib.import_module("list-files-in-space")

class TestListFilesInSpace(unittest.TestCase):
    
    # This test shows no success from failed file 
    def test_matches_extension(self):
        self.assertEqual(list_files_in_space.matches_extension(".jpg,.jpeg,.JPG", "file.jpg"), True)
        self.assertEqual(list_files_in_space.matches_extension(".jpg,.jpeg,.JPG", "file.JPEG"), False)
        self.assertEqual(list_files_in_space.matches_extension(".jpg,.jpeg,.JPG", "file.JPG"), True)
        self.assertEqual(list_files_in_space.matches_extension(".jpg,.jpeg,.JPG", "file.png"), False)
        self.assertEqual(list_files_in_space.matches_extension("", "file.png"), True)
        self.assertEqual(list_files_in_space.matches_extension(".jpg,.jpeg,.JPG", "my.cool.file.jpeg"), True)
        

if __name__ == '__main__':
    unittest.main()

