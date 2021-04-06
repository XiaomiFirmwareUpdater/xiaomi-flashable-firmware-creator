from pathlib import Path
from typing import List

# from google.protobuf.pyext._message import RepeatedCompositeContainer

from xiaomi_flashable_firmware_creator.extractors.handlers.base_handler import BaseHandler
from xiaomi_flashable_firmware_creator.extractors.ota_payload_extractor.extract_android_ota_payload \
    import Payload, parse_payload


class AndroidOneZip(BaseHandler):
    payload: Payload

    # partitions: Dict[str, RepeatedCompositeContainer]

    def __init__(self, zip_file_path, tmp_dir, extractor):
        super().__init__(zip_file_path, tmp_dir, extractor)
        self.payload_file = None
        self.all_partitions = set()
        self.files = []

    def prepare(self) -> List[str]:
        """
        Extract payload from zip in order to get partition names
        :return: a list of partition names strings
        """
        self.payload_file = open(self.extractor.extract('payload.bin', self._tmp_dir), 'rb')
        self.payload = Payload(self.payload_file)
        self.payload.Init()
        self.partitions = {i.partition_name: i for i in self.payload.manifest.partitions}
        self.all_partitions = set(self.partitions.keys())
        self.files = sorted([f"firmware-update/{i}.img" for i in self.all_partitions])
        return self.files

    def extract(self, files_to_extract: List[str]):
        """
        Extract partitions from payload file
        :param files_to_extract: a list of files to extract
        :return:
        """
        Path(self._tmp_dir / 'payload.bin').unlink()
        Path(self._tmp_dir / 'firmware-update').mkdir(parents=True, exist_ok=True)
        files_to_extract: set = set(self.files).intersection(set(files_to_extract))
        for file in files_to_extract:
            # partition: RepeatedCompositeContainer = self.partitions.get(file.split('/')[-1].split('.')[0])
            partition = self.partitions.get(file.split('/')[-1].split('.')[0])
            with open(Path(self._tmp_dir / f"firmware-update/{partition.partition_name}.img"), 'wb') as out_f:
                parse_payload(self.payload, partition, out_f)
        self.payload_file.close()
