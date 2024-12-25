from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class FileAttributes(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.FileAttributes

    useDirectBlit: bool
    useGPU: bool
    hasMetadata: bool
    actionScript3: bool
    noCrossDomainCaching: bool
    swfRelativeUrls: bool
    useNetwork: bool

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            bits.padding(1)
            useDirectBlit = bits.read_bool()
            useGPU = bits.read_bool()
            hasMetadata = bits.read_bool()
            actionScript3 = bits.read_bool()
            noCrossDomainCaching = bits.read_bool()
            swfRelativeUrls = bits.read_bool()
            useNetwork = bits.read_bool()
            bits.padding(24)
        return cls(
            useDirectBlit,
            useGPU,
            hasMetadata,
            actionScript3,
            noCrossDomainCaching,
            swfRelativeUrls,
            useNetwork,
        )


Tag.register(FileAttributes)
