"""Local Zip Extractor is a concrete class that implements BaseExtractor methods \
that deals with local zip files using zipfile standard library."""

from pathlib import Path
from typing import Union, List
from zipfile import ZipFile

from remotezip import RemoteZip
from requests import head

from xiaomi_flashable_firmware_creator.extractors.handlers.android_one_zip import AndroidOneZip
from xiaomi_flashable_firmware_creator.extractors.handlers.standard_zip import StandardZip


class ZipExtractor:
    """ZipExtractor provides methods for dealing with local and remote zip files."""

    zip_file_path: Union[Path, str]
    zip_file: str
    zip_url: str
    handler: Union[StandardZip, AndroidOneZip]

    def __init__(self, zip_file, tmp_dir):
        """
        Initialize LocalZipExtractor.

        :param zip_file: a path object or a string to a zip that contains a full recovery ROM.
        :param tmp_dir: output directory to place the extracted zip in.
        """
        self.zip_url = zip_file if "http" in zip_file or "ota.d.miui.com" in zip_file else ""
        self.zip_file_path = Path(zip_file) if not self.zip_url and isinstance(zip_file, str) else ""
        self.files = []
        self._extractor = RemoteZip(self.zip_url) if self.zip_url else ZipFile(self.zip_file_path)
        self.handler = AndroidOneZip(self.zip_file_path, tmp_dir, self._extractor) \
            if "payload.bin" in str(self._extractor.namelist()) \
            else StandardZip(self.zip_file_path, tmp_dir, self._extractor)

    def exists(self) -> bool:
        """
        Check if the local zip file exists.

        :return: True if zip file exists, False otherwise.
        """
        return self.zip_file_path.exists() if self.zip_file_path else head(self.zip_url).ok

    def get_files_list(self):
        """
        Get contents of the local zip file as list and store it in files attribute.

        :return:
        """
        self.files = self._extractor.namelist()

    def get_file_name(self) -> str:
        """
        Get input zip file name and return it as a string.

        :return: a string of the input zip file name.
        """
        return self.zip_file_path.name if self.zip_file_path else self.zip_url.split('/')[-1]

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

    def close(self):
        """
        Close the zip file.

        :return:
        """
        self._extractor.close()
