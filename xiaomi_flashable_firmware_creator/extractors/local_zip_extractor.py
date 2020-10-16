"""Local Zip Extractor is a concrete class that implements BaseExtractor methods \
that deals with local zip files using zipfile standard library."""

from pathlib import Path
from typing import Union
from zipfile import ZipFile

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class LocalZipExtractor(BaseExtractor):
    """LocalZipExtractor provides methods for dealing with local zip files."""

    zip_file_path: Union[Path, str]
    zip_file: ZipFile

    def __init__(self, zip_file: Union[str, Path], out_dir):
        """
        Initialize LocalZipExtractor.

        :param zip_file: a path object or a string to a zip that contains a full recovery ROM.
        :param out_dir: output directory to place the extracted zip in.
        """
        self.zip_file_path = Path(zip_file) if isinstance(
            zip_file, str) else zip_file
        super().__init__(out_dir)

    def exists(self):
        """
        Check if the local zip file exists.

        :return: True if zip file exists, False otherwise.
        """
        return self.zip_file_path.exists()

    def open(self):
        """
        Open a local zip to use afterwards.

        :return:
        """
        self.file = ZipFile(self.zip_file_path, 'r')

    def get_files_list(self):
        """
        Get contents of the local zip file as list and store it in files attribute.

        :return:
        """
        self.files = self.file.namelist()

    def get_file_name(self):
        """
        Get input zip file name and return it as a string.

        :return: a string of the input zip file name.
        """
        return self.zip_file_path.name
