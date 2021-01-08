#!/usr/bin/env python3
"""Xiaomi Flashable Firmware Creator cli module."""

from argparse import ArgumentParser

from xiaomi_flashable_firmware_creator.firmware_creator import FlashableFirmwareCreator


def arg_parse() -> (str, str, str):
    """
    Parse command-line arguments.

    This function parse command-line arguments and return
     the required parameters to be used in FlashableFirmwareCreator class constructor.

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
    """Xiaomi Flashable Firmware Creator main module."""
    zip_, process, output = arg_parse()
    firmware_creator = FlashableFirmwareCreator(zip_, process, output)
    print("Unzipping MIUI ROM...")
    new_zip = firmware_creator.auto()
    print(f"All done! Output file is {new_zip}")
