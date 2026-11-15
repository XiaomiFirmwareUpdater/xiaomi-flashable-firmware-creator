"""Pytest-based tests for Xiaomi Flashable Firmware Creator."""

import os
import shutil
import subprocess
from contextlib import suppress
from pathlib import Path
from zipfile import ZipFile

import pytest

from xiaomi_flashable_firmware_creator.extractors import zip_extractor
from xiaomi_flashable_firmware_creator.extractors.handlers.payload_zip import PayloadError
from xiaomi_flashable_firmware_creator.xiaomi_flashable_firmware_creator import (
    FlashableFirmwareCreator,
)

TESTS_DIR = Path(__file__).parent
ROM_FILES = sorted(TESTS_DIR.glob('files/*/*.zip'))

if not ROM_FILES:
    pytestmark = pytest.mark.skip(reason='No ROM files available for tests')


@pytest.fixture(params=ROM_FILES, ids=lambda path: f'{path.parent.name}/{path.name}')
def rom_zip(request):
    """Provide each available ROM zip as an individual test parameter."""
    return request.param


def _run_auto_allowing_empty(process: str, rom_zip: Path, tmp_path: Path) -> str | None:
    """Execute auto() while tolerating expected extraction edge cases."""
    creator = FlashableFirmwareCreator(str(rom_zip), process, tmp_path)
    try:
        return creator.auto()
    except RuntimeError as err:  # pragma: no cover - defensive guard
        if str(err) != 'Nothing found to extract!':
            raise
        return None
    except PayloadError:
        return None
    finally:
        assert not creator._tmp_dir.exists()


@pytest.mark.parametrize('process', ['firmware', 'vendor'])
def test_auto_creates_flashable_zip(process: str, rom_zip: Path, tmp_path: Path) -> None:
    output = _run_auto_allowing_empty(process, rom_zip, tmp_path)
    if output:
        assert Path(output).is_file()


@pytest.mark.parametrize('process', ['firmwareless', 'nonarb'])
def test_auto_handles_missing_artifacts(process: str, rom_zip: Path, tmp_path: Path) -> None:
    _run_auto_allowing_empty(process, rom_zip, tmp_path)


def test_remote_zip_has_timeout(monkeypatch, tmp_path: Path) -> None:
    class FakeRemoteZip:
        def __init__(self, _url, **kwargs):
            self.timeout = kwargs['timeout']

        @staticmethod
        def namelist():
            return []

    monkeypatch.setattr(zip_extractor, 'RemoteZip', FakeRemoteZip)
    extractor = zip_extractor.ZipExtractor('https://example.com/rom.zip', tmp_path)
    assert extractor._extractor.timeout == (30, 300)


def test_updater_script_has_no_build_date(rom_zip: Path, tmp_path: Path) -> None:
    creator = FlashableFirmwareCreator(str(rom_zip), 'firmware', tmp_path)
    try:
        try:
            creator.extract()
        except PayloadError as err:
            pytest.skip(f'ROM payload invalid: {err}')
        creator.generate_flashing_script([])
        update_script = Path(creator._flashing_script_dir / 'updater-script').read_text()
        assert 'ro.build.date.utc' not in update_script
    finally:
        with suppress(FileNotFoundError):
            creator.cleanup()
        creator.close()


@pytest.fixture
def payload_rom_zip(tmp_path: Path) -> Path:
    rom_zip = tmp_path / 'pandora-ota_full-OS3.0.3.0.WBLCNXM-user-16.0-hash.zip'
    with ZipFile(rom_zip, 'w') as archive:
        archive.writestr('payload.bin', b'')
        archive.writestr(
            'META-INF/com/android/metadata',
            'ota-type=AB\npre-device=pandora|pandora_global\n',
        )
    return rom_zip


def test_payload_update_binary_is_portable_shell(payload_rom_zip: Path, tmp_path: Path) -> None:
    creator = FlashableFirmwareCreator(str(payload_rom_zip), 'firmware', tmp_path)
    try:
        injection_marker = tmp_path / 'hostname-injection'
        creator.host = f'$(touch {injection_marker})\nwipe_cache'
        creator.uses_payload = True
        firmware_dir = creator._tmp_dir / 'firmware-update'
        firmware_dir.mkdir()
        (firmware_dir / 'abl.img').write_bytes(b'abl')
        (firmware_dir / 'modem.img').touch()
        creator.generate_flashing_script({'modem.img'})

        update_binary = creator._flashing_script_dir / 'update-binary'
        contents = update_binary.read_text()
        assert contents.startswith('#!/sbin/sh\n')
        assert 'wipe_cache' not in contents
        image_check = contents.index('\ncheck_image abl 203d2b8b')
        preflight = contents.index('\npreflight_partition abl 3\n')
        inactive = contents.index('\nflash_slot "$INACTIVE_SLOT"\n')
        active = contents.index('\nflash_slot "$ACTIVE_SLOT"\n')
        assert image_check < preflight < inactive < active
        assert 'preflight_partition modem' not in contents
        assert "TARGET_DEVICES='pandora pandora_global'" in contents
        assert 'for slot in a b' in contents
        assert 'conv=fsync' in contents
        assert 'iflag=count_bytes' in contents
        assert 'head -c' not in contents
        subprocess.run(['/bin/sh', '-n', update_binary], check=True)

        output = creator.make_zip()
        with ZipFile(output) as archive:
            info = archive.getinfo('META-INF/com/google/android/update-binary')
            assert info.compress_type == 8
            assert archive.read(info).startswith(b'#!/sbin/sh\n')
            assert 'META-INF/com/google/android/updater-script' not in archive.namelist()
            assert archive.getinfo('firmware-update/abl.img').compress_type == 8
            assert archive.testzip() is None

        required_tools = ('bash', 'blockdev', 'dd', 'head', 'sed', 'sha256sum', 'tr', 'unzip')
        if Path('/proc/self/fd').exists() and all(shutil.which(tool) for tool in required_tools):
            tools_dir = tmp_path / 'tools'
            tools_dir.mkdir()
            getprop = tools_dir / 'getprop'
            getprop.write_text(
                '#!/bin/sh\n'
                'case "$1" in\n'
                '  ro.product.device) echo pandora ;;\n'
                '  ro.boot.slot_suffix) echo _a ;;\n'
                'esac\n'
            )
            getprop.chmod(0o755)
            result = subprocess.run(
                ['bash', update_binary, '3', '1', output],
                check=False,
                capture_output=True,
                text=True,
                env={'PATH': f'{tools_dir}:{os.environ["PATH"]}'},
            )
            assert result.returncode != 0
            assert 'Missing block device: abl_a' in result.stdout
            assert '[INFO] Updating' not in result.stdout
            assert not injection_marker.exists()
    finally:
        creator.cleanup()
        creator.close()


@pytest.mark.parametrize(
    ('filename', 'message'),
    [(None, 'No firmware images found'), ('xbl.config.img', 'invalid partition name')],
)
def test_payload_update_binary_rejects_unsafe_images(
    payload_rom_zip: Path, tmp_path: Path, filename: str | None, message: str
) -> None:
    creator = FlashableFirmwareCreator(str(payload_rom_zip), 'firmware', tmp_path)
    try:
        creator.uses_payload = True
        if filename:
            firmware_dir = creator._tmp_dir / 'firmware-update'
            firmware_dir.mkdir()
            (firmware_dir / filename).write_bytes(b'image')
        with pytest.raises(RuntimeError, match=message):
            creator.generate_flashing_script(set())
    finally:
        creator.cleanup()
        creator.close()


@pytest.mark.parametrize(
    ('metadata', 'message'),
    [
        (None, 'no valid OTA metadata'),
        ('ota-type=BLOCK\npre-device=pandora\n', 'ota-type=AB'),
        ('ota-type=AB\npre-device=pandora;reboot\n', 'no valid pre-device'),
    ],
)
def test_payload_update_binary_rejects_unsafe_metadata(
    tmp_path: Path, metadata: str | None, message: str
) -> None:
    rom_zip = tmp_path / 'pandora-ota_full-V1-user-1.0-hash.zip'
    with ZipFile(rom_zip, 'w') as archive:
        archive.writestr('payload.bin', b'')
        if metadata is not None:
            archive.writestr('META-INF/com/android/metadata', metadata)

    creator = FlashableFirmwareCreator(str(rom_zip), 'firmware', tmp_path)
    try:
        creator.uses_payload = True
        firmware_dir = creator._tmp_dir / 'firmware-update'
        firmware_dir.mkdir()
        (firmware_dir / 'abl.img').write_bytes(b'abl')
        with pytest.raises(RuntimeError, match=message):
            creator.generate_flashing_script(set())
    finally:
        creator.cleanup()
        creator.close()


def test_non_payload_update_binary_is_preserved(tmp_path: Path) -> None:
    rom_zip = tmp_path / 'mocked_miui_TEST_V1.0.0.0.TEST_1.0.zip'
    original = b'original update binary'
    with ZipFile(rom_zip, 'w') as archive:
        archive.writestr('META-INF/com/google/android/update-binary', original)
        archive.writestr(
            'META-INF/com/google/android/updater-script',
            'package_extract_file("firmware-update/modem.mbn", '
            '"/dev/block/bootdevice/by-name/modem");',
        )
        archive.writestr('firmware-update/modem.mbn', b'modem')

    creator = FlashableFirmwareCreator(str(rom_zip), 'firmware', tmp_path)
    try:
        _, invalid_files = creator.extract()
        update_binary = creator._flashing_script_dir / 'update-binary'

        assert update_binary.read_bytes() == original

        assert creator.uses_payload is False
        creator.generate_flashing_script(invalid_files)
        assert update_binary.read_bytes() == original

        with ZipFile(creator.make_zip()) as archive:
            assert archive.read('META-INF/com/google/android/update-binary') == original
    finally:
        creator.cleanup()
        creator.close()
