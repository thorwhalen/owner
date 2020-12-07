import hashlib

def bytes_to_hash(b):  # todo: returns string; needs to return bytes
    return hashlib.sha256(b).digest()

assert (bytes_to_hash(b'bob and alice') 
        == b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5')

def int_to_bytes(i, n_bytes=64, byteorder='big'):
    assert i < 2 ** n_bytes, f"too big for {n_bytes} bytes"
    return (i).to_bytes(n_bytes, byteorder)
    
def bytes_to_int(b, n_bytes=64, byteorder='big'):
    return int.from_bytes(b, byteorder)

assert bytes_to_int(int_to_bytes(123456)) == 123456

def weave(src, extra_info='', offset_pointer_n_bytes=64):  
    """From src (a file or it's bytes), return the same, but with a header with extra info.
    
    Format:
    <content-offset>  # 64 bytes int (byteorder='big') indicating what byte offset content starts at
    <content-hash>  # SHA-256 of the original contents
    <extra-info>  # 0 to 2 ** 64 (or what ever the conent-offset reserved bytes is) bytes to add info
    <content>  # the original content
    """
    if isinstance(src, str) and os.path.isfile(src):
        # todo: do it streaming and incremental to be able to handle big files with little RAM footprint
        with open(src, 'rb') as fp:  
            src = fp.read()
    assert isinstance(src, bytes), "src needs to be bytes"

    extra_info = extra_info.encode()  # todo: params?
    src_hash = bytes_to_hash(src)

    header = src_hash + extra_info
    offset = offset_pointer_n_bytes + len(header)
    header = int_to_bytes(offset, offset_pointer_n_bytes) + header

    return header + src


assert (weave(b'bob and alice') == 
        (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r'
         b'\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5bob and alice')
       )


def unweave(src, assert_content_hash=True, offset_pointer_n_bytes=64):  # todo: specify as hash kind
    """From src (a file or it's bytes), return the same, but with a header with extra info.

    Format:
    <content-offset>  # 64 bytes int (byteorder='big') indicating what byte offset content starts at
    <content-hash>  # SHA-256 of the original contents
    <extra-info>  # 0 to 2 ** 64 (or what ever the conent-offset reserved bytes is) bytes to add info
    <content>  # the original content
    """
    if isinstance(src, str) and os.path.isfile(src):
        # todo: do it streaming and incremental to be able to handle big files with little RAM footprint
        with open(src, 'rb') as fp:  
            src = fp.read()
    assert isinstance(src, bytes), "src needs to be bytes"

    offset = bytes_to_int(src[:offset_pointer_n_bytes])
    src_hash, content = src[offset_pointer_n_bytes:offset], src[offset:]
    
    if assert_content_hash:
        assert src_hash == bytes_to_hash(content)
    
    return content

unweave(weave(b'bob and alice')) == b'bob and alice'