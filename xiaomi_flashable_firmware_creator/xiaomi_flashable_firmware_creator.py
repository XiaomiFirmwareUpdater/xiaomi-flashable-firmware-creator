#!/usr/bin/env python3
"""Xiaomi Flashable Firmware Creator"""

from argparse import ArgumentParser

from xiaomi_flashable_firmware_creator.extractors.local_extractor import LocalExtractor
from xiaomi_flashable_firmware_creator.extractors.remote_extractor import RemoteExtractor


def arg_parse() -> (str, str):
    """
    Parses command-line arguments
    :return: process, file
    """
    parser = ArgumentParser(prog='python3 -m xiaomi_flashable_firmware_creator',
                            description='Xiaomi Flashable Firmware Creator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-F", "--firmware", help="Create normal Firmware zip")
    group.add_argument("-N", "--nonarb", help="Create non-ARB Firmware zip")
    group.add_argument("-L", "--firmwareless", help="Create Firmware-less zip")
    group.add_argument("-V", "--vendor", help="Create Firmware+Vendor zip")
    args = parser.parse_args()
    choose = {k: v for k, v in vars(args).items() if v is not None}
    process, zip_ = list(choose.items())[0]
    return process, zip_


def main():
    """
    Xiaomi Flashable Firmware Creator
    """
    process, zip_ = arg_parse()
    extractor = RemoteExtractor(process, zip_) if "http" in zip_ else LocalExtractor(process, zip_)
    print(f"Unzipping MIUI... ({extractor.zip_type.name}) device")
    extractor.extract()
    print("Generating updater-script..")
    extractor.generate_updater_script()
    print("Creating new zip file..")
    extractor.make_zip()
    extractor.cleanup()
    extractor.close()
    print("All done!")
