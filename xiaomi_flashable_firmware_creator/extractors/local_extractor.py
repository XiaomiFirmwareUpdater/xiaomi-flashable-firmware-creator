from pathlib import Path
from shutil import rmtree
from typing import Union
from zipfile import ZipFile

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class LocalExtractor(BaseExtractor):
    def __init__(self, _extract_mode: str, zip_file: Union[str, Path], out_dir=''):
        self.zip_file_path = Path(zip_file) if isinstance(zip_file, str) else zip_file

        super().__init__(_extract_mode, out_dir)

        if not self.zip_file_path.exists():
            raise FileNotFoundError(f"Zip file {self.zip_file_path.name} does not exist.")

        self.zip_file = ZipFile(self.zip_file_path, 'r')
        self.files = self.zip_file.namelist()

        if self.is_valid_firmware_zip():
            self.get_fw_type()
        else:
            rmtree(self._tmp_dir)
            raise RuntimeError(f"{self.zip_file} is not a valid ROM zip file. Exiting..")

    def is_valid_firmware_zip(self):
        return "META-INF/com/google/android/update-binary" in self.files \
               or "META-INF/com/google/android/updater-script" in self.files

    def extract(self):
        self.zip_file.extractall(path=self._tmp_dir, members=self.get_files_list())

    def close(self):
        self.zip_file.close()

    def get_zip_name(self):
        return self.zip_file_path.name
