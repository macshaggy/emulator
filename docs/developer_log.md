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
