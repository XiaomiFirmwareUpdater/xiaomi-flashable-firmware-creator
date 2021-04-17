"""
Xiaomi Flashable Firmware Creator class.

Xiaomi Flashable Firmware Creator class provides an easy way to
   create a flashable firmware zip file from any supported ROM.
Using extract, generate_updater_script, and make_zip you can create
   flashable files according to the provided configuration
   ('firmware', 'nonarb', 'firmwareless', 'vendor) .
"""

# pylint: disable=too-many-instance-attributes
import re
from datetime import datetime
from pathlib import Path
from shutil import rmtree, make_archive, copy2
from socket import gethostname
from typing import List

from xiaomi_flashable_firmware_creator import work_dir
from xiaomi_flashable_firmware_creator.extractors.handlers.android_one_zip import AndroidOneZip
from xiaomi_flashable_firmware_creator.extractors.zip_extractor import ZipExtractor
from xiaomi_flashable_firmware_creator.helpers.misc import extract_codename, \
    ScriptTemplate, cleanup_codename
from xiaomi_flashable_firmware_creator.types import ProcessTypes, ZipTypes


class FlashableFirmwareCreator:
    """FlashableFirmwareCreator provides methods for creating \
     flashable firmware files from Xiaomi supported ROMs."""

    extractor: ZipExtractor
    input_file: str
    _tmp_dir: Path
    _flashing_script_dir: Path
    host: str
    datetime: datetime
    _extract_mode: str
    extract_mode: ProcessTypes
    type: ZipTypes
    update_script: str
    is_android_one: bool

    def __init__(self, input_file, _extract_mode, out_dir=""):
        """
        Initialize FlashableFirmwareCreator.

        :param input_file: zip file to extract from.
         It can be a local path or a remote direct url.
        :param _extract_mode: Which mode should the tool use.
         This must be one of "firmware", "nonarb", "firmwareless" or "vendor".
        :param out_dir: The output directory to store the extracted file in.
        """
        self.input_file = input_file
        self._tmp_dir = Path(out_dir) / 'tmp' if out_dir else work_dir / 'tmp'
        self._out_dir = self._tmp_dir.parent.absolute()
        self._flashing_script_dir = self._tmp_dir.absolute() / 'META-INF/com/google/android'
        self.host = gethostname()
        self.datetime = datetime.now()
        self.extract_mode = self.get_extract_mode(_extract_mode)
        self.update_script = ''
        self.is_android_one = False
        self.firmware_excluded_files = ['dtbo', 'logo', 'splash', 'vbmeta', 'boot.img', 'system',
                                        'vendor', 'product', 'odm', 'exaid',
                                        'dynamic_partitions_op_list']
        self.extractor = ZipExtractor(self.input_file, self._tmp_dir)
        self.init()

    def init(self):
        """
        Do some initial checks and housekeeping.

        - This method checks if the temporary directory exists
         and removes it then creates a new one.
        - Creates updater-script temporary path.
        - Checks if the input zip file exists and
         raise a FileNotFoundError exception if not.
        - Open the zip and get contents list.
        - Checks if the zip file is a valid ROM. If true get the ROM type.
         Otherwise, remove the temporary directory and raise a RuntimeError.
        """
        if self._tmp_dir.exists():
            rmtree(self._tmp_dir)
        self._tmp_dir.mkdir(parents=True, exist_ok=True)
        self._flashing_script_dir.mkdir(parents=True, exist_ok=True)
        if not self.extractor.exists():
            raise FileNotFoundError(
                f"input file {self.input_file} does not exist!")
        self.extractor.get_files_list()
        if not self.is_valid_rom():
            rmtree(self._tmp_dir)
            raise RuntimeError(
                f"{self.input_file} is not a valid ROM file. Exiting..")

    @staticmethod
    def get_extract_mode(extract_mode) -> ProcessTypes:
        """
        Get the extract mode enum according to extract_mode string value.

        :param extract_mode: "firmware", "nonarb", "firmwareless" or "vendor"
        :return: ProcessTypes enum
        """
        modes = {
            'firmware': ProcessTypes.firmware,
            'nonarb': ProcessTypes.non_arb_firmware,
            'firmwareless': ProcessTypes.firmware_less,
            'vendor': ProcessTypes.vendor
        }
        try:
            return modes[extract_mode]
        except KeyError as err:
            print('Unknown process!')
            raise err

    def is_valid_rom(self) -> bool:
        """
        Check if the zip file is valid ROM.

        :return: True if update-binary or updater-script or payload.bin is present
         in contents list, False otherwise.
        """
        return "META-INF/com/google/android/update-binary" in self.extractor.files \
               or "META-INF/com/google/android/updater-script" in self.extractor.files \
               or "payload.bin" in self.extractor.files

    def get_rom_type(self):
        """
        Get the type of the input ROM or raise a RuntimeError.

        :return: An enum of ROM type. Either qcom or mtk.
        """
        files = str(self.extractor.files)
        if 'lk.img' in files or 'preloader.img' in files:
            self.type = ZipTypes.mtk
        elif 'firmware-update' in files or 'rpm' in files or 'tz' in files \
                or 'keymaster' in files:
            self.type = ZipTypes.qcom
        else:
            raise RuntimeError("Can't detect rom type. It's not qcom or mtk!'")

    def get_files_list(self) -> List[str]:
        """
        Get files to extract list according to the extract mode Enum.

        :return: a list of file names string.
        """
        # TODO: match fastboot and android one img files
        #  when no firmware-update directory is found
        if self.extract_mode is ProcessTypes.firmware:
            return [i for i in self.extractor.files if
                    (i.startswith('META-INF/')
                     and (i.endswith('updater-script') or i.endswith('update-binary'))
                     ) or all(n not in i for n in self.firmware_excluded_files)] \
                if self.type is ZipTypes.qcom \
                else [n for n in self.extractor.files if all(
                file not in n for file in self.firmware_excluded_files + ['file_contexts'])]
        if self.extract_mode is ProcessTypes.non_arb_firmware:
            return [n for n in self.extractor.files if 'dspso.bin' in n
                    or n.startswith('firmware-update/BTFM.bin')
                    or n.startswith('firmware-update/NON-HLOS.bin')
                    or n.startswith('META-INF/')
                    and (n.endswith('updater-script') or n.endswith('update-binary'))]
        if self.extract_mode is ProcessTypes.firmware_less:
            return [n for n in self.extractor.files if not n.startswith('firmware-update/')] \
                if self.type is ZipTypes.qcom else []
        if self.extract_mode is ProcessTypes.vendor:
            return [n for n in self.extractor.files if not n.startswith('system')
                    and not n.startswith('vbmeta')]
        return []  # Will never happen

    def get_updater_script_lines(self) -> str:
        """
        Get selective lines from the update-script according to process type enum value.

        :return: a string of the updater-script lines
        """
        original_updater_script = Path(self._flashing_script_dir / 'updater-script')
        if not original_updater_script.exists():
            raise FileNotFoundError("updater-script not found!")
        original_updater_script = original_updater_script.read_text().splitlines()
        lines = []
        if self.extract_mode is ProcessTypes.firmware:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "firmware-update" in line and ("ro.product" in line or all(
                file not in line for file in self.firmware_excluded_files))] \
                if self.type is ZipTypes.qcom \
                else [line for line in original_updater_script if "ro.product" in line or
                      all(file not in line for file in self.firmware_excluded_files)]
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "modem" in line or "bluetooth" in line or "dsp" in line]
        elif self.extract_mode is ProcessTypes.firmware_less:
            lines = [line for line in original_updater_script if "getprop" in line
                     or "Target" in line
                     or "boot.img" in line or "system" in line or "vendor" in line
                     or "product" in line] \
                if self.type is ZipTypes.qcom else []
        elif self.extract_mode is ProcessTypes.vendor:
            lines = [line for line in original_updater_script
                     if "getprop" in line or "Target" in line
                     or "firmware-update" in line
                     or "vendor" in line] if self.type is ZipTypes.qcom \
                else [line for line in original_updater_script if
                      "system" not in line and 'boot.img' not in line]
        return '\n'.join(lines)

    def generate_updater_script(self):
        """
        Generate the new zip updater-script and write it to the temporary directory.

        :return:
        """
        template = ScriptTemplate(Path(
            Path(__file__).parent / 'templates/recovery_updater_script').read_text())
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
        with open(f"{str(self._flashing_script_dir)}/updater-script", "w") as out:
            out.write(updater_script)
        # Use modified dynamic_partitions_op_list with resize vendor line only
        if self.extract_mode is ProcessTypes.vendor and "dynamic_partitions_op_list" in updater_script:
            original_dynamic_partitions_list = Path(self._tmp_dir / 'dynamic_partitions_op_list').read_text()
            vendor_resize = re.search(r'(resize vendor .*$)', original_dynamic_partitions_list, re.M)
            if vendor_resize:
                with open(f"{str(self._tmp_dir)}/dynamic_partitions_op_list", "w") as out:
                    out.write(vendor_resize.group(1))

    # def generate_update_binary(self):
    #     """
    #     Generate the new zip update-binary and write it to the temporary directory.
    #
    #     :return:
    #     """
    #     template = ScriptTemplate(Path(
    #         Path(__file__).parent / 'templates/recovery_update-binary').read_text())
    #     update_binary_text = template.substitute(datetime=self.datetime, host=self.host)
    #     update_binary = Path(f"{str(self._flashing_script_dir)}/update-binary")
    #     update_binary.write_text(update_binary_text)
    #     update_binary.chmod(775)

    def generate_ab_updater_script(self):
        script_template = ScriptTemplate(Path(
            Path(__file__).parent / 'templates/recovery_ab_updater_script').read_text())
        flashing_template = ScriptTemplate(Path(
            Path(__file__).parent / 'templates/partition_flashing').read_text())
        lines = [flashing_template.substitute(partition=file.split('/')[-1].split('.')[0])
                 for file in self.get_files_list()
                 if file.startswith('firmware-update/')]
        updater_script = script_template.substitute(
            datetime=self.datetime, host=self.host,
            zip_name=self.extractor.get_file_name(), lines='\n'.join(lines))
        with open(f"{str(self._flashing_script_dir)}/updater-script", "w") as out:
            out.write(updater_script)

    def generate_flashing_script(self):
        """
        Generate update_script or update-binary
        :return:
        """
        if self.is_android_one is True:
            self.generate_ab_updater_script()
            copy2(Path(Path(__file__).parent / 'binaries/update-binary'),
                  f"{str(self._flashing_script_dir)}/update-binary")
        else:
            self.generate_updater_script()

    def make_zip(self) -> str:
        """
        Compress the temporary directory into a zip archive in output directory.

        Also, name it according to process parameters.
        :return:
        """
        out = Path(f'{self._out_dir}/result.zip')
        partial_path = '/'.join(out.parts[1:-1])
        make_archive(f"/{partial_path}/{out.stem}", 'zip', self._tmp_dir)
        if not out.exists():
            raise RuntimeError("Could not create result zip file!")
        if not self.is_android_one:
            codename = extract_codename(self.update_script)
        else:
            codename = cleanup_codename(self.extractor.get_file_name().split('_')[1]).lower()
        zip_prefix = ""
        if self.extract_mode is ProcessTypes.firmware:
            zip_prefix = "fw"
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            zip_prefix = "fw-non-arb"
        elif self.extract_mode is ProcessTypes.firmware_less:
            zip_prefix = "fw-less"
        elif self.extract_mode is ProcessTypes.vendor:
            zip_prefix = "fw-vendor"
        else:
            pass  # This should never happen
        zip_name = f"{self._out_dir}/{zip_prefix}_{codename}_{self.extractor.get_file_name()}"
        out.rename(zip_name)
        return zip_name

    def extract(self):
        """
        Invoke the extract method of extractor object.

        :return:
        """
        if hasattr(self.extractor, 'handler') and isinstance(self.extractor.handler, AndroidOneZip):
            self.is_android_one = True
            self.extractor.prepare()
        self.get_rom_type()
        files_to_extract = self.get_files_list()
        if not files_to_extract or (
                len(files_to_extract) == 2
                and "updater-script" in str(files_to_extract)
                and "update-binary" in str(files_to_extract)
        ):
            self.cleanup()
            self.close()
            raise RuntimeError("Nothing found to extract!")
        self.extractor.extract(files_to_extract)

    def cleanup(self):
        """
        Cleanup temporary directory and files.

        :return:
        """
        rmtree(self._tmp_dir)

    def close(self):
        """
        Invoke close method of the extractor object.

        :return:
        """
        self.extractor.close()

    def auto(self) -> str:
        """
        Auto-pilot method for doing everything with a single call.

        This is useful for using this class from a command line interface
         or another application.
        :return: output zip file name as a string.
        """
        self.extract()
        print("Generating flashing script...")
        self.generate_flashing_script()
        print("Creating new zip file..")
        new_zip = self.make_zip()
        self.cleanup()
        self.close()
        return new_zip
