from typing import List
from zipfile import ZipFile


class BaseHandler:
    file: ZipFile

    def __init__(self, zip_file_path, tmp_dir):
        self.zip_file_path = zip_file_path
        self._tmp_dir = tmp_dir

    def exists(self) -> bool:
        return self.zip_file_path.exists()

    def open(self) -> ZipFile:
        self.file = ZipFile(self.zip_file_path, 'r')
        return self.file

    def get_files_list(self) -> List[str]:
        return self.file.namelist()

    def extract(self, files_to_extract: List[str]):
        self.file.extractall(path=self._tmp_dir, members=files_to_extract)

    def get_file_name(self) -> str:
        return self.zip_file_path.name
