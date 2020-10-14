## Xiaomi Flashable Firmware Creator
Create flashable firmware zip from MIUI Recovery ROMs!

[![Crowdin](https://badges.crowdin.net/mi-flashable-firmware-creator/localized.svg)](https://crowdin.com/project/mi-flashable-firmware-creator)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Xiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI ROMS.

It supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs.

### CLI Usage:

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
- Creating firmware + vendor flashable zip:
```
python3 create_flashable_firmware.py -V [MIUI ZIP]
```
