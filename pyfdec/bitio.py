r"""Exports a BitIO class to read and write bits on streams.

    >>> from io import BytesIO
    >>> stream = BytesIO()
    >>>
    >>> wrapped = BitIO(stream)
    >>> wrapped.write('00')
    0
    >>> wrapped.write('10000')
    0
    >>> wrapped.write([True] * 9)
    2
    >>> wrapped.close()
    >>> stream.getvalue()
    b'!\xff'
    >>>
    >>> stream.seek(0)
    0
    >>> wrapped = BitIO(stream)
    >>> wrapped.read(4)
    bitarray('0010')
    >>> wrapped.read(6)
    bitarray('000111')
    >>> wrapped.read()
    bitarray('111111')
"""


__author__ = 'Gaming32'
__version__ = '1.1.0'


import io
from typing import Sequence

from bitarray import bitarray


class BitIO:
    r"""Wraps an io stream and allows bitarray read and write to that stream.
However, it can only read or write. A new one must be created to do the
other function."""
    __slots__ = ['_readable', '_writable', '_stream', '_buffer']

    def __init__(self, stream:io.RawIOBase):
        self._stream = stream
        self._buffer = bitarray()
        self._readable = None
        self._writable = None

    def readable(self) -> bool:
        """Returns True if this stream is readable (will always be False if a write has occured on it)"""
        if self._readable is None:
            return self._stream.readable()
        return self._readable

    def writable(self) -> bool:
        """Returns True if this stream is writable (will always be False if a read has occured on it)"""
        if self._writable is None:
            return self._stream.writable()
        return self._writable

    def seekable(self) -> bool:
        """Returns True if this stream is seekable (will always be False)"""
        return False

    def seek(self, where, whence=0) -> int:
        """Raises io.UnsupportedOperation('seek')"""
        raise io.UnsupportedOperation('seek')

    def tell(self) -> int:
        """Raises io.UnsupportedOperation('tell')"""
        raise io.UnsupportedOperation('tell')
        return max((self._stream.tell() - 1) * 8 + len(self._buffer), 0)

    def flush(self, flush_wrapped_stream=True):
        """Flushes the buffer to the wrapped stream (this should never have to happen)
If flush_wrapped_stream is True, this also calls self._stream.flush()"""
        if self.writable():
            while len(self._buffer) >= 8:
                towrite, self._buffer = self._buffer[:8], self._buffer[8:]
                self._stream.write(towrite.tobytes())
        if flush_wrapped_stream:
            self._stream.flush()

    def write(self, bits:Sequence[bool]) -> int:
        """Returns the number of BYTES written"""
        if not self.writable():
            raise io.UnsupportedOperation('write')
        self._readable = False

        self._buffer.extend(bits)
        bytes_written = 0
        while len(self._buffer) >= 8:
            towrite, self._buffer = self._buffer[:8], self._buffer[8:]
            self._stream.write(towrite.tobytes())
            bytes_written += 1
        return bytes_written

    def read(self, c=-1) -> bitarray:
        """Reads c bits from the wrapped stream
If c is ommitted or negative, reads all bits from the wrapped stream"""
        if not self.readable():
            raise io.UnsupportedOperation('read')
        self._writable = False

        if c < 0:
            self._buffer.frombytes(self._stream.read())
            return self._buffer
        result, self._buffer = self._buffer[:c], self._buffer[c:]
        c -= len(result)
        bytes_to_read, bits_to_read = divmod(c, 8)
        result.frombytes(self._stream.read(bytes_to_read))
        if bits_to_read:
            self._buffer.frombytes(self._stream.read(1))
            result.extend(self._buffer[:bits_to_read])
            self._buffer = self._buffer[bits_to_read:]
        return result

    def close(self):
        """Calls self.flush(flush_wrapped_stream=False)"""
        self.flush(flush_wrapped_stream=False)

    def __del__(self):
        """Calls self.close()"""
        self.close()

    def __enter__(self):
        """Returns self"""
        return self

    def __exit__(self, *exc_info):
        """Calls self.close()"""
        self.close()


io.IOBase.register(BitIO)


del Sequence


if __name__ == '__main__':
    from io import BytesIO
    stream = BytesIO()
    wrapped = BitIO(stream)
    wrapped.write('00')
    wrapped.write('10000')
    wrapped.write([True] * 9)
    wrapped.close()
    stream.getvalue()
    stream.seek(0)
    wrapped = BitIO(stream)
    wrapped.read(4)
    wrapped.read(6)
    wrapped.read()