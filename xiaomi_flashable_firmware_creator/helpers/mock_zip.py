"""Mock a zip file and create a placeholder files of its contents."""
from pathlib import Path
from shutil import make_archive, rmtree
from sys import argv
from typing import Union
from zipfile import ZipFile


def mock_zip(zip_file: str, out_dir: Union[str, Path]):
    """Create a mock zip of a given zip file.

    It iterates over the zip contents, creates the folders
    and creates a file that contains one byte of every file inside the zip
    :param out_dir: zip file to mock
    :param out_dir: out directory
    :type zip_file: str
    :type out_dir: str or Path
    """
    if isinstance(out_dir, str):
        out_dir = Path(out_dir) / 'mock_tmp'
    else:
        out_dir = out_dir / 'mock_tmp'
    out_dir = out_dir.absolute()
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_file = Path(zip_file)

    with ZipFile(zip_file, 'r') as zipfile:
        files = zipfile.namelist()
        for item in files:
            item_path = Path(out_dir / item)
            if item.endswith('/'):
                if not item_path.exists():
                    item_path.mkdir(parents=True, exist_ok=True)
            else:
                if not item_path.exists():
                    item_path.parent.mkdir(parents=True, exist_ok=True)
                if item.endswith("updater-script"):
                    zipfile.extract(item, out_dir)
                else:
                    with open(f"{out_dir}/{item}", 'wb') as out:
                        out.write(b'')

    mocked_zip = f"{out_dir.parent}/mocked_{zip_file.stem}"
    make_archive(mocked_zip, zip_file.suffix.split('.')[-1], out_dir)
    out = Path(f"{mocked_zip}.zip")
    if not out.exists():
        raise RuntimeError("Could not create mocked zip file!")
    rmtree(out_dir)


if __name__ == '__main__':
    mock_zip(argv[1], argv[2])
