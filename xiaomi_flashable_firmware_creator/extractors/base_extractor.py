from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union
from zipfile import ZipFile

from remotezip import RemoteZip


class BaseExtractor(ABC):
    file: Union[ZipFile, RemoteZip]
    files: List[str]
    _out_dir: Path

    def __init__(self, _out_dir):
        self._out_dir = _out_dir
        self.files = []

    @abstractmethod
    def exists(self):
        raise NotImplementedError

    @abstractmethod
    def open(self):
        raise NotImplementedError

    @abstractmethod
    def get_files_list(self):
        raise NotImplementedError

    def extract(self, files_to_extract: List[str]):
        self.file.extractall(path=self._out_dir, members=files_to_extract)

    def close(self):
        self.file.close()

    @abstractmethod
    def get_file_name(self):
        raise NotImplementedError
