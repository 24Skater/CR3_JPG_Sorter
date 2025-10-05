import os
import shutil
import tempfile
from ImageSorterCore import move_to_type_folder, move_to_other_folder, is_image_file

def test_move_to_type_folder():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.JPG')
        with open(test_file, 'w') as f:
            f.write('dummy')
        ok, err = move_to_type_folder(test_file, tmpdir)
        assert ok, f"Failed to move: {err}"
        assert os.path.exists(os.path.join(tmpdir, 'JPG', 'test.JPG'))

def test_move_to_other_folder():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.xyz')
        with open(test_file, 'w') as f:
            f.write('dummy')
        ok, err = move_to_other_folder(test_file, tmpdir)
        assert ok, f"Failed to move: {err}"
        assert os.path.exists(os.path.join(tmpdir, 'Other', 'test.xyz'))

def test_is_image_file():
    assert is_image_file('foo.JPG')
    assert not is_image_file('foo.xyz')

if __name__ == '__main__':
    test_move_to_type_folder()
    test_move_to_other_folder()
    test_is_image_file()
    print('All tests passed!')
