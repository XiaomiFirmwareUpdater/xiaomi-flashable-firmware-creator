#!/usr/bin/env python3.7
"""Xiaomi Flashable Firmware Creator"""

from argparse import ArgumentParser
from datetime import datetime
from distutils.dir_util import copy_tree
from glob import glob
from os import makedirs, rename, remove, path
from shutil import move, make_archive, rmtree
from socket import gethostname
from zipfile import ZipFile
from sys import exit as exit_
import re


def arg_parse():
    """
    Parses command-line arguments
    :return: rom, process
    """
    process = None
    rom = None
    switches = ArgumentParser(description='Xiaomi Flashable Firmware Creator', )
    group = switches.add_mutually_exclusive_group(required=True)
    group.add_argument("-F", "--firmware", help="Create normal Firmware zip")
    group.add_argument("-N", "--nonarb", help="Create non-ARB Firmware zip")
    group.add_argument("-L", "--firmwareless", help="Create Firmware-less zip")
    group.add_argument("-V", "--vendor", help="Create Firmware+Vendor zip")
    args = vars(switches.parse_args())
    firmware = args["firmware"]
    firmwareless = args["firmwareless"]
    nonarb = args["nonarb"]
    vendor = args["vendor"]
    if firmware is not None:
        process = "firmware"
        rom = firmware
    elif nonarb is not None:
        process = "nonarb"
        rom = nonarb
    elif firmwareless is not None:
        process = "firmwareless"
        rom = firmwareless
    elif vendor is not None:
        process = "vendor"
        rom = vendor
    return rom, process


def init():
    """Initial checks and housekeeping"""
    if path.exists('out'):
        rmtree('out')
    if path.exists('tmp'):
        rmtree('tmp')
    makedirs("tmp", exist_ok=True)
    makedirs("out", exist_ok=True)
    makedirs("out/META-INF/com/google/android", exist_ok=True)


def pre():
    """
    Sets today data and hostname
    :return: today, host
    """
    today = str(datetime.today()).split('.')[0]
    host = str(gethostname())
    return today, host


def check_firmware():
    """
    Checks firmware existence
    """
    if not path.exists('tmp/META-INF/com/google/android/update-binary') \
            or not path.exists('tmp/META-INF/com/google/android/updater-script'):
        print("This zip isn't a valid ROM!")
        rmtree("tmp")
        exit_(2)


def firmware_type(rom):
    """
    Checks firmware type
    :return fw_type
    """
    fw_type = None
    with ZipFile(rom, 'r') as zip_file:
        files = zip_file.namelist()
        if 'firmware-update' in str(files):
            fw_type = 'qcom'
        elif 'lk.img' in files or 'preloader.img' in str(files):
            fw_type = 'mtk'
    return fw_type


def firmware_extract(rom, process):
    """
    Extracts firmware from qcom device's ROM
    """
    if process == "firmware":
        with ZipFile(rom, 'r') as zip_file:
            files = [n for n in zip_file.namelist()
                     if n.startswith('firmware-update/') or n.startswith('META-INF/')]
            to_extract = [i for i in files if 'dtbo' not in i
                          and 'splash' not in i and 'logo' not in i and 'vbmeta' not in i]
            zip_file.extractall(path="tmp", members=to_extract)
    elif process == "nonarb":
        with ZipFile(rom, 'r') as zip_file:
            files = [n for n in zip_file.namelist()
                     if n.startswith('firmware-update/dspso.bin')
                     or n.startswith('firmware-update/BTFM.bin')
                     or n.startswith('firmware-update/NON-HLOS.bin')
                     or n.startswith('META-INF/')]
            zip_file.extractall(path="tmp", members=files)
    check_firmware()
    move('tmp/firmware-update/', 'out/firmware-update/')
    move('tmp/META-INF/com/google/android/update-binary', 'out/META-INF/com/google/android/')


def mtk_firmware_extract(rom):
    """
    Extracts firmware from mtk device's ROM
    """
    with ZipFile(rom, 'r') as zip_file:
        files = [n for n in zip_file.namelist() if 'system' not in n and 'vendor' not in n
                 and 'product' not in n and 'boot.img' not in n and 'file_contexts' not in n]
        zip_file.extractall(path="tmp", members=files)
    check_firmware()
    for file in glob('tmp/*'):
        if 'META-INF' not in file:
            move(file, f'out/{file.split("/")[-1]}')
    move('tmp/META-INF/com/google/android/update-binary', 'out/META-INF/com/google/android/')


def rom_extract(rom):
    """
    Extracts ROM without firmware for qcom device
    :return:
    """
    with ZipFile(rom, 'r') as zip_file:
        files = [n for n in zip_file.namelist()
                 if not n.startswith('firmware-update/')]
        zip_file.extractall(path="tmp", members=files)
    check_firmware()
    copy_tree('tmp/', 'out/')


def vendor_extract(rom):
    """
    Extracts vendor and firmware
    :return:
    """
    with ZipFile(rom, 'r') as zip_file:
        files = [n for n in zip_file.namelist()
                 if not n.startswith('system') and not n.startswith('vbmeta')]
        zip_file.extractall(path="tmp", members=files)
    check_firmware()
    copy_tree('tmp/', 'out/')
    remove("out/META-INF/com/google/android/updater-script")


def firmware_updater():
    """
    Generates updater-script for firmware zip
    """
    print("Generating updater-script..")
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/updater-script", "w", newline='\n') as out:
        out.writelines("show_progress(0.200000, 10);\n\n")
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing Normal firmware...");\n')
        out.writelines(line for line in i if "getprop" in line or "Target" in line
                       or "firmware-update" in line and "dtbo.img" not in line
                       and "vbmeta" not in line and "splash" not in line and "logo" not in line)
        out.writelines('\nshow_progress(0.100000, 2);\nset_progress(1.000000);\n')
    with open("out/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        correct = i.read().replace('/firmware/image/sec.dat', '/dev/block/bootdevice/by-name/sec') \
            .replace('/firmware/image/splash.img', '/dev/block/bootdevice/by-name/splash')
        out.write(correct)
    remove("out/updater-script")


def mtk_firmware_updater():
    """
    Generates updater-script for firmware zip (mtk)
    """
    print("Generating updater-script..")
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing Normal firmware...");\n')
        out.writelines(line for line in i.readlines() if "system" not in line
                       and "vendor" not in line and 'boot.img' not in line)


def nonarb_updater():
    """
    Generates updater-script for non-arb firmware zip
    """
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/updater-script", "w", newline='\n') as out:
        out.writelines("show_progress(0.200000, 10);\n\n")
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing non-ARB firmware...");\n')
        out.writelines(line for line in i if "getprop" in line or "Target" in line
                       or "modem" in line or "bluetooth" in line or "dsp" in line)
        out.writelines('\nshow_progress(0.100000, 2);\nset_progress(1.000000);\n')
    with open("out/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        correct = i.read().replace('/firmware/image/sec.dat', '/dev/block/bootdevice/by-name/sec') \
            .replace('/firmware/image/splash.img', '/dev/block/bootdevice/by-name/splash')
        out.write(correct)
    remove("out/updater-script")


def firmwareless_updater():
    """
    Generates updater-script for fw-less zip
    """
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        out.writelines("show_progress(0.200000, 10);\n\n")
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing firmware-less ROM...");\n')
        out.writelines(line for line in i if "getprop" in line or "Target" in line
                       or "boot.img" in line or "system" in line or "vendor" in line)
        out.writelines('\nshow_progress(0.100000, 2);\nset_progress(1.000000);\n')


def vendor_updater():
    """
    Generates updater-script for fw-vendor zip
    """
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/updater-script", "w", newline='\n') as out:
        out.writelines("show_progress(0.200000, 10);\n\n")
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing firmware+vendor...");\n')
        out.writelines(line for line in i if "getprop" in line or "Target" in line
                       or "firmware-update" in line
                       or "vendor" in line)
        out.writelines('\nshow_progress(0.100000, 2);\nset_progress(1.000000);\n')
    with open("out/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        correct = i.read().replace('/firmware/image/sec.dat', '/dev/block/bootdevice/by-name/sec') \
            .replace('/firmware/image/splash.img', '/dev/block/bootdevice/by-name/splash')
        out.write(correct)
    remove("out/updater-script")


def mtk_vendor_updater():
    """
    Generates updater-script for firmware+vendor zip (mtk)
    """
    today, host = pre()
    with open("tmp/META-INF/com/google/android/updater-script", 'r') as i, \
            open("out/META-INF/com/google/android/updater-script", "w", newline='\n') as out:
        out.writelines("# Generated by Xiaomi Flashable Firmware Creator\n"
                       + f"# {today} - {host}\n\n")
        out.writelines('ui_print("Flashing firmware+vendor...");\n')
        out.writelines(line for line in i.readlines() if "system" not in line
                       and 'boot.img' not in line)


def make_zip(rom, process):
    """
    Creates zip from extracted files
    """
    rom = path.basename(rom)
    with open("out/META-INF/com/google/android/updater-script", 'r') as i:
        updater_script = i.read()
    # codename = str(i.readlines()[7].split('/', 3)[2]).split(':', 1)[0].replace('_', '-')
    try:
        codename = re.findall(r'/.*:[0-9]', updater_script)[0].split('/')[-1].split(':')[0]
    except IndexError:
        try:
            codename = re.search(r'get_device_compatible\(\"([a-z]*)|\\\"([a-z]*)\\\"',
                                 updater_script).group(1)
        except Exception as err:
            print(f"Error: can't get this device codename ({err})\n")
            codename = "codename"
    if codename.find('_') > 1:
        codename = codename.replace('_', '-')
    print(f"Creating {process} zip from {rom} for {codename}")
    make_archive('firmware', 'zip', 'out/')
    if path.exists('firmware.zip'):
        if process == "firmware":
            rename('firmware.zip', f'fw_{codename}_{rom}')
        elif process == "nonarb":
            rename('firmware.zip', f'fw-non-arb_{codename}_{rom}')
        elif process == "firmwareless":
            rename('firmware.zip', f'fw-less_{codename}_{rom}')
        elif process == "vendor":
            rename('firmware.zip', f'fw-vendor_{codename}_{rom}')
        print("All done!")
        rmtree("tmp")
        rmtree('out')
    else:
        print("Failed!\n Check out folder!")


def main():
    """
    Xiaomi Flashable Firmware Creator
    """
    rom, process = arg_parse()
    init()
    fw_type = firmware_type(rom)
    if fw_type == 'qcom':
        if process == "firmware":
            print(f"Unzipping MIUI... ({fw_type}) device")
            firmware_extract(rom, process)
            firmware_updater()
        elif process == "nonarb":
            print("Unzipping MIUI..")
            firmware_extract(rom, process)
            print("Generating updater-script..")
            nonarb_updater()
        elif process == "firmwareless":
            print("Unzipping MIUI..")
            rom_extract(rom)
            print("Generating updater-script..")
            firmwareless_updater()
        elif process == "vendor":
            print("Unzipping MIUI..")
            vendor_extract(rom)
            print("Generating updater-script..")
            vendor_updater()
    elif fw_type == 'mtk':
        if process == "firmware":
            print(f"Unzipping MIUI... ({fw_type}) device")
            mtk_firmware_extract(rom)
            mtk_firmware_updater()
        elif process == "vendor":
            print("Unzipping MIUI..")
            vendor_extract(rom)
            print("Generating updater-script..")
            mtk_vendor_updater()
        else:
            print('Unsupported operation for MTK. Exiting!')
            exit_(3)
    else:
        print("I couldn't find firmware! Exiting.")
        exit_(4)
    make_zip(rom, process)


if __name__ == '__main__':
    main()
