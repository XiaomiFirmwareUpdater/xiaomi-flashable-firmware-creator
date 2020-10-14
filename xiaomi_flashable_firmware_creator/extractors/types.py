from enum import Enum, auto


class ProcessTypes(Enum):
    firmware = auto()
    non_arb_firmware = auto()
    firmware_less = auto()
    vendor = auto()


class ZipTypes(Enum):
    qcom = auto()
    mtk = auto()
