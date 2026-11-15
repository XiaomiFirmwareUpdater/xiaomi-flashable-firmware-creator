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
from hashlib import file_digest, md5
from pathlib import Path
from shlex import quote
from shutil import make_archive, rmtree
from socket import gethostname
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from xiaomi_flashable_firmware_creator import work_dir
from xiaomi_flashable_firmware_creator.extractors.handlers.payload_zip import PayloadZip
from xiaomi_flashable_firmware_creator.extractors.zip_extractor import ZipExtractor
from xiaomi_flashable_firmware_creator.helpers.misc import (
    ScriptTemplate,
    extract_codename,
    extract_payload_codename,
    write_text_to_file,
)
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
    uses_payload: bool

    def __init__(self, input_file, _extract_mode, out_dir=''):
        """
        Initialize FlashableFirmwareCreator.

        :param input_file: zip file to extract from.
         It can be a local path or a remote direct url.
        :param _extract_mode: Which mode should the tool use.
         This must be one of "firmware", "nonarb", "firmwareless" or "vendor".
        :param out_dir: The output directory to store the extracted file in.
        """
        self.input_file = input_file
        _tmp_sub_dir = md5(Path(input_file).name.encode()).hexdigest()
        self._tmp_dir = (
            Path(out_dir) / 'tmp' / _tmp_sub_dir if out_dir else work_dir / 'tmp' / _tmp_sub_dir
        )
        self._out_dir = self._tmp_dir.parent.parent.absolute()
        self._flashing_script_dir = self._tmp_dir.absolute() / 'META-INF/com/google/android'
        self.host = gethostname()
        self.datetime = datetime.now()
        self.extract_mode = self.get_extract_mode(_extract_mode)
        self.update_script = ''
        self.uses_payload = False
        self.firmware_excluded_files = [
            'dtbo',
            'logo',
            'splash',
            'vbmeta',
            'boot.img',
            'recovery.img',
            'system',
            'vendor',
            'product',
            'odm',
            'exaid',
            'mi_ext',
            'dynamic_partitions_op_list',
            'metadata.pb',
        ]
        self.vendor_excluded_files = [
            'vbmeta',
            'system',
            'product.',
            'odm.',
            'metadata.pb',
        ]
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
            raise FileNotFoundError(f'input file {self.input_file} does not exist!')
        self.extractor.get_files_list()
        if not self.is_valid_rom():
            rmtree(self._tmp_dir)
            raise RuntimeError(f'{self.input_file} is not a valid ROM file. Exiting..')

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
            'vendor': ProcessTypes.vendor,
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
        return (
            'META-INF/com/google/android/update-binary' in self.extractor.files
            or 'META-INF/com/google/android/updater-script' in self.extractor.files
            or 'payload.bin' in self.extractor.files
        )

    def get_rom_type(self):
        """
        Get the type of the input ROM or raise a RuntimeError.

        :return: An enum of ROM type. Either qcom or mtk.
        """
        files = str(self.extractor.files)
        if 'lk.img' in files or 'preloader.img' in files:
            self.type = ZipTypes.mtk
        elif 'firmware-update' in files or 'rpm' in files or 'tz' in files or 'keymaster' in files:
            self.type = ZipTypes.qcom
        else:
            raise RuntimeError("Can't detect rom type. It's not qcom or mtk!'")

    def get_files_list(self) -> list[str]:
        """
        Get files to extract list according to the extract mode Enum.

        :return: a list of file names string.
        """
        # TODO: match fastboot and android one img files
        #  when no firmware-update directory is found
        if self.extract_mode is ProcessTypes.firmware:
            return (
                [
                    i
                    for i in self.extractor.files
                    if (
                        i.startswith('META-INF/')
                        and (i.endswith('updater-script') or i.endswith('update-binary'))
                    )
                    or all(n not in i for n in self.firmware_excluded_files)
                ]
                if self.type is ZipTypes.qcom
                else [
                    n
                    for n in self.extractor.files
                    if all(
                        file not in n for file in self.firmware_excluded_files + ['file_contexts']
                    )
                ]
            )
        if self.extract_mode is ProcessTypes.non_arb_firmware:
            return [
                n
                for n in self.extractor.files
                if 'dspso.bin' in n
                or n.startswith('firmware-update/BTFM.bin')
                or n.startswith('firmware-update/NON-HLOS.bin')
                or n.startswith('META-INF/')
                and (n.endswith('updater-script') or n.endswith('update-binary'))
            ]
        if self.extract_mode is ProcessTypes.firmware_less:
            return (
                [n for n in self.extractor.files if not n.startswith('firmware-update/')]
                if self.type is ZipTypes.qcom
                else []
            )
        if self.extract_mode is ProcessTypes.vendor:
            return [
                i
                for i in self.extractor.files
                if all(n not in i for n in self.vendor_excluded_files)
            ]
        return []  # Will never happen

    def get_updater_script_lines(self, invalid_files: set[str]) -> str:
        """
        Get selective lines from the update-script according to process type enum value.

        :return: a string of the updater-script lines
        """
        original_updater_script = Path(self._flashing_script_dir / 'updater-script')
        if not original_updater_script.exists():
            raise FileNotFoundError('updater-script not found!')
        original_updater_script = original_updater_script.read_text().splitlines()
        lines = []
        if self.extract_mode is ProcessTypes.firmware:
            lines = (
                [
                    line
                    for line in original_updater_script
                    if ('getprop' in line and 'ro.build.date.utc' not in line)
                    or 'Target' in line
                    or (
                        'firmware-update' in line
                        and line.split('/')[1].split('"')[0] not in invalid_files
                    )
                    and (
                        'ro.product' in line
                        or all(file not in line for file in self.firmware_excluded_files)
                    )
                ]
                if self.type is ZipTypes.qcom
                else [
                    line
                    for line in original_updater_script
                    if 'ro.product' in line
                    or all(file not in line for file in self.firmware_excluded_files)
                ]
            )
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            lines = [
                line
                for line in original_updater_script
                if ('getprop' in line and 'ro.build.date.utc' not in line)
                or 'Target' in line
                or 'modem' in line
                or 'bluetooth' in line
                or 'dsp' in line
            ]
        elif self.extract_mode is ProcessTypes.firmware_less:
            lines = (
                [
                    line
                    for line in original_updater_script
                    if ('getprop' in line and 'ro.build.date.utc' not in line)
                    or 'Target' in line
                    or 'boot.img' in line
                    or 'system' in line
                    or 'vendor' in line
                    or 'product' in line
                ]
                if self.type is ZipTypes.qcom
                else []
            )
        elif self.extract_mode is ProcessTypes.vendor:
            lines = (
                [
                    line
                    for line in original_updater_script
                    if ('getprop' in line and 'ro.build.date.utc' not in line)
                    or 'Target' in line
                    or 'dynamic_partitions_op_list' in line
                    or (
                        'firmware-update' in line
                        and line.split('/')[1].split('"')[0] not in invalid_files
                    )
                    and 'vbmeta' not in line
                    or 'vendor' in line
                ]
                if self.type is ZipTypes.qcom
                else [
                    line
                    for line in original_updater_script
                    if 'system' not in line and 'boot.img' not in line
                ]
            )
        return '\n'.join(lines)

    def generate_updater_script(self, invalid_files: set[str]):
        """
        Generate the new zip updater-script and write it to the temporary directory.

        :return:
        """
        template = ScriptTemplate(
            Path(Path(__file__).parent / 'templates/recovery_updater_script').read_text()
        )
        lines = self.get_updater_script_lines(invalid_files)
        if not lines:
            raise RuntimeError('Could not extract lines from updater-script!')
        if self.extract_mode is ProcessTypes.firmware:
            process = 'Normal Firmware'
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            process = 'non-ARB firmware'
        elif self.extract_mode is ProcessTypes.firmware_less:
            process = 'firmware-less ROM'
        elif self.extract_mode is ProcessTypes.vendor:
            process = 'firmware+vendor'
        else:
            process = 'Unknown'  # This should never happen

        updater_script = template.substitute(
            datetime=self.datetime, host=self.host, process=process, lines=lines
        )
        # correct some updater-script lines that exist in old devices' file
        if '/firmware/image/sec.dat' in updater_script:
            updater_script = updater_script.replace(
                '/firmware/image/sec.dat', '/dev/block/bootdevice/by-name/sec'
            )
        if '/firmware/image/splash.img' in updater_script:
            updater_script = updater_script.replace(
                '/firmware/image/splash.img', '/dev/block/bootdevice/by-name/splash'
            )
        self.update_script = updater_script
        write_text_to_file(f'{str(self._flashing_script_dir)}/updater-script', updater_script)
        # Use modified dynamic_partitions_op_list with resize vendor line only
        if (
            self.extract_mode is ProcessTypes.vendor
            and 'dynamic_partitions_op_list' in updater_script
        ):
            original_dynamic_partitions_list = Path(
                self._tmp_dir / 'dynamic_partitions_op_list'
            ).read_text()
            vendor_resize = re.search(
                r'(resize vendor .*$)', original_dynamic_partitions_list, re.M
            )
            if vendor_resize:
                write_text_to_file(
                    f'{self._tmp_dir!s}/dynamic_partitions_op_list',
                    vendor_resize.group(1),
                )

    def get_payload_devices(self) -> list[str]:
        try:
            metadata = self.extractor.read('META-INF/com/android/metadata').decode()
        except (KeyError, UnicodeDecodeError) as error:
            raise RuntimeError('Payload ROM has no valid OTA metadata!') from error

        properties = dict(line.split('=', 1) for line in metadata.splitlines() if '=' in line)
        if properties.get('ota-type') != 'AB':
            raise RuntimeError('Payload ROM metadata does not declare ota-type=AB!')

        devices = sorted(
            filter(
                None,
                (device.strip() for device in re.split(r'[|,:]', properties.get('pre-device', ''))),
            )
        )
        if not devices or any(not re.fullmatch(r'[A-Za-z0-9_.-]+', device) for device in devices):
            raise RuntimeError('Payload ROM metadata has no valid pre-device!')
        return devices

    def generate_ab_flashing_scripts(self):
        def digest(file: Path) -> str:
            with file.open('rb') as stream:
                return file_digest(stream, 'sha256').hexdigest()

        image_files = list((self._tmp_dir / 'firmware-update').glob('*.img'))
        for file in image_files:
            if not file.stat().st_size:
                file.unlink()
        images = sorted(
            (file.stem, file.stat().st_size, digest(file)) for file in image_files if file.exists()
        )
        if not images:
            raise RuntimeError('No firmware images found to flash!')
        if any(not re.fullmatch(r'[A-Za-z0-9_-]+', partition) for partition, _, _ in images):
            raise RuntimeError('Payload contains an invalid partition name!')
        devices = self.get_payload_devices()
        update_binary_template = ScriptTemplate(
            Path(Path(__file__).parent / 'templates/recovery_ab_update-binary').read_text()
        )
        update_binary = update_binary_template.substitute(
            devices=quote(' '.join(devices)),
            image_check_lines='\n'.join(
                f'check_image {quote(partition)} {digest}' for partition, _, digest in images
            ),
            preflight_lines='\n'.join(
                f'preflight_partition {quote(partition)} {size}' for partition, size, _ in images
            ),
            flash_lines='\n'.join(
                f'flash_partition {quote(partition)} {size} {digest} "$slot"'
                for partition, size, digest in images
            ),
        )
        update_binary_path = self._flashing_script_dir / 'update-binary'
        write_text_to_file(update_binary_path, update_binary)
        update_binary_path.chmod(0o755)

    def generate_flashing_script(self, invalid_files: set[str]):
        """
        Generate update_script or update-binary
        :return:
        """
        if self.uses_payload is True:
            self.generate_ab_flashing_scripts()
        else:
            self.generate_updater_script(invalid_files)

    def make_zip(self) -> str:
        """
        Compress the temporary directory into a zip archive in output directory.

        Also, name it according to process parameters.
        :return:
        """
        out = Path(f'{self._out_dir}/result.zip')
        if self.uses_payload:
            with ZipFile(out, 'w', ZIP_DEFLATED, allowZip64=True) as archive:
                for file in self._tmp_dir.rglob('*'):
                    archive.write(file, file.relative_to(self._tmp_dir))
            try:
                with ZipFile(out) as archive:
                    infos = archive.infolist()
                    names = [info.filename for info in infos]
                    images = [info for info in infos if info.filename.endswith('.img')]
                    if (
                        archive.testzip()
                        or names.count('META-INF/com/google/android/update-binary') != 1
                        or 'META-INF/com/android/metadata' in names
                        or not images
                        or len(images) != len({info.filename for info in images})
                        or any(info.compress_type != ZIP_DEFLATED for info in images)
                    ):
                        raise RuntimeError('Generated firmware archive is invalid!')
            except BadZipFile as error:
                raise RuntimeError('Generated firmware archive is invalid!') from error
        else:
            make_archive(str(out.with_suffix('').absolute()), 'zip', self._tmp_dir)
        if not out.exists():
            raise RuntimeError('Could not create result zip file!')
        if not self.uses_payload:
            codename = extract_codename(self.update_script)
        else:
            file_name = self.extractor.get_file_name()
            codename = extract_payload_codename(file_name)
        zip_prefix = ''
        if self.extract_mode is ProcessTypes.firmware:
            zip_prefix = 'fw'
        elif self.extract_mode is ProcessTypes.non_arb_firmware:
            zip_prefix = 'fw-non-arb'
        elif self.extract_mode is ProcessTypes.firmware_less:
            zip_prefix = 'fw-less'
        elif self.extract_mode is ProcessTypes.vendor:
            zip_prefix = 'fw-vendor'
        else:
            pass  # This should never happen
        zip_name = f'{self._out_dir}/{zip_prefix}_{codename}_{self.extractor.get_file_name()}'
        out.rename(zip_name)
        return zip_name

    def extract(self) -> tuple[set[str], set[str]]:
        """
        Invoke the extract method of extractor object.

        :return: a tuple of a set of valid files to extract and a set of zero length invalid files.
        """
        if hasattr(self.extractor, 'handler') and isinstance(self.extractor.handler, PayloadZip):
            self.uses_payload = True
            self.extractor.prepare()
        self.get_rom_type()
        files_to_extract = self.get_files_list()
        if not files_to_extract or (
            len(files_to_extract) == 2
            and 'updater-script' in str(files_to_extract)
            and 'update-binary' in str(files_to_extract)
        ):
            self.cleanup()
            self.close()
            raise RuntimeError('Nothing found to extract!')
        self.extractor.extract(files_to_extract)
        # Filter out zero length invalid files
        invalid_files = set()
        firmware_update_dir = Path(self._tmp_dir / 'firmware-update')
        if not firmware_update_dir.exists():
            return set(files_to_extract), invalid_files
        for file in firmware_update_dir.iterdir():
            if file.is_file() and file.stat().st_size == 0:
                file.unlink(missing_ok=True)
                invalid_files.add(file.name)
        return set(files_to_extract).difference(invalid_files), invalid_files

    def cleanup(self):
        """
        Cleanup temporary directory and files.

        :return:
        """
        rmtree(self._tmp_dir, ignore_errors=True)

    def close(self):
        """
        Invoke close method of the extractor object.

        :return:
        """
        self.extractor.close()

    def auto(self) -> str:
        """
        Autopilot method for doing everything with a single call.

        This is useful for using this class from a command line interface
         or another application.
        :return: output zip file name as a string.
        """
        try:
            _, invalid_files = self.extract()
            print('Generating flashing script...')
            self.generate_flashing_script(invalid_files)
            print('Creating new zip file..')
            return self.make_zip()
        finally:
            self.cleanup()
            self.close()
