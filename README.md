# flash-multiple-esp-devices

## Requirements
  + For Python Requirements check the [requirements.txt](requirements.txt)

## Setup Steps
##### Step 1: Install Python dependencies
+ pip install -r requirements.txt
##### Step 2: Create config.json
+ Add the 'bin_file' value 
  + Use the .bin file name and add it to the directory
+ Add the 'friendly_name' value in config.json
  + This may be the prefix you'd use in a Device Name
+ Example
    ```
    {
      "bin_file": "tasmota-sensors.bin",
      "friendly_name": "EZsalt"
    }
    ```
##### Step 3: .bin file
+ As stated above don't forget to add your .bin file to the directory

## Running Script
```
python flash_loop.py
```
+ This File runs a thread for every COM port available and atttempts to flash the device using the flash_once.py script which uses esptool.py

```
python flash_once.py COM3
```
+ This File takes the COM port as a command line argument to flash

## esptool.py - Modifications
  + Added a return_array to get the esp Object from esptool.py
  + Added the attribute MAC_ADDRESS to the esp Object that is returned
