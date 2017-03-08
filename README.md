# NodeMCU REPL

This is a tool to ease the development on the ESP8266 running the NodeMCU
firmware. It is a serial communication client adapted to the NodeMCU's
interpreter plus a file loader.

It features **readline**-like support: command history, inline input editing,
syntax highlighting.

I was constantly alternating between my terminal emulator to monitor the
device and [Luatool](https://github.com/4refr0nt/luatool) to upload files
to it, both of which bind on the serial port and cannot run simultaneously.

## Requirements

* Python 3
* [pySerial](https://github.com/pyserial/pyserial)
* [Prompt toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)

If need multiple versions of Python I could not recommend
you more [pyenv](https://github.com/pyenv/pyenv).

For installing Python modules the preferred way is through
[pip](https://pip.pypa.io/en/stable).

## Installing

Clone this repo, use the script.

Also `chmod +x nodemcu-repl/repl.py` and
`export PATH=$PATH:~/nodemcu-repl` if you want to.

## Using

```sh
$ python repl.py
```

**Upload** a local file to the device; it will be stored with the same name.

```lua
> .copy '/path/to/file'
```

**List** files in the device.

```Lua
> .list
```

For other actions related to files like **delete** or **rename**,
use the NodeMCU API.

NodeMCU interpreter does not print evaluated statements unless otherwise
stated. There is a Lua trick that will prevent you from writing `print()`
everytime, just prefix an equals sign like this:

```lua
> =wifi.sta.status()
5
```

## TODO

* Autocompletion of NodeMCU API.
* Human-readable representation of Lua tables
([see this](http://lua-users.org/wiki/TableSerialization)).
* Make use of [LuaMinify](https://github.com/stravant/LuaMinify)
file **minifier** to reduce the size of uploaded Lua scripts.
Harder than expected as it needs a revamp. Meanwhile, why not to strip
comments?

## Acknowledgments

Ideas and lines of code were borrowed from
[Luatool](https://github.com/4refr0nt/luatool).
