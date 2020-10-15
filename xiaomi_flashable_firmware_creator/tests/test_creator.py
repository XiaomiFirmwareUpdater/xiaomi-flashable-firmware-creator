import unittest
from pathlib import Path
from shutil import rmtree

from xiaomi_flashable_firmware_creator.extractors.local_extractor import LocalExtractor


class TestCreator(unittest.TestCase):
    def setUp(self):
        self.work_dir = Path(__file__).parent
        self.out_dir = self.work_dir / 'out'
        self.files = self.work_dir.glob('files/*/*.zip')

    @staticmethod
    def run_extractor(extractor):
        print(f"Unzipping MIUI... ({extractor.zip_type.name}) device")
        extractor.extract()
        print("Generating updater-script..")
        extractor.generate_updater_script()
        print("Creating new zip file..")
        extractor.make_zip()
        extractor.cleanup()
        extractor.close()

    def test_firmware(self):
        for file in self.files:
            extractor = LocalExtractor('firmware', str(file.absolute()), self.out_dir)
            print(f"Testing {file.name}")
            self.run_extractor(extractor)

    def tearDown(self):
        rmtree(self.out_dir)


if __name__ == '__main__':
    unittest.main()
