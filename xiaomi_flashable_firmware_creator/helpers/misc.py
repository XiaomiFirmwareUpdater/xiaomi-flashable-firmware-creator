"""Miscellaneous functions used by the tool."""
import re
from string import Template


def extract_codename(updater_script) -> str:
    r"""Extract device codename form updater-script.

    Regex pattern explanation:
    - (?:/[\w\d_-]+/([\w\d]+):\d) matches codename in update fingerprint like
    Xiaomi/cmi_global/cmi:11/RKQ1.200710.002/V12.1.2.0.RJAMIXM:user/release-keys
    - (?:\(\"ro\.product\.device\"\) == \"([\w\d]+)\") matches codename
     in getprop("ro.product.device") statements
    - (?:get_device_compatible\(\"([\w\d]+)\"\)) matches get_device_compatible() statements
    :param updater_script: updater-script file as string
    :return: extracted codename if found or 'codename' if not found.
    """
    pattern = re.compile(r'(?:/[\w\d_-]+/([\w\d]+):\d)|'
                         r'(?:\(\"ro\.product\.device\"\) == \"([\w\d]+)\")|'
                         r'(?:get_device_compatible\(\"([\w\d]+)\"\))')
    match = pattern.search(updater_script)
    if match:
        codename = [i for i in match.groups() if i is not None]
        return codename[0]
    return 'codename'


def cleanup_codename(codename: str) -> str:
    """
    Remove region names from codename and android one's "SPROUT"
    :param codename: codename from miui zip
    :return: clean codename
    """
    if "SPROUT" in codename:
        codename = codename.replace("SPROUT", "")
    if "EEAGlobal" in codename:
        return codename.replace("EEAGlobal", "")
    if "IDGlobal" in codename:
        return codename.replace("IDGlobal", "")
    if "INGlobal" in codename:
        return codename.replace("INGlobal", "")
    if "RUGlobal" in codename:
        return codename.replace("RUGlobal", "")
    if "TRGlobal" in codename:
        return codename.replace("TRGlobal", "")
    if "TWGlobal" in codename:
        return codename.replace("TWGlobal", "")
    if "Global" in codename:
        return codename.replace("Global", "")
    return codename


class ScriptTemplate(Template):
    delimiter = "[-]"
