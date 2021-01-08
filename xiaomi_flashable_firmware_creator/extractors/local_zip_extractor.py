"""Local Zip Extractor is a concrete class that implements BaseExtractor methods \
that deals with local zip files using zipfile standard library."""

from pathlib import Path
from typing import Union, List
from zipfile import ZipFile

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor
from xiaomi_flashable_firmware_creator.extractors.handlers.android_one_zip import AndroidOneZip
from xiaomi_flashable_firmware_creator.extractors.handlers.base_handler import BaseHandler
from xiaomi_flashable_firmware_creator.extractors.handlers.standard_zip import StandardZip


class LocalZipExtractor(BaseExtractor):
    """LocalZipExtractor provides methods for dealing with local zip files."""

    zip_file_path: Union[Path, str]
    zip_file: Union[str, Path]
    handler: BaseHandler

    def __init__(self, zip_file, tmp_dir):
        """
        Initialize LocalZipExtractor.

        :param zip_file: a path object or a string to a zip that contains a full recovery ROM.
        :param tmp_dir: output directory to place the extracted zip in.
        """
        self.zip_file_path = Path(zip_file) if isinstance(zip_file, str) else zip_file
        super().__init__(tmp_dir)
        with ZipFile(self.zip_file_path, 'r') as file:
            self.handler = AndroidOneZip(self.zip_file_path, tmp_dir) \
                if "payload.bin" in str(file.namelist()) else StandardZip(self.zip_file_path, tmp_dir)

    def exists(self) -> bool:
        """
        Check if the local zip file exists.

        :return: True if zip file exists, False otherwise.
        """
        return self.handler.exists()

    def open(self):
        """
        Open a local zip to use afterwards.

        :return:
        """
        self.file = self.handler.open()

    def get_files_list(self):
        """
        Get contents of the local zip file as list and store it in files attribute.

        :return:
        """
        self.files = self.handler.get_files_list()

    def get_file_name(self):
        """
        Get input zip file name and return it as a string.

        :return: a string of the input zip file name.
        """
        return self.handler.get_file_name()

    def prepare(self):
        if isinstance(self.handler, AndroidOneZip):
            self.files = self.handler.prepare()

    def extract(self, files_to_extract: List[str]):
        """
        Extract a list of files from the zip file

        :param files_to_extract: a list of files to extract
        :return:
        """
        self.handler.extract(files_to_extract)
