"""
Tools to prove ownership of content
"""
from owner.util import bytes_to_sha256, src_to_bytes, int_to_bytes, bytes_to_int, decode_with
from owner.base import HeadWeaver, UnWovenBaseHeaderWeave, weave, unweave

assert unweave(weave(b'bob and alice')) == b'bob and alice'
