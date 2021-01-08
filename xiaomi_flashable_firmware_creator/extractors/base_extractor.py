"""
BaseExtractor is the abstract base class for zip extractors classes.

It defines some basic stuff like checking if zip exists, opening the zip,
 getting its contents, extracting a list of files from it, and closing the zip file.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union
from zipfile import ZipFile

from remotezip import RemoteZip


class BaseExtractor(ABC):
    """BaseExtractor provides abstract methods for dealing with zip files."""

    file: Union[ZipFile, RemoteZip]
    files: List[str]
    _out_dir: Path

    def __init__(self, _out_dir):
        """
        Initialize BaseExtractor class.

        :param _out_dir: output directory to place the extracted zip in.
        """
        self._out_dir = _out_dir
        self.files = []

    @abstractmethod
    def exists(self):
        """
        Check if the zip file exists.

        :return: should return True if file exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def open(self):
        """
        Open a remote zip to use afterwards.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_files_list(self):
        """
        Get contents of the remote zip file as list and store it in files attribute.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def extract(self, files_to_extract: List[str]):
        raise NotImplementedError

    # def extract(self, files_to_extract: List[str]):
    #     """
    #     Extract a list of files from the zip file into an output directory.
    #
    #     :param files_to_extract: a list of files to extract
    #     :return:
    #     """
    #     self.file.extractall(path=self._out_dir, members=files_to_extract)

    def close(self):
        """
        Close the zip file.

        :return:
        """
        self.file.close()

    @abstractmethod
    def get_file_name(self) -> str:
        """
        Get input zip file name and return it as a string.

        :return: a string of the input zip file name.
        """
        raise NotImplementedError
