from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Sequence

from xiaomi_flashable_firmware_creator.extractors.handlers.base_handler import (
    BaseHandler,
)


class PayloadError(Exception):
    pass


class PayloadZip(BaseHandler):
    def __init__(self, zip_file_path, tmp_dir, extractor):
        super().__init__(zip_file_path, tmp_dir, extractor)
        self.files: list[str] = []
        self._payload_bin_path: Path | None = None
        self._partitions: set[str] = set()

    def prepare(self) -> List[str]:
        """Extract payload.bin and determine available partitions."""

        payload_bin = self.extractor.extract('payload.bin', self._tmp_dir)
        self._payload_bin_path = Path(payload_bin)

        output = self._run_payload_dumper(['--list', str(self._payload_bin_path)])
        partitions = self._parse_partitions(output.stdout)
        if not partitions:
            raise PayloadError('payload-dumper-go did not return any partitions')

        self._partitions = partitions
        self.files = sorted(f'firmware-update/{name}.img' for name in partitions)
        return self.files

    def extract(self, files_to_extract: List[str]):
        """Extract the requested partitions using payload-dumper-go."""

        if not self._payload_bin_path or not self._payload_bin_path.exists():
            raise PayloadError('payload.bin is missing; call prepare() first')

        requested_files = set(self.files).intersection(set(files_to_extract))
        if not requested_files:
            return

        partition_names = self._to_partition_names(requested_files)

        Path(self._tmp_dir / 'firmware-update').mkdir(parents=True, exist_ok=True)
        args = [
            '--output',
            str(Path(self._tmp_dir / 'firmware-update')),
            '--partitions',
            ','.join(sorted(partition_names)),
            str(self._payload_bin_path),
        ]

        self._run_payload_dumper(args)

        try:
            self._payload_bin_path.unlink()
        finally:  # pragma: no branch - defensive cleanup
            self._payload_bin_path = None

    def _to_partition_names(self, files: Sequence[str]) -> list[str]:
        names: list[str] = []
        for file in files:
            stem = Path(file).stem
            if stem:
                names.append(stem)
        if self._partitions:
            names = [name for name in names if name in self._partitions]
        return names

    @staticmethod
    def _parse_partitions(stdout: str) -> set[str]:
        partitions: set[str] = set()
        capturing = False
        for line in stdout.splitlines():
            if not capturing and line.strip().startswith('Found partitions:'):
                capturing = True
                continue
            if capturing:
                if '(' not in line:
                    break
                entries = [entry.strip() for entry in line.split(',') if entry.strip()]
                for entry in entries:
                    partitions.add(entry.split(' ')[0])
        if not partitions:
            # Fallback to regex in case output format changes slightly
            partitions.update(re.findall(r'\b([A-Za-z0-9_-]+)\s*\(', stdout))
        return partitions

    @staticmethod
    def _payload_dumper_path() -> str:
        binary = shutil.which('payload-dumper-go')
        if not binary:
            raise PayloadError('payload-dumper-go binary not found in PATH')
        return binary

    def _run_payload_dumper(self, args: list[str]) -> subprocess.CompletedProcess:
        binary = self._payload_dumper_path()
        try:
            return subprocess.run(  # noqa: S603,S607 - executed with a trusted binary
                [binary, *args],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:  # pragma: no cover - defensive guard
            output = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            raise PayloadError(f'payload-dumper-go failed: {output}') from exc
