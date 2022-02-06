from pathlib import Path
from context import decoder

if __name__ == '__main__':
    opcode_file = Path('GamePyBoy/data/Opcodes.json')
    game_file = Path('GamePyBoy/storage/snake.gb')

    if opcode_file.exists() & game_file.exists():
        dec = decoder.Decoder.create(
                opcode_file=opcode_file,
                data=game_file.read_bytes(),
                address=0)

        _, instruction = dec.decode(0x204)
        print(instruction)
    else:
        print(f'opcode exists: {opcode_file.exists()}')
        print(f'  game exists: {game_file.exists()}')
