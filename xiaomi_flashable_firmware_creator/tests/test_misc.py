"""Pytest-based regression tests for misc helpers."""

from pathlib import Path

import pytest

from xiaomi_flashable_firmware_creator.helpers.misc import (
    cleanup_codename,
    extract_codename,
    extract_payload_codename,
)

TESTS_DIR = Path(__file__).parent
UPDATER_SCRIPTS = sorted((TESTS_DIR / 'files/updater-scripts').glob('*'))

if not UPDATER_SCRIPTS:
    pytestmark = pytest.mark.skip(reason='No updater-script fixtures available')


@pytest.mark.parametrize('script_path', UPDATER_SCRIPTS, ids=lambda path: path.name)
def test_extract_codename(script_path: Path) -> None:
    codename = extract_codename(script_path.read_text())
    assert codename and codename != 'codename'


def test_extract_codename_prefers_longest_candidate() -> None:
    script = (
        'if get_device_compatible("kle") || abort();\n'
        'getprop("ro.product.device") == "KLEIN" || abort();\n'
    )
    assert extract_codename(script) == 'KLEIN'


@pytest.mark.parametrize(
    'file_name,expected',
    [
        ('miui_KLEININGlobal_V816.0.3.0.UGSINXM_dbc3ca2050_14.0.zip', 'klein'),
        ('miui_APOLLO_V12.5.3.0.RJDCNXM_d98b4e09b5_11.0.zip', 'apollo'),
        (
            'miui_ANGELICAININGlobal_V12.0.19.0.QCRINXM_355be36c6c_10.0.zip',
            'angelicain',
        ),
        (
            'miui_AGATEEEAGlobal_V13.0.1.0.SKUEUXM_1234567890_12.0.zip',
            'agate',
        ),
        (
            'miui_LAVENDERINGlobal_V14.0.1.0.TEAINXM_a1b2c3d4e5_13.0.zip',
            'lavender',
        ),
        (
            'miui_CUPIDGlobal_V14.0.3.0.TLCEUXM_f1e2d3c4b5_13.0.zip',
            'cupid',
        ),
        (
            'miui_HMWSGGlobal_V6.6.1.0.KHBMICF_033545b329_4.4.zip',
            'hmwsg',
        ),
        (
            'miui_EMERALDRGlobal_OS1.0.1.0.UFOMIXM_76a0f6e428_14.0.zip',
            'emeraldr',
        ),
        (
            'miui_WATERGlobal_V14.0.40.0.TGOMIXM_2107d4a455_13.0.zip',
            'water',
        ),
        (
            'miui_CMIGlobal_OS1.0.2.0.TJAMIXM_31571224b7_13.0.zip',
            'cmi',
        ),
        (
            'miui_DITINGJPGlobal_OS1.0.18.0.ULFJPXM_e571fa75a2_14.0.zip',
            'diting',
        ),
        (
            'miui_RUBYKRGlobal_OS1.0.1.0.UMOKRXM_17fa26a30e_14.0.zip',
            'ruby',
        ),
        ('pandora-ota_full-OS3.0.3.0.WBLCNXM-user-16.0-6fb27afb9b.zip', 'pandora'),
        ('air-ota_full-OS2.0.209.0.VGQCNXM-user-15.0-ab49a7767d.zip', 'air'),
        (
            'air_eea_global-ota_full-OS2.0.205.0.VGQEUXM-user-15.0-19ba823095.zip',
            'air',
        ),
        (
            'amethyst_ru_global-ota_full-OS2.0.202.0.VOPRUXM-user-15.0-c62176f993.zip',
            'amethyst',
        ),
        (
            'aurora_tw_global-ota_full-OS2.0.2.0.VGQTWXM-user-15.0-eaf08568df.zip',
            'aurora',
        ),
        (
            'miui_LAURELSPROUTGlobal_V12.0.26.0.RFQMIXM_88b2e6c4fb_11.0.zip',
            'laurel',
        ),
        (
            'miui_LAURELSPROUTEEAGlobal_V12.0.23.0.RFQEUXM_b8e12280dc_11.0.zip',
            'laurel',
        ),
    ],
)
def test_extract_payload_codename(file_name: str, expected: str) -> None:
    assert extract_payload_codename(file_name) == expected


@pytest.mark.parametrize(
    'codename,cleaned',
    [
        ('KLEININGlobal', 'klein'),
        ('KLEINGlobal', 'klein'),
        ('CHOPINGlobal', 'chopin'),
        ('air_eea_global', 'air'),
        ('amethyst_ru_global', 'amethyst'),
        ('AGATEEEAGlobal', 'agate'),
        ('LAVENDERINGlobal', 'lavender'),
        ('CUPIDGlobal', 'cupid'),
        ('HMWSGGlobal', 'hmwsg'),
        ('ROCKIDGlobal', 'rock'),
        ('VEUXJPGlobal', 'veux'),
        ('EMERALDRGlobal', 'emeraldr'),
        ('WATERGlobal', 'water'),
        ('CMIGlobal', 'cmi'),
        ('DITINGJPGlobal', 'diting'),
        ('RUBYKRGlobal', 'ruby'),
    ],
)
def test_cleanup_codename_handles_in_regions(codename: str, cleaned: str) -> None:
    assert cleanup_codename(codename) == cleaned
