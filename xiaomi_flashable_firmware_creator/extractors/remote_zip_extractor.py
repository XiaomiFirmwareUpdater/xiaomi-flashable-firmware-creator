from remotezip import RemoteZip
from requests import head

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class RemoteZipExtractor(BaseExtractor):
    zip_url: str
    zip_file: RemoteZip

    def __init__(self, zip_url: str, out_dir):
        self.zip_url = zip_url
        super().__init__(out_dir)

    def exists(self) -> bool:
        return head(self.zip_url).ok

    def open(self):
        self.file = RemoteZip(self.zip_url)

    def get_files_list(self):
        self.files = self.file.namelist()

    def get_file_name(self) -> str:
        return self.zip_url.split('/')[-1]
