# NodeMCU REPL

This is a tool to ease the development on the ESP8266 running the NodeMCU
firmware. It is a serial communication client adapted to the NodeMCU's
interpreter plus a file loader.

It features **readline**-like support (command history, inline input editing,
syntax highlighting) thanks to
[Prompt toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)
and makes use of
[LuaMinify](https://github.com/stravant/LuaMinify)
file **minifier** to reduce the size of uploaded Lua scripts.

I was constantly alternating between my terminal emulator to monitor the
device and [Luatool](https://github.com/4refr0nt/luatool) to upload files
to it, both of which bind on the serial port and cannot run simultaneously.

## TODO

* Autocompletion of NodeMCU API
* Minifier
* Pretty printer (for tables at least)

## Acknowledgments

Several lines of code were grabbed from
[Luatool](https://github.com/4refr0nt/luatool).
