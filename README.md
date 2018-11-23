## Xiaomi Flashable Firmware Creator (Py version)
Create flashable firmware zip from MIUI Recovery ROMS!

[![Build Status](https://travis-ci.org/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator.svg?branch=py)](https://travis-ci.org/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator)

[![GitHub release](https://img.shields.io/github/release/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator.svg)](https://github.com/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/releases/)
[![Download](https://img.shields.io/github/downloads/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/total.svg)](https://github.com/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/releases/latest)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Xiaomi Flashable Firmware Creator is a script which generates flashable firmware-update packages, extracted from official MIUI ROMS.

It supports creating untouched firmware, non-arb firmware, and firmware-less ROMs.

### Usage:

- Creating normal (untouched) firmware:
```
python3 create_flashable_firmware.py -F [MIUI ZIP]
```
- Creating non-arb firmware (without anti-rollback):
```
python3 create_flashable_firmware.py -N [MIUI ZIP]
```
- Creating firmware-less ROM (stock untouched ROM with just firmware removed):
```
python3 create_flashable_firmware.py -L [MIUI ZIP]
```

### Using binary files:

If you want to use binary executable file for Windows and Linux check [releases](https://github.com/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/releases)! It's compiled with [pyinstaller](https://www.pyinstaller.org/).

Note that builds which automatically generated using travis-ci doesn't have a tag. If you prefer to go for stable release get the latest tagged one.
