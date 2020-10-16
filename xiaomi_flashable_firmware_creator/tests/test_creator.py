import unittest
from pathlib import Path
from shutil import rmtree

from xiaomi_flashable_firmware_creator.xiaomi_flashable_firmware_creator import FlashableFirmwareCreator


class TestCreator(unittest.TestCase):
    def setUp(self):
        self.work_dir = Path(__file__).parent
        self.out_dir = self.work_dir / 'out'
        self.files = self.work_dir.glob('files/*/*.zip')

    @staticmethod
    def run_extractor(firmware_creator):
        print(f"Unzipping MIUI... ({firmware_creator.zip_type.name}) device")
        firmware_creator.extract()
        firmware_creator.generate_updater_script()
        firmware_creator.make_zip()
        firmware_creator.cleanup()
        firmware_creator.close()

    def test_firmware(self):
        for file in self.files:
            firmware_creator = FlashableFirmwareCreator(str(file.absolute()), 'firmware', self.out_dir)
            print(f"Testing {file.name}")
            self.run_extractor(firmware_creator)

    def tearDown(self):
        rmtree(self.out_dir)


if __name__ == '__main__':
    unittest.main()
