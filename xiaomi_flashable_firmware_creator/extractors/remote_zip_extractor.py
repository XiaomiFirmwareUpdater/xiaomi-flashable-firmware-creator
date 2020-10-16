"""Remote Zip Extractor is a concrete class that implements BaseExtractor methods \
that deals with remote zip files using remotezip library."""

from remotezip import RemoteZip
from requests import head

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class RemoteZipExtractor(BaseExtractor):
    """RemoteZipExtractor provides methods for dealing with remote zip files."""

    zip_url: str
    zip_file: RemoteZip

    def __init__(self, zip_url: str, out_dir):
        """
        Initialize RemoteZipExtractor.

        :param zip_url: a direct url to a zip that contains a full recovery ROM.
        :param out_dir: output directory to place the extracted zip in.
        """
        self.zip_url = zip_url
        super().__init__(out_dir)

    def exists(self) -> bool:
        """
        Check if the remote file exists.

        :return: True if http code is 200 OK, False otherwise.
        """
        return head(self.zip_url).ok

    def open(self):
        """
        Open a remote zip to use afterwards.

        :return:
        """
        self.file = RemoteZip(self.zip_url)

    def get_files_list(self):
        """
        Get contents of the remote zip file as list and store it in files attribute.

        :return:
        """
        self.files = self.file.namelist()

    def get_file_name(self) -> str:
        """
        Get input zip url file name and return it as a string.

        :return: a string of the input zip url file name.
        """
        return self.zip_url.split('/')[-1]
