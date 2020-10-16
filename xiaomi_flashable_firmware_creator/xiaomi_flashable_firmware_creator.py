#!/usr/bin/env python3
"""Xiaomi Flashable Firmware Creator"""

from argparse import ArgumentParser

from xiaomi_flashable_firmware_creator.firmware_creator import FlashableFirmwareCreator


def arg_parse() -> (str, str, str):
    """
    Parses command-line arguments
    :return: file, process, output dir
    """
    output = None
    parser = ArgumentParser(prog='python3 -m xiaomi_flashable_firmware_creator',
                            description='Xiaomi Flashable Firmware Creator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-F", "--firmware", help="Create normal Firmware zip")
    group.add_argument("-N", "--nonarb", help="Create non-ARB Firmware zip")
    group.add_argument("-L", "--firmwareless", help="Create Firmware-less zip")
    group.add_argument("-V", "--vendor", help="Create Firmware+Vendor zip")
    parser.add_argument('-o', "--output", help="Output directory")
    args = parser.parse_args()
    if args.output:
        output = args.output
        del args.output
    choose = {k: v for k, v in vars(args).items() if v is not None}
    process, zip_ = list(choose.items())[0]
    return zip_, process, output


def main():
    """
    Xiaomi Flashable Firmware Creator
    """
    zip_, process, output = arg_parse()
    firmware_creator = FlashableFirmwareCreator(zip_, process, output)
    print(f"Unzipping MIUI... ({firmware_creator.type.name}) device")
    firmware_creator.extract()
    print("Generating updater-script..")
    firmware_creator.generate_updater_script()
    print("Creating new zip file..")
    firmware_creator.make_zip()
    firmware_creator.cleanup()
    firmware_creator.close()
    print("All done!")
