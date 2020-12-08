# owner
Tools to prove ownership of content


To install:	```pip install owner```


# Essentially


```python
from owner import weave, unweave

assert unweave(weave(b'bob and alice')) == b'bob and alice'
```

## What's happening?

Well, here's what's happening by default.

First, a weaver is made...


```python
from owner import HeadWeaver

weaver = HeadWeaver()
```

## weave

When we weave, we get the same original content, but with a bunch of "other junk"...


```python
content = b'--this is where content goes--'
extra_info = b'**optional free-from "extra info goes here: It is meant for ownership and dating info.**'
w = weaver.weave(content, extra_info)
w
```



    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb8\xe8gU\xcc\xc1\n)\xd1\xb0\x1dd\x07\xa4\x90\xbd\xfe\x0f7\xe9\xb5\xcd\xf8\xd7[z\xc5\xeao\xac\x03|8**optional free-from "extra info goes here: It is meant for ownership and dating info.**--this is where content goes--'



## unweave

No fret though, we can unjunk the weave.


```python
unwoven_content = weaver.unweave(w)
assert unwoven_content == content  # see that the unwoven content is the same as the original content
unwoven_content
```




    b'--this is where content goes--'



What does weaving and unweaving do for you?

Well, that's up to you. It's just a means to add some information to some content, within the bytes of the content itself, and be able to still access the original content. 

What you put in the `extra_info` depends on you and your use case. 
The use case we have in mind here is: I want to prove that some content is mine by posting a hash of it on a block-chain. 
But if I just hash the content, only the content is represented, not any other information (such as my name etc.). 
Simple solution to that: Just prepend my name (or any other information) to the raw content.
That's what `extra_info` is.
Ah... but then I need to know where the original content starts. 
That's what `offset` is.
And then we added a `content_hash` to add extra error-correcting abilities. 

Let's now have a look at how the woven bytes are parsed.

## inspecting the parts of the woven


```python
parts = weaver.unweave_parts(w)
parts
```




    UnWovenBaseHeaderWeave(offset=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb8', content_hash=b'\xe8gU\xcc\xc1\n)\xd1\xb0\x1dd\x07\xa4\x90\xbd\xfe\x0f7\xe9\xb5\xcd\xf8\xd7[z\xc5\xeao\xac\x03|8', extra_info=b'**optional free-from "extra info goes here: It is meant for ownership and dating info.**', content=b'--this is where content goes--')




```python
parts._fields
```




    ('offset', 'content_hash', 'extra_info', 'content')



As you see in the print out above, the parts are all given in raw bytes format. 

If you need them to be interpreted you can do so like this:


```python
parts = weaver.unweave_parts(w, interpret_bytes=True)
parts
```




    UnWovenBaseHeaderWeave(offset=184, content_hash='e86755ccc10a29d1b01d6407a490bdfe0f37e9b5cdf8d75b7ac5ea6fac037c38', extra_info=b'**optional free-from "extra info goes here: It is meant for ownership and dating info.**', content=b'--this is where content goes--')



The offset tells us where the content actually starts. Here, we know it starts at the 184th byte.


```python
parts.offset
```




    184



The ``content_hash`` is the sha256 of the original contents, here presented in hex form.


```python
parts.content_hash
```




    'e86755ccc10a29d1b01d6407a490bdfe0f37e9b5cdf8d75b7ac5ea6fac037c38'




```python
parts.extra_info
```




    b'**optional free-from "extra info goes here: It is meant for ownership and dating info.**'




```python
parts.content
```




    b'--this is where content goes--'



## a bit more control on how you get your woven parts 


```python
import json

weaver = HeadWeaver()
content = 'This is some text'
extra_info = {"name": "Thor Whalen", 
              "date": "2013-12-11"}
w = weaver.weave(content.encode(), json.dumps(extra_info).encode())


parts = weaver.unweave_parts(w, interpret_bytes=True, decode_content=True, decode_extra_info=json.loads)
parts
```




    UnWovenBaseHeaderWeave(offset=141, content_hash='2263d8dd95ccfe1ad45d732c6eaaf59b3345e6647331605cb15aae52002dff75', extra_info={'name': 'Thor Whalen', 'date': '2013-12-11'}, content='This is some text')




```python
assert isinstance(parts.extra_info, dict)  # I'm now getting extra_info in the form of a dict
parts.extra_info
```




    {'name': 'Thor Whalen', 'date': '2013-12-11'}




```python
assert isinstance(parts.content, str)  # content is as a str
parts.content
```




    'This is some text'



