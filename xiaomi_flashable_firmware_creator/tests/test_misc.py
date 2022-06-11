"""
Xiaomi Flashable Firmware Creator Miscellaneous tests.
"""

import unittest
from pathlib import Path

from xiaomi_flashable_firmware_creator.helpers.misc import extract_codename


class TestMisc(unittest.TestCase):
    """
    Testing misc utilities class

    This test class is used to test misc utilities functions.
    """

    def setUp(self):
        """
        Setting up the class attributes.

        :return:
        """
        self.work_dir = Path(__file__).parent
        self.files = self.work_dir.glob("files/updater-scripts/*")

    def test_extract_codename(self):
        """
        Test extracting the codename from a set of files.

        :return:
        """
        for file in self.files:
            updater_script = file.read_text()
            codename = extract_codename(updater_script)
            self.assertNotEqual("codename", codename)


if __name__ == "__main__":
    unittest.main()
