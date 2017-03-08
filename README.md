# NodeMCU REPL

This is a tool to ease the development on the ESP8266 running the
[NodeMCU firmware](https://github.com/nodemcu/nodemcu-firmware).
It is a serial communication client adapted to the NodeMCU's
interpreter plus a file loader.

It features **readline**-like support: command history, inline input editing,
syntax highlighting.

I was constantly alternating between my terminal emulator to monitor the
device and [Luatool](https://github.com/4refr0nt/luatool) to upload files
to it, both of which bind on the serial port and cannot run simultaneously.
NodeMCU REPL addresses this issue in less than 150 lines of code.

## Requirements

* Python 3
* [pySerial](https://github.com/pyserial/pyserial)
* [Prompt toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)

If in need of multiple versions of Python I could not recommend
you more [pyenv](https://github.com/pyenv/pyenv).

For installing Python modules the preferred way is through
[pip](https://pip.pypa.io/en/stable) or just use you system's
package manager.

## Installing

Clone/download this repo, use the script. You will need root
privileges or to belong to the `uucp` group.

Also `chmod +x nodemcu-repl/repl.py` and
`export PATH=$PATH:~/nodemcu-repl` if you want the
touch and feel of a command.

## Using

```sh
$ python repl.py --port /dev/ttyUSB0 --baud 115200
```

**Port** and **baud** are optional and default to the aforementioned values.

### Dot commands

**Upload** a local file to the device; it will be stored with the same name.

```lua
> .copy '/path/to/init.lua'
```

**List** size and files stored in the device.

```Lua
> .list
  30 init.lua
 100 main.lua
```

For other actions related to files like **delete** or **rename**,
use the NodeMCU API.

### Inspecting

NodeMCU interpreter does not print evaluated statements unless otherwise
stated. There is a Lua trick that will prevent you from writing `print()`
everytime, just prefix an equals sign, this way:

```lua
> =wifi.sta.status()
5
```

### Important

NodeMCU REPL will disable the UART module echo at start and will re-enable
at exit. If a disconnection happens in-between this will not occur.
In that case, you can re-start the REPL and try to exit normally.

## TODO

* Autocompletion of NodeMCU API.
* Human-readable representation of Lua tables
([see this](http://lua-users.org/wiki/TableSerialization)).
* Make use of [LuaMinify](https://github.com/stravant/LuaMinify)
file **minifier** to reduce the size of uploaded Lua scripts.
Harder than expected as it needs a revamp. Meanwhile, why not to strip
comments?

* Buffer overflow exception.
* UTF-8 decoding error.

## Acknowledgments

Ideas and lines of code were borrowed from
[Luatool](https://github.com/4refr0nt/luatool).
