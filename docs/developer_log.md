# Developer Log

### 22 Jan 2022 - 1036 hrs.

This is my first developer log entry. Most code will be on the DEV branch as I update that faster than the MAIN branch.

My reason for this is that the MAIN branch should always have working code, while DEV branch may or may not work. To see the code running start up a REPL (I prefer IPython), and import gamepyboy.py:

    import gamepyboy as gpb

and then load the Opcodes table:

    prefix_ops, regular_ops = gpb.load_opcodes()

The opcodes will be used later as I'm just now starting the next page on the site, ["Game Boy Emulator: Writing the Z80 Disassembler"](https://www.inspiredpython.com/course/game-boy-emulator/game-boy-emulator-writing-the-z80-disassembler). That is the next steps into the project. And I'll write any problems/solutions that I may come across here in this log.

### 26 Jane 2022 - 1050 hrs.

Removed iPython from pyproject.toml. After consideration this is not a part of the project. It is a tool that I prefer to use but it shouldn't be a requirement to run the emulator.

Doing research on reading the cartridge data. Cartridge header is can be read but now need to process the header, and the rest of the ROM. I will update when I have completed reading the end of the ROM into memory.
### 4 Feb 2022 - 1632 hrs.

Well, I finally figured out that the tests folder shouldn't be buried within the game directory. There were imports that had to be corrected in GamePyBoy/__init__.py so that pytest and hypothesis could find the correct files and conduct the test. It was successful as now the project has pass the current test.

### 6 Feb 2022 - 1611 hrs.

The decoder work is essential for understanding & creating the emulato of the Z80 cpu. (Per the web article this is not entirely correct).

The data section of the decoder is just a generic bytestring and will be replaced with the emulator's memory banks.

#### 1752 hrs.

I think I have the decoder working. I couldn't use the example given in the article as the gamefile isn't the same exact one. But I've read a different location and pulled just the one byte and compared it to the regular opcode and it is identical. So, I now know that decode and read are working in the manner expected. ```test_decoder.py``` should be run like any python file from the root directory and not with pytest (yet).

### 13 Feb 2022 - 1213 hrs.

Whew, I was having issues with testing and running the program due to circular imports and relative imports bs. I finally figured it out with a context.py file for the testing and everything is run from the emulator directory instead of the GamePyBoy directory.

The directory structure is now pretty good.

#### 1240 hrs.

Well, that was quick to get the disassembler working. In order to test and run everything make sure that you are in the emulator directory. You will need to do a couple of things. First you will need to import Path from pathlib that is for the decoder. Then import sys and prefix sys.path with the GamePyBoy directory. Next import gamepyboy and create the decorder. One the decoder is created pass that to gamepyboy.disassemble, the starting point which should be 0x150 and the # of lines. You should get what looks like the assembly of the game file.
