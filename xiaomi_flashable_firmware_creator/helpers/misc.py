"""Miscellaneous functions used by the tool."""

from dataclasses import dataclass
import re
from pathlib import Path
from string import Template
from typing import Callable


PAYLOAD_CODENAME_PATTERNS = (
    (
        re.compile(
            r'miui_(?P<miui_name>[\w\d]+)_(?P<version>.*)_(?P<md5_part>[\w\d]+)_(?P<android>[\d.]+)\.zip'
        ),
        'miui_name',
    ),
    (
        re.compile(
            r'(?P<codename>[\w\d_]+)-ota_full-(?P<version>[\da-zA-Z.]+)-(?P<type>\w+)-'
            r'(?P<android>[\d.]+)-(?P<md5_part>[\w\d]+)\.zip'
        ),
        'codename',
    ),
)


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
    pattern = re.compile(
        r'(?:/[\w_-]+/(\w+):\d)|'
        r'(?:\(\"ro\.product\.device\"\) == \"(\w+)\")|'
        r'(?:get_device_compatible\(\"(\w+)\"\))'
    )
    matches = pattern.findall(updater_script)
    if matches:
        candidates = [value for match in matches for value in match if value]
        if candidates:
            return max(candidates, key=len)
    return 'codename'


@dataclass(frozen=True)
class _SuffixRule:
    suffix: str
    transform: Callable[[str], str]
    exceptions: frozenset[str] = frozenset()


_SUFFIX_RULES: tuple[_SuffixRule, ...] = (
    # _SuffixRule('EMERALDRGLOBAL', lambda prefix: 'emerald_r'),
    _SuffixRule('JPGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('KRGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('EEAGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('IDGLOBAL', lambda prefix: prefix.lower(), frozenset({'CUPIDGLOBAL'})),
    _SuffixRule(
        'INGLOBAL', lambda prefix: prefix.lower(), frozenset({'CHOPINGLOBAL', 'KLEINGLOBAL'})
    ),
    _SuffixRule('RUGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('TRGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('TWGLOBAL', lambda prefix: prefix.lower()),
    _SuffixRule('GLOBAL', lambda prefix: prefix.lower()),
)


def cleanup_codename(codename: str) -> str:
    """Remove region names from codename and android one's "SPROUT"."""
    codename = codename.replace('SPROUT', '')
    if codename.endswith('PRE'):
        codename = codename[: -len('PRE')]

    if '_' in codename:
        return codename.split('_', 1)[0].lower()

    upper = codename.upper()
    for rule in _SUFFIX_RULES:
        if upper.endswith(rule.suffix) and upper not in rule.exceptions:
            prefix = upper[: -len(rule.suffix)]
            return rule.transform(prefix)
    return upper.lower()


def extract_payload_codename(file_name: str) -> str:
    file_name = Path(file_name).name
    for pattern, group in PAYLOAD_CODENAME_PATTERNS:
        match = pattern.search(file_name)
        if match and match.groupdict().get(group):
            codename = match.group(group)
            return cleanup_codename(codename).lower()
    base_name = Path(file_name).stem
    android_one_segment = base_name.split('_', 1)[0]
    return cleanup_codename(android_one_segment.split('-', 1)[0]).lower()


class ScriptTemplate(Template):
    delimiter = '[-]'


def write_text_to_file(file: str | Path, text: str):
    Path(file).write_bytes(text.encode('utf-8'))
