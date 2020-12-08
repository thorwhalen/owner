import hashlib
import os
from typing import Union, Callable

DFLT_OFFSET_POINTER_N_BYTES = 64
DFLT_ENCODING = 'utf-8'


def bytes_to_sha256(b: bytes):  # todo: returns string; needs to return bytes
    r"""Compute sha56 of given bytes

    :param b: bytes to compute the sha256 of
    :return: the bytes of the sha256 hash

    >>> bytes_to_sha256(b'bob and alice')
    b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5'

    """
    return hashlib.sha256(b).digest()


def src_to_bytes(src):
    """Gets the bytes of src.
    If src is a string, is assumed to be a filepath.
    If not, asserts src is of the bytes type.
    """
    if isinstance(src, str) and os.path.isfile(src):
        # todo: do it streaming and incremental to be able to handle big files with little RAM footprint
        with open(src, 'rb') as fp:
            src = fp.read()
    assert isinstance(src, bytes), "src needs to be bytes"
    return src


def int_to_bytes(i, n_bytes=64, byteorder='big'):
    r"""

    :param i:
    :param n_bytes:
    :param byteorder:
    :return:

    >>> an_integer = 123456
    >>> b = int_to_bytes(an_integer)
    >>> assert isinstance(b, bytes)
    >>> back_to_int = bytes_to_int(b)
    >>> assert back_to_int == an_integer

    >>> int_to_bytes(7, n_bytes=3)
    b'\x00\x00\x07'
    >>> int_to_bytes(255, n_bytes=3)
    b'\x00\x00\xff'
    >>> int_to_bytes(256, n_bytes=3)
    b'\x00\x01\x00'
    >>> int_to_bytes(256 + 7, n_bytes=3)
    b'\x00\x01\x07'
    """
    assert i < 2 ** (8 * n_bytes), f"too big for {n_bytes} bytes"
    return i.to_bytes(n_bytes, byteorder)


def bytes_to_int(b, byteorder='big'):
    r"""

    :param b:
    :param byteorder:
    :return:

    >>> bytes_to_int(int_to_bytes(123456)) == 123456
    True
    >>> bytes_to_int(b'\x00\x00\x07')
    7
    >>> bytes_to_int(b'\x00\x01\x00')
    256
    >>> assert bytes_to_int(b'\x00\x01\x07') == 256 + 7
    """
    return int.from_bytes(b, byteorder)


assert bytes_to_int(int_to_bytes(123456)) == 123456


def sha256_and_extras_header(content, extra_info: bytes = b''):
    r"""computes sha256 hash of content and contatenation content_hash + extra_info

    >>> sha256_and_extras_header(b'bob and alice', 'extra info'.encode())
    b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5extra info'
    """
    assert isinstance(extra_info, bytes), \
        "extra_info needs to be in bytes. If you specified string s, try entering s.encode() instead."
    content_hash = bytes_to_sha256(content)
    return content_hash + extra_info


def decode_with(x, decoder: Union[str, bool, Callable] = False):
    """Decode ``x`` with specified decoder

    :param x: Input to decode
    :param decoder: How to decode (if at all). Could be:
        bool: If ``False``, leaves ``x`` as is, if ``True`` uses default `bytes.decode`
        str: Taken to be the ``encoding`` param of ``bytes.decode``
        callable: Calls ``decoder(x)``

    """

    if decoder:
        if decoder is True:
            return x.decode()
        elif isinstance(decoder, str):
            return x.decode(decoder)
        elif isinstance(decoder, Callable):
            return decoder(x)
    else:
        return x
