"""This module provides ProcessTypes and ZipTypes classes that handle some \
type checks of the tool process."""

from enum import Enum, auto


class ProcessTypes(Enum):
    """
    A process type enum that defines the type of the current run process.

    Values are firmware, non_arb_firmware, firmware_less and vendor.
    """

    firmware = auto()
    non_arb_firmware = auto()
    firmware_less = auto()
    vendor = auto()


class ZipTypes(Enum):
    """
    An enum that represents supported zip ROM types.

    Values are qcom for Qualcomm devices' ROMs and mtk for Mediatek devices' ROMs.
    """

    qcom = auto()
    mtk = auto()
