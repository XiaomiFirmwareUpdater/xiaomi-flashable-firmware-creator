## Xiaomi Flashable Firmware Creator
Create flashable firmware zip from MIUI Recovery ROMs!

[![PyPI version](https://badge.fury.io/py/xiaomi-flashable-firmware-creator.svg)](https://pypi.org/project/xiaomi-flashable-firmware-creator/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-3776AB?style=flat&labelColor=3776AB&logo=python&logoColor=white&link=https://www.python.org/)](https://www.python.org/)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](#) <br />
[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat&labelColor=00457C&logo=PayPal&logoColor=white&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat&labelColor=F96854&logo=Patreon&logoColor=white&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat&labelColor=F6C915&logo=Liberapay&logoColor=white&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)


Xiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI ROMS.

It supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs.

### CLI Usage:

- Creating normal (untouched) firmware:
```
python3 -m xiaomi_flashable_firmware_creator -F [MIUI ZIP]
```
- Creating non-arb firmware (without anti-rollback):
```
python3 -m xiaomi_flashable_firmware_creator -N [MIUI ZIP]
```
- Creating firmware-less ROM (stock untouched ROM with just firmware removed):
```
python3 -m xiaomi_flashable_firmware_creator -L [MIUI ZIP]
```
- Creating firmware + vendor flashable zip:
```
python3 -m xiaomi_flashable_firmware_creator -V [MIUI ZIP]
```
