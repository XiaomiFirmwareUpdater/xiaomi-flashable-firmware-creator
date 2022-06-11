"""Xiaomi Flashable Firmware Creator unittest module."""

import unittest
from pathlib import Path
from shutil import rmtree

from xiaomi_flashable_firmware_creator.xiaomi_flashable_firmware_creator import (
    FlashableFirmwareCreator,
)


class TestCreator(unittest.TestCase):
    """Xiaomi Flashable Firmware Creator testing class"""

    def setUp(self):
        """
        set up work and output directories and the list of files to work with.

        :return:
        """
        self.work_dir = Path(__file__).parent
        self.out_dir = self.work_dir / "out"
        self.files = self.work_dir.glob("files/*/*.zip")

    @staticmethod
    def run_extractor(firmware_creator):
        """
        Run firmware_creator object auto method.

        :param firmware_creator: FlashableFirmwareCreator object
        :return:
        """
        print("Unzipping MIUI ROM...")
        firmware_creator.auto()

    def test_firmware(self):
        """
        Test firmware generation

        :return:
        """
        for file in self.files:
            firmware_creator = FlashableFirmwareCreator(
                str(file.absolute()), "firmware", self.out_dir
            )
            print(f"Testing {file.name}")
            self.run_extractor(firmware_creator)

    def test_firmwareless(self):
        """
        Test firmware-less ROM generation

        :return:
        """
        for file in self.files:
            firmware_creator = FlashableFirmwareCreator(
                str(file.absolute()), "firmwareless", self.out_dir
            )
            print(f"Testing {file.name}")
            try:
                self.run_extractor(firmware_creator)
            except RuntimeError as err:
                if str(err) != "Nothing found to extract!":
                    raise err

    def test_nonarb(self):
        """
        Test non-ARB firmware generation

        :return:
        """
        for file in self.files:
            firmware_creator = FlashableFirmwareCreator(
                str(file.absolute()), "nonarb", self.out_dir
            )
            print(f"Testing {file.name}")
            try:
                self.run_extractor(firmware_creator)
            except RuntimeError as err:
                if str(err) != "Nothing found to extract!":
                    raise err

    def test_vendor(self):
        """
        Test firmware+vendor generation

        :return:
        """
        for file in self.files:
            firmware_creator = FlashableFirmwareCreator(
                str(file.absolute()), "vendor", self.out_dir
            )
            print(f"Testing {file.name}")
            self.run_extractor(firmware_creator)

    def tearDown(self):
        """
        Remove output directory after finishing tests

        :return:
        """
        rmtree(self.out_dir)


if __name__ == "__main__":
    unittest.main()
