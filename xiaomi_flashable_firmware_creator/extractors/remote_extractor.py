from remotezip import RemoteZip
from requests import head

from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class RemoteExtractor(BaseExtractor):
    zip_url: str
    zip_file: RemoteZip

    def __init__(self, _extract_mode: str, zip_url: str, out_dir: str = ''):
        self.zip_url = zip_url
        super().__init__(_extract_mode, out_dir)

        if not head(zip_url).ok:
            raise FileNotFoundError(f"Zip file {self.zip_url} does not exist.")

        self.zip_file = RemoteZip(self.zip_url)
        self.files = self.zip_file.namelist()

        if self.is_valid_firmware_zip():
            self.get_fw_type()
        else:
            raise RuntimeError(f"{self.zip_file} is not a valid ROM zip file. Exiting..")

    def get_zip_name(self):
        return self.zip_url.split('/')[-1]
