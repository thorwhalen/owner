# owner.base

Base `Owner` machinery: wrap a store so that values are written with owner-checked headers.

### Functions

| [`unweave`](#owner.base.unweave)(src, \*\*weaver_kwargs)                  | From src (a file or it's bytes), return the same, but with a header with extra info.   |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [`weave`](#owner.base.weave)(src[, extra_info, offset_pointer_n_bytes]) | From src (a file or it's bytes), return the same, but with a header with extra info.   |

### Classes

| [`HeadWeaver`](#owner.base.HeadWeaver)([offset_pointer_n_bytes])              | HeadWeaver will weave some information in some contents in a header, and allow you to parse it back out.   |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| [`UnWovenBaseHeaderWeave`](#owner.base.UnWovenBaseHeaderWeave)(offset, content_hash, ...) |                                                                                                            |

### *class* owner.base.HeadWeaver(offset_pointer_n_bytes=64)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

HeadWeaver will weave some information in some contents in a header, and allow you to parse it back out.

The format is:

```default
<header><content>
```

where

```default
<header> :=  <content-offset><content-hash><extra-info>
```

More info:
<content-offset>  # 64 bytes int (byteorder=’big’) indicating what byte offset content starts at
<content-hash>  # 32 bytes: SHA-256 of the original contents
<extra-info>  # 0 to 2 \*\* 64 - 64 - 32) (if offset_pointer_n_bytes=64) bytes to add info
<content>  # the original content

#### *static* content_and_extra_info_2_header(content, extra_info=b'')

computes sha256 hash of content and contatenation content_hash + extra_info

```pycon
>>> sha256_and_extras_header(b'bob and alice', 'extra info'.encode())
b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5extra info'
```

#### unweave_parts(src, interpret_bytes=False, decode_extra_info=False, decode_content=False)

Get the four parts of a woven source.

* **Parameters:**
  * **src** ([`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes)) – Source (filepath or bytes) to unweaver
  * **interpret_bytes** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to intepret the raw bytes or not
    If True, the offset will be given as an int, the content_hash in hex.
    This also enables decode_extra_info and decode_content to be used to whether and how how to decode these.
  * **decode_extra_info** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)]) – Whether (and how) to decode extra_info.
  * **decode_content** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)]) – Whether (and how) to decode content.
* **Returns:**
  A named tuple of the four parts of the woven source

### *class* owner.base.UnWovenBaseHeaderWeave(offset, content_hash, extra_info, content)

Bases: [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)

#### content

Alias for field number 3

#### content_hash

Alias for field number 1

#### extra_info

Alias for field number 2

#### offset

Alias for field number 0

### owner.base.unweave(src, \*\*weaver_kwargs)

From src (a file or it’s bytes), return the same, but with a header with extra info.

```pycon
>>> assert unweave(weave(b'bob and alice')) == b'bob and alice'
```

### owner.base.weave(src, extra_info=b'', offset_pointer_n_bytes=64)

From src (a file or it’s bytes), return the same, but with a header with extra info.

Format:
<content-offset>  # 64 bytes int (byteorder=’big’) indicating what byte offset content starts at
<content-hash>  # 32 bytes: SHA-256 of the original contents
<extra-info>  # 0 to 2 \*\* 64 - 64 - 32) (if offset_pointer_n_bytes=64) bytes to add info
<content>  # the original content

```pycon
>>> assert (weave(b'--this is where content goes--', b'**here is some extra info, like who the owners are**') ==
...         (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
...          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
...          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x94\xe8gU\xcc\xc1\n)\xd1\xb0\x1dd\x07\xa4\x90'
...          b'\xbd\xfe\x0f7\xe9\xb5\xcd\xf8\xd7[z\xc5\xeao\xac\x03|8'
...          b'**here is some extra info, like who the owners are**'
...          b'--this is where content goes--')
...         )
>>>
```
