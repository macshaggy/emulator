# Developer Log

### 22 Jan 2022 - 1036 hrs.

This is my first developer log entry. Most code will be on the DEV branch as I update that faster than the MAIN branch.

My reason for this is that the MAIN branch should always have working code, while DEV branch may or may not work. To see the code running start up a REPL (I prefer IPython), and import gamepyboy.py:

    import gamepyboy as gpb

and then load the Opcodes table:

    prefix_ops, regular_ops = gpb.load_opcodes()

The opcodes will be used later as I'm just now starting the next page on the site, ["Game Boy Emulator: Writing the Z80 Disassembler"](https://www.inspiredpython.com/course/game-boy-emulator/game-boy-emulator-writing-the-z80-disassembler). That is the next steps into the project. And I'll write any problems/solutions that I may come across here in this log.
