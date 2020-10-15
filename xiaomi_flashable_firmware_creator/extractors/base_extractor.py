from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from shutil import rmtree, make_archive
from socket import gethostname
from string import Template
from typing import List

from xiaomi_flashable_firmware_creator import work_dir
from xiaomi_flashable_firmware_creator.extractors.types import ProcessTypes, ZipTypes
from xiaomi_flashable_firmware_creator.helpers.misc import extract_codename


class BaseExtractor(ABC):
    _tmp_dir: Path
    _updater_script_dir: Path
    host: str
    datetime: datetime
    _extract_mode: str
    extract_mode: ProcessTypes
    zip_type: ZipTypes
    files: List[str]
    update_script: str

    def __init__(self, _extract_mode, out_dir=""):
        self._tmp_dir = Path(out_dir) / 'tmp' if out_dir else work_dir / 'tmp'
        self._out_dir = self._tmp_dir.parent
        self._updater_script_dir = self._tmp_dir / 'META-INF/com/google/android'
        self.host = gethostname()
        self.datetime = datetime.now()
        self.extract_mode = self.get_extract_mode(_extract_mode)
        self.files = []
        self.update_script = ''
        self.init()

    def init(self):
        """Initial checks and housekeeping"""
        if self._tmp_dir.exists():
            rmtree(self._tmp_dir)
        self._tmp_dir.mkdir(parents=True, exist_ok=True)
        self._updater_script_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_extract_mode(extract_mode):
        modes = {
            'firmware': ProcessTypes.firmware,
            'nonarb': ProcessTypes.non_arb_firmware,
            'firmwareless': ProcessTypes.firmware_less,
            'vendor': ProcessTypes.vendor
        }
        try:
            return modes[extract_mode]
        except KeyError:
            raise RuntimeError('Unknown process!')

    def is_valid_firmware_zip(self):
        return "META-INF/com/google/android/update-binary" in self.files \
               or "META-INF/com/google/android/updater-script" in self.files

    def get_fw_type(self):
        if 'firmware-update' in str(self.files):
            self.zip_type = ZipTypes.qcom
        elif 'lk.img' in str(self.files) or 'preloader.img' in str(self.files):
            self.zip_type = ZipTypes.mtk

    def get_files_list(self):
        if self.extract_mode is ProcessTypes.firmware:
            return [i for i in self.files if
                    (i.startswith('META-INF/')
                     and (i.endswith('updater-script') or i.endswith('update-binary'))
                     ) or (i.startswith('firmware-update/')
                           and 'dtbo' not in i
                           and 'splash' not in i
                           and 'logo' not in i
                           and 'vbmeta' not in i)] \
                if self.zip_type is ZipTypes.qcom \
                else [n for n in self.files if 'system' not in n
                      and 'vendor' not in n
                      and 'product' not in n
                      and 'boot.img' not in n
                      and 'file_contexts' not in n]
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            return [n for n in self.files if n.startswith('firmware-update/dspso.bin')
                    or n.startswith('firmware-update/BTFM.bin')
                    or n.startswith('firmware-update/NON-HLOS.bin')
                    or n.startswith('META-INF/')]
        elif self.extract_mode is ProcessTypes.firmware_less:
            return [n for n in self.files if not n.startswith('firmware-update/')] \
                if self.zip_type is ZipTypes.qcom else []
        elif self.extract_mode is ProcessTypes.vendor:
            return [n for n in self.files if not n.startswith('system')
                    and not n.startswith('vbmeta')]
        else:
            return []  # Will never happen

    @abstractmethod
    def extract(self):
        raise NotImplementedError

    def get_updater_script_lines(self):
        original_updater_script = Path(self._updater_script_dir / 'updater-script'
                                       ).read_text().splitlines()
        lines = []
        if self.extract_mode is ProcessTypes.firmware:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "firmware-update" in line and "dtbo.img" not in line
                     and "vbmeta" not in line and "splash" not in line
                     and "logo" not in line] \
                if self.zip_type is ZipTypes.qcom \
                else [line for line in original_updater_script if "system" not in line
                      and "vendor" not in line and 'boot.img' not in line]
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "modem" in line or "bluetooth" in line or "dsp" in line]
        elif self.extract_mode is ProcessTypes.firmware_less:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "boot.img" in line or "system" in line or "vendor" in line
                     or "product" in line] \
                if self.zip_type is ZipTypes.qcom else []
        elif self.extract_mode is ProcessTypes.vendor:
            lines = [line for line in original_updater_script
                     if "getprop" in line or "Target" in line
                     or "firmware-update" in line
                     or "vendor" in line] if self.zip_type is ZipTypes.qcom \
                else [line for line in original_updater_script if
                      "system" not in line and 'boot.img' not in line]
        return '\n'.join(lines)

    def generate_updater_script(self):
        current_dir = Path(__file__).parent
        template = Template(Path(
            current_dir.parent / 'templates/recovery_updater_script.txt').read_text())
        lines = self.get_updater_script_lines()
        if not lines:
            raise RuntimeError("Could not extract lines from updater-script!")
        if self.extract_mode is ProcessTypes.firmware:
            process = "Normal Firmware"
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            process = "non-ARB firmware"
        elif self.extract_mode is ProcessTypes.firmware_less:
            process = "firmware-less ROM"
        elif self.extract_mode is ProcessTypes.vendor:
            process = "firmware+vendor"
        else:
            process = "Unknown"  # This should never happen

        updater_script = template.substitute(datetime=self.datetime, host=self.host,
                                             process=process, lines=lines)
        # correct some updater-script lines that exist in old devices' file
        if "/firmware/image/sec.dat" in updater_script:
            updater_script = updater_script.replace(
                '/firmware/image/sec.dat', '/dev/block/bootdevice/by-name/sec')
        if '/firmware/image/splash.img' in updater_script:
            updater_script = updater_script.replace(
                '/firmware/image/splash.img', '/dev/block/bootdevice/by-name/splash')
        self.update_script = updater_script
        with open(f"{str(self._updater_script_dir)}/updater-script", "w") as out:
            out.write(updater_script)

    def make_zip(self):
        out = Path(f'{self._out_dir}/result.zip')
        make_archive(str(out).split('.')[0], 'zip', self._tmp_dir)
        if not out.exists():
            raise RuntimeError("Could not create result zip file!")
        codename = extract_codename(self.update_script)
        if self.extract_mode is ProcessTypes.firmware:
            out.rename(f"{self._out_dir}/fw_{codename}_{self.get_zip_name()}")
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            out.rename(f"{self._out_dir}/fw-non-arb_{codename}_{self.get_zip_name()}")
        elif self.extract_mode is ProcessTypes.firmware_less:
            out.rename(f"{self._out_dir}/fw-less_{codename}_{self.get_zip_name()}")
        elif self.extract_mode is ProcessTypes.vendor:
            out.rename(f"{self._out_dir}/fw-vendor_{codename}_{self.get_zip_name()}")
        else:
            pass  # This should never happen

    def cleanup(self):
        rmtree(self._tmp_dir)

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def get_zip_name(self):
        raise NotImplementedError
