from pathlib import Path
from typing import Union
from zipfile import ZipFile

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class LocalZipExtractor(BaseExtractor):
    zip_file_path: Union[Path, str]
    zip_file: ZipFile

    def __init__(self, zip_file: Union[str, Path], out_dir):
        self.zip_file_path = Path(zip_file) if isinstance(zip_file, str) else zip_file
        super().__init__(out_dir)

    def exists(self):
        return self.zip_file_path.exists()

    def open(self):
        self.file = ZipFile(self.zip_file_path, 'r')

    def get_files_list(self):
        self.files = self.file.namelist()

    def get_file_name(self):
        return self.zip_file_path.name
