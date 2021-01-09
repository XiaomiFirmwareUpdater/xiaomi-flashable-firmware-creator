from xiaomi_flashable_firmware_creator.extractors.handlers.base_handler import BaseHandler


class StandardZip(BaseHandler):
    def __init__(self, zip_file_path, tmp_dir, extractor):
        super().__init__(zip_file_path, tmp_dir, extractor)
