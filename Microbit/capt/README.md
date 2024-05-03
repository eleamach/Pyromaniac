# Micro:bit capt

## Author:
- Elea MACHILLOT

## Microbit program

The present program main.cpp read a json from serial, encrypt, and send it through radio :
- Read from serial a json
- When data = 14 (because we use an encryption function with max 16 char) it encrypt data and add a string "+*_*+".
- This continue until it find "}" wich is the end of our json.
- Then, it takes the whole data (1st part encrypted, "+*_*+", last part encrypted) 
- Finally, it is send through radio to another microbit.


## Overview

The micro:bit runtime provides an easy to use environment for programming the BBC micro:bit in the C/C++ language, written by Lancaster University. It contains device drivers for all the hardware capabilities of the micro:bit, and also a suite of runtime mechanisms to make programming the micro:bit easier and more flexible. These range from control of the LED matrix display to peer-to-peer radio communication and secure Bluetooth Low Energy services. The micro:bit runtime is proudly built on the ARM mbed and Nordic nrf51 platforms.

In addition to supporting development in C/C++, the runtime is also designed specifically to support higher level languages provided by our partners that target the micro:bit. It is currently used as a support library for all the languages on the BBC www.microbit.co.uk website, including Microsoft Block, Microsoft TouchDevelop, Code Kingdoms JavaScript and Micropython languages.

## Links

[micro:bit runtime docs](http://lancaster-university.github.io/microbit-docs/) | [microbit-dal](https://github.com/lancaster-university/microbit-dal) |  [uBit](https://github.com/lancaster-university/microbit)

## Build Environments

| Build Environment | Documentation |
| ------------- |-------------|
| ARM mbed online | http://lancaster-university.github.io/microbit-docs/online-toolchains/#mbed |
| yotta  | http://lancaster-university.github.io/microbit-docs/offline-toolchains/#yotta |

##  microbit-dal Configuration

The DAL also contains a number of compile time options can be modified. A full list and explanation
can be found in our [documentation](http://lancaster-university.github.io/microbit-docs/advanced/#compile-time-options-with-microbitconfigh).

Alternately, `yotta` can be used to configure the dal regardless of module/folder structure, through providing a
`config.json` in this directory.

Here is an example of `config.json` with all available options configured:
```json
{
    "microbit-dal":{
        "bluetooth":{
            "enabled": 1,
            "pairing_mode": 1,
            "private_addressing": 0,
            "open": 0,
            "whitelist": 1,
            "advertising_timeout": 0,
            "tx_power": 0,
            "dfu_service": 1,
            "event_service": 1,
            "device_info_service": 1
        },
        "reuse_sd": 1,
        "default_pullmode":"PullDown",
        "gatt_table_size": "0x300",
        "heap_allocator": 1,
        "nested_heap_proportion": 0.75,
        "system_tick_period": 6,
        "system_components": 10,
        "idle_components": 6,
        "use_accel_lsb": 0,
        "min_display_brightness": 1,
        "max_display_brightness": 255,
        "display_scroll_speed": 120,
        "display_scroll_stride": -1,
        "display_print_speed": 400,
        "panic_on_heap_full": 1,
        "debug": 0,
        "heap_debug": 0,
        "stack_size":2048,
        "sram_base":"0x20000008",
        "sram_end":"0x20004000",
        "sd_limit":"0x20002000",
        "gatt_table_start":"0x20001900"
    }
}
```
##  Debug on Visual Studio Code (Windows)

1. build sample. You can build "HELLO WORLD! :)" program.
2. Copy microbit-samples\build\bbc-microbit-classic-gcc\source\microbit-samples-combined.hex to micro:bit.
3. Launch the Visual Studio Code
4. File -> Open Folder... and select "microbit-samples" folder.
5. Set break point to "main()" function.
6. View -> Debug (Ctrl + Shift + D)
7. Debug -> Start Debugging (F5)

![Debug on Visual Studio Code](/debugOnVisualStudioCode.gif)

## BBC Community Guidelines

[BBC Community Guidelines](https://www.microbit.co.uk/help#sect_cg)
