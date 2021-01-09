from typing import List, Union
from zipfile import ZipFile

from remotezip import RemoteZip


class BaseHandler:
    extractor: Union[ZipFile, RemoteZip]

    def __init__(self, zip_file_path, tmp_dir, extractor):
        self.zip_file_path = zip_file_path
        self._tmp_dir = tmp_dir
        self.extractor = extractor

    def extract(self, files_to_extract: List[str]):
        self.extractor.extractall(path=self._tmp_dir, members=files_to_extract)
