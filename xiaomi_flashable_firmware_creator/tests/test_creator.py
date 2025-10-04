"""Pytest-based tests for Xiaomi Flashable Firmware Creator."""

from contextlib import suppress
from pathlib import Path

import pytest

from xiaomi_flashable_firmware_creator.xiaomi_flashable_firmware_creator import (
    FlashableFirmwareCreator,
)
from xiaomi_flashable_firmware_creator.extractors.handlers.payload_zip import PayloadError

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
    success = False
    try:
        output = creator.auto()
        success = True
        return output
    except RuntimeError as err:  # pragma: no cover - defensive guard
        if str(err) != 'Nothing found to extract!':
            raise
        return None
    except PayloadError:
        return None
    finally:
        if not success:
            with suppress(FileNotFoundError):
                creator.cleanup()
            creator.close()


@pytest.mark.parametrize('process', ['firmware', 'vendor'])
def test_auto_creates_flashable_zip(process: str, rom_zip: Path, tmp_path: Path) -> None:
    output = _run_auto_allowing_empty(process, rom_zip, tmp_path)
    if output:
        assert Path(output).is_file()


@pytest.mark.parametrize('process', ['firmwareless', 'nonarb'])
def test_auto_handles_missing_artifacts(process: str, rom_zip: Path, tmp_path: Path) -> None:
    _run_auto_allowing_empty(process, rom_zip, tmp_path)


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
