# NodeMCU REPL

This is a tool to ease the development on the ESP8266 running the NodeMCU
firmware. It is a serial communication client adapted to the NodeMCU's
interpreter plus a file loader.

It features **readline** support (command history, inline editing, tab
completion) and a file **minifier** through
[LuaMinify](https://github.com/stravant/LuaMinify) to reduce the size of
uploaded Lua scripts.

I was constantly alternating between my terminal emulator to monitor the
device and [Luatool](https://github.com/4refr0nt/luatool) to upload files
to it, both of which bind on the serial port and cannot run simultaneously.

## TODO

* Readline
* Minifier
* Pretty printer

## Acknowledgments

Several lines of code were grabbed from
[Luatool](https://github.com/4refr0nt/luatool).
