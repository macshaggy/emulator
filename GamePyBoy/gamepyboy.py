import struct
import json
from collections import namedtuple
from pathlib import Path
<<<<<<< HEAD
from instructions import Operand, Instruction
=======
from .instructions import Operand, Instruction
>>>>>>> main


FIELDS = [
  (None, "="),  # "Native" endian.
  (None, 'xxxx'),  # 0x100-0x103 (entrypoint)
  (None, '48x'),  # 0x104-0x133 (nintendo logo)
  ("title", '15s'),  # 0x134-0x142 (cartridge title) (0x143 is shared with the
  # cgb flag)
  ("cgb", 'B'),  # 0x143 (cgb flag)
  ("new_licensee_code", 'H'),  # 0x144-0x145 (new licensee code)
  ("sgb", 'B'),  # 0x146 (sgb `flag)
  ("cartridge_type", 'B'),  # 0x147 (cartridge type)
  ("rom_size", 'B'),  # 0x148 (ROM size)
  ("ram_size", 'B'),  # 0x149 (RAM size)
  ("destination_code", 'B'),  # 0x14A (destination code)
  ("old_licensee_code", 'B'),  # 0x14B (old licensee code)
  ("mask_rom_version", 'B'),  # 0x14C (mask rom version)
  ("header_checksum", 'B'),  # 0x14D (header checksum)
  ("global_checksum", 'H'),  # 0x14E-0x14F (global checksum)
]


CARTRIDGE_HEADER = "".join(format_type for _, format_type in FIELDS)

CartridgeMetadata = namedtuple(
    "CartridgeMetadata",
    [field_name for field_name, _ in FIELDS if field_name is not None],
)


def read_cartridge_metadata(buffer, offset: int = 0x100):
    """
    Unpacks the cartridge metadata from `buffer` at `offset` and
    returns a `CartridgeMetadata` object.
    """
    data = struct.unpack_from(CARTRIDGE_HEADER, buffer, offset=offset)
    return CartridgeMetadata._make(data)


def load_opcodes(file: Path = Path("data/Opcodes.json")) -> dict:
    """
    Reads the opcodes file into a dictionary from `file`. The dictionary
    has codes in two parts `unprefixed` and `cbprefixed`. The first and second
    elements are the prefix codes.
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
