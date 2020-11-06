"""Miscellaneous functions used by the tool."""
import re


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
