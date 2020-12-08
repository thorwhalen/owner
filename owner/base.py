from collections import namedtuple
from typing import Union, Callable

from owner.util import (
    sha256_and_extras_header, DFLT_OFFSET_POINTER_N_BYTES,
    src_to_bytes, int_to_bytes, bytes_to_int,
    decode_with, bytes_to_sha256)

UnWovenBaseHeaderWeave = namedtuple('UnWovenBaseHeaderWeave',
                                    field_names=('offset', 'content_hash', 'extra_info', 'content'))


class HeadWeaver:
    """HeadWeaver will weave some information in some contents in a header, and allow you to parse it back out.

    The format is:

    ::

        <header><content>

    where

    ::

        <header> :=  <content-offset><content-hash><extra-info>

    More info:
    <content-offset>  # 64 bytes int (byteorder='big') indicating what byte offset content starts at
    <content-hash>  # 32 bytes: SHA-256 of the original contents
    <extra-info>  # 0 to 2 ** 64 - 64 - 32) (if offset_pointer_n_bytes=64) bytes to add info
    <content>  # the original content
    """
    hash_n_bytes = 32
    content_and_extra_info_2_header = staticmethod(sha256_and_extras_header)
    dflt_encoding = 'utf-8'

    def __init__(self, offset_pointer_n_bytes=DFLT_OFFSET_POINTER_N_BYTES):
        self.offset_pointer_n_bytes = offset_pointer_n_bytes
        self._extra_info_pointer = self.offset_pointer_n_bytes + self.hash_n_bytes

    def header_with_offset_pointer(self, src, extra_info: bytes = b''):
        src = src_to_bytes(src)
        header = self.content_and_extra_info_2_header(src, extra_info)
        offset_pointer_bytes = int_to_bytes(self.offset_pointer_n_bytes + len(header))
        return offset_pointer_bytes + header  # return header with offset_pointer prepended

    def weave(self, src, extra_info: bytes = b''):
        src = src_to_bytes(src)
        return self.header_with_offset_pointer(src, extra_info) + src

    def unweave_parts(self,
                      src: bytes,
                      interpret_bytes: bool = False,
                      decode_extra_info: Union[str, bool, Callable] = False,
                      decode_content: Union[str, bool, Callable] = False,
                      ):
        """Get the four parts of a woven source.

        :param src: Source (filepath or bytes) to unweaver
        :param interpret_bytes: Whether to intepret the raw bytes or not
            If True, the offset will be given as an int, the content_hash in hex.
            This also enables decode_extra_info and decode_content to be used to whether and how how to decode these.
        :param decode_extra_info: Whether (and how) to decode extra_info.
        :param decode_content: Whether (and how) to decode content.
        :return: A named tuple of the four parts of the woven source

        """

        src = src_to_bytes(src)
        offset = src[:self.offset_pointer_n_bytes]
        offset_int = bytes_to_int(offset)

        content = src[offset_int:]
        content_hash = src[self.offset_pointer_n_bytes:self._extra_info_pointer]
        extra_info = src[self._extra_info_pointer:offset_int]

        if interpret_bytes:
            offset = offset_int
            content_hash = content_hash.hex()
            content = decode_with(content, decode_content)
            extra_info = decode_with(extra_info, decode_extra_info)
        else:
            assert (not decode_extra_info and not decode_content), \
                f"decode_extra_info and decode_content must be False if interpret_bytes is False"

        return UnWovenBaseHeaderWeave(offset=offset, content_hash=content_hash, extra_info=extra_info, content=content)

    def unweave(self, src, assert_content_hash=True):
        unwoven = self.unweave_parts(src, interpret_bytes=False)

        if assert_content_hash:
            assert unwoven.content_hash == bytes_to_sha256(unwoven.content)

        return unwoven.content


def weave(src, extra_info=b'', offset_pointer_n_bytes=64):
    r"""From src (a file or it's bytes), return the same, but with a header with extra info.

    Format:
    <content-offset>  # 64 bytes int (byteorder='big') indicating what byte offset content starts at
    <content-hash>  # 32 bytes: SHA-256 of the original contents
    <extra-info>  # 0 to 2 ** 64 - 64 - 32) (if offset_pointer_n_bytes=64) bytes to add info
    <content>  # the original content

    >>> assert (weave(b'--this is where content goes--', b'**here is some extra info, like who the owners are**') ==
    ...         (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ...          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ...          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x94\xe8gU\xcc\xc1\n)\xd1\xb0\x1dd\x07\xa4\x90'
    ...          b'\xbd\xfe\x0f7\xe9\xb5\xcd\xf8\xd7[z\xc5\xeao\xac\x03|8'
    ...          b'**here is some extra info, like who the owners are**'
    ...          b'--this is where content goes--')
    ...         )
    >>>
    """
    return HeadWeaver(offset_pointer_n_bytes=offset_pointer_n_bytes).weave(src, extra_info)


def unweave(src, **weaver_kwargs):  # todo: specify as hash kind
    """From src (a file or it's bytes), return the same, but with a header with extra info.

    >>> assert unweave(weave(b'bob and alice')) == b'bob and alice'

    """
    return HeadWeaver(**weaver_kwargs).unweave(src)
