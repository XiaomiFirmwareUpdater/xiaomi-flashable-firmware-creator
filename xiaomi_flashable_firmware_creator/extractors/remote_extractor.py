from xiaomi_flashable_firmware_creator.extractors.base_extractor import BaseExtractor


class RemoteExtractor(BaseExtractor):
    def __init__(self, _extract_mode: str, zip_url: str):
        self.zip_url = zip_url
        super().__init__(_extract_mode)

    def is_valid_firmware_zip(self):
        pass

    def get_fw_type(self):
        pass

    def extract(self):
        pass

    def close(self):
        pass

    def get_zip_name(self):
        pass
