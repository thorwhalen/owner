# owner.util

Utilities for owner: hashing and header helpers.

### Functions

| [`bytes_to_int`](#owner.util.bytes_to_int)(b[, byteorder])                    |                                                                             |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [`bytes_to_sha256`](#owner.util.bytes_to_sha256)(b)                              | Compute sha56 of given bytes                                                |
| [`decode_with`](#owner.util.decode_with)(x[, decoder])                       | Decode `x` with specified decoder                                           |
| [`int_to_bytes`](#owner.util.int_to_bytes)(i[, n_bytes, byteorder])           |                                                                             |
| [`sha256_and_extras_header`](#owner.util.sha256_and_extras_header)(content[, extra_info]) | computes sha256 hash of content and contatenation content_hash + extra_info |
| [`src_to_bytes`](#owner.util.src_to_bytes)(src)                               | Gets the bytes of src.                                                      |

### owner.util.bytes_to_int(b, byteorder='big')

* **Parameters:**
  * **b**
  * **byteorder**
* **Returns:**

```pycon
>>> bytes_to_int(int_to_bytes(123456)) == 123456
True
>>> bytes_to_int(b'\x00\x00\x07')
7
>>> bytes_to_int(b'\x00\x01\x00')
256
>>> assert bytes_to_int(b'\x00\x01\x07') == 256 + 7
```

### owner.util.bytes_to_sha256(b)

Compute sha56 of given bytes

* **Parameters:**
  **b** ([`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes)) – bytes to compute the sha256 of
* **Returns:**
  the bytes of the sha256 hash

```pycon
>>> bytes_to_sha256(b'bob and alice')
b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5'
```

### owner.util.decode_with(x, decoder=False)

Decode `x` with specified decoder

* **Parameters:**
  * **x** – Input to decode
  * **decoder** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)]) – How to decode (if at all). Could be:
    bool: If `False`, leaves `x` as is, if `True` uses default `bytes.decode`
    str: Taken to be the `encoding` param of `bytes.decode`
    callable: Calls `decoder(x)`

### owner.util.int_to_bytes(i, n_bytes=64, byteorder='big')

* **Parameters:**
  * **i**
  * **n_bytes**
  * **byteorder**
* **Returns:**

```pycon
>>> an_integer = 123456
>>> b = int_to_bytes(an_integer)
>>> assert isinstance(b, bytes)
>>> back_to_int = bytes_to_int(b)
>>> assert back_to_int == an_integer
```

```pycon
>>> int_to_bytes(7, n_bytes=3)
b'\x00\x00\x07'
>>> int_to_bytes(255, n_bytes=3)
b'\x00\x00\xff'
>>> int_to_bytes(256, n_bytes=3)
b'\x00\x01\x00'
>>> int_to_bytes(256 + 7, n_bytes=3)
b'\x00\x01\x07'
```

### owner.util.sha256_and_extras_header(content, extra_info=b'')

computes sha256 hash of content and contatenation content_hash + extra_info

```pycon
>>> sha256_and_extras_header(b'bob and alice', 'extra info'.encode())
b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5extra info'
```

### owner.util.src_to_bytes(src)

Gets the bytes of src.
If src is a string, is assumed to be a filepath.
If not, asserts src is of the bytes type.
