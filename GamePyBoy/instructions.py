from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Operand:

    immediate: bool
    name: str
    bytes: int
    value: int | None
    adjust: Literal["+", "-"] | None

    def create(self, value):
        return Operand(immediate=self.immediate,
                       name=self.name,
                       bytes=self.bytes,
                       value=value,
                       adjust=self.adjust)

    def copy(self, value):
        return Operand(immediate=self.immediate,
                       name=self.name,
                       bytes=self.bytes,
                       value=value,
                       adjust=self.adjust)

    def print(self):
        if self.adjust is None:
            adjust = ""
        else:
            adjust = self.adjust

        if self.value is not None:
            if self.bytes is not None:
                val = hex(self.value)
            else:
                val = self.value

            v = val
        else:
            v = self.name

        v = v + adjust

        if self.immediate:
            return v

        return f'({v})'


@dataclass
class Instruction:

    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

    def create(self, operands):
        return Instruction(opcode=self.opcode,
                           immediate=self.immediate,
                           operands=operands,
                           cycles=self.cycles,
                           bytes=self.bytes,
                           mnemonic=self.mnemonic)

    def copy(self, operands):
        return Instruction(opcode=self.opcode,
                           immediate=self.immediate,
                           operands=operands,
                           cycles=self.cycles,
                           bytes=self.bytes,
                           mnemonic=self.mnemonic)

    def print(self):
        ops = ', '.join(op.print() for op in self.operands)
        s = f"{self.mnemonic:<8} {ops}"

        if self.comment:
            s = s + f" ; {self.comment:<10}"

        return s
