import unittest
from pathlib import Path

from xiaomi_flashable_firmware_creator.helpers.misc import extract_codename


class TestMisc(unittest.TestCase):
    def setUp(self):
        self.work_dir = Path(__file__).parent
        self.files = self.work_dir.glob('files/updater-scripts/*')

    def test_extract_codename(self):
        for file in self.files:
            updater_script = file.read_text()
            codename = extract_codename(updater_script)
            self.assertNotEqual('codename', codename)


if __name__ == '__main__':
    unittest.main()
