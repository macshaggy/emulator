import sys
import json
from dataclasses import dataclass
from pathlib import Path
from instructions import Instruction, Operand


def load_opcodes(file: Path) -> dict:
    """Load the opcodes file and parse into two dicts
    Args:
        file (Path, optional): [Path obj representing the file].
    Returns:
        dict: [returns the parsed json file opcodes.]
    """
    def _get_operands(operands_list: list) -> list:
        op_list = []
        for operand in operands_list:
            name = operand.get('name')
            immediate = operand.get('immediate')
            bytes = operand.get('bytes')
            value = operand.get('value')
            adjust = operand.get('adjust')
            op_list.append(Operand(immediate=immediate,
                                   name=name,
                                   bytes=bytes,
                                   value=value,
                                   adjust=adjust))
        return op_list

    def _get_opcodes(opcodes_json: dict) -> dict:
        opcodes_dict = {}
        for key in list(opcodes_json.keys()):
            opcode = int(key, base=16)
            operands = _get_operands(opcodes_json[key]["operands"])
            immediate = opcodes_json[key].get("immediate")
            cycles = opcodes_json[key].get("cycles")
            bytes = opcodes_json[key].get("bytes")
            mnemonic = opcodes_json[key].get("mnemonic")
            comment = opcodes_json[key].get("comment")
            opcodes_dict[opcode] = Instruction(opcode=opcode,
                                               immediate=immediate,
                                               operands=operands,
                                               cycles=cycles,
                                               bytes=bytes,
                                               mnemonic=mnemonic,
                                               comment=comment)
        return opcodes_dict

    opcodes_file = json.load(file.open())
    prefix_json, reg_json = opcodes_file['cbprefixed'],\
        opcodes_file['unprefixed']

    return _get_opcodes(prefix_json), _get_opcodes(reg_json)


@dataclass
class Decoder:

    data: bytes
    address: int
    prefixed_instructions: dict
    instructions: dict

    @classmethod
    def create(cls, opcode_file: Path, data: bytes, address: int = 0):
        """Loads the opcodes from the opcode file.

        Args:
            opcode_file (Path): [Path obj representing the file.]
            data (bytes): [data to be decoded]
            address (int, optional): [last position known]. Defaults to 0.
        """
        prefixed, regular = load_opcodes(opcode_file)

        return cls(
            prefixed_instructions=prefixed,
            instructions=regular,
            data=data,
            address=address,
        )

    def read(self, address: int, count: int = 1):
        """Reads `count` bytes starting from `address`.

        Args:
            address (int): [starting address]
            count (int, optional): [number of bytes to read]. Defaults to 1.

        Returns:

        """
        if 0 <= address + count <= len(self.data):
            v = self.data[address: address + count]

            return int.from_bytes(v, sys.byteorder)
        else:
            raise IndexError(f'{address=}+{count=} is out of range.')

    def decode(self, address: int):
        """Decodes the instruction at `address`.

        Args:
            address (int): [instruction]

        Returns:
            address (int): [instruction]
            decoded_instruction: [copy of instruction from opcodes dict]
        """
        opcode = None
        decoded_instruction = None
        opcode = self.read(address)
        address += 1

        # 0xCB is a special prefix instruction. Read from
        # prefixed_instructions instead and increment address
        if opcode == 0xCB:
            opcode = self.read(address)
            address += 1
            instruction = self.prefixed_instructions[opcode]
        else:
            instruction = self.instructions[opcode]

        new_operands = []
        for operand in instruction.operands:
            if operand.bytes is not None:
                value = self.read(address, operand.bytes)
                address += operand.bytes
                new_operands.append(operand.copy(value))
            else:
                # No bytes; that means it's not a memory address
                new_operands.append(operand)

        decoded_instruction = instruction.copy(operands=new_operands)

        return address, decoded_instruction
