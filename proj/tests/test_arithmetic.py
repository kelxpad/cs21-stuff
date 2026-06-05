import sys
from pathlib import Path

import pytest

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import CPU, OPCODES, Reg, WORD_MASK


def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def cpu_with_instruction(op1, op2, opcode, pc=0):
    memory = [0] * 65536
    memory[pc] = instruction_word(op1, op2, opcode)
    cpu = CPU(memory, 0)
    cpu.regs[Reg.PC] = pc
    return cpu


def execute(cpu, handler):
    decoded = cpu.decode()
    handler(decoded)


def test_set_register_from_register():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["set"])
    cpu.regs[Reg.GA] = 0x1111
    cpu.regs[Reg.GB] = 0xBEEF

    execute(cpu, cpu.execute_set)

    assert cpu.regs[Reg.GA] == 0xBEEF
    assert cpu.regs[Reg.GB] == 0xBEEF


def test_set_register_from_memory():
    cpu = cpu_with_instruction(0x00, 0x09, OPCODES["set"])
    cpu.regs[Reg.GB] = 300
    cpu.memory[300] = 0xCAFE

    execute(cpu, cpu.execute_set)

    assert cpu.regs[Reg.GA] == 0xCAFE


def test_set_memory_from_register():
    cpu = cpu_with_instruction(0x08, 0x01, OPCODES["set"])
    cpu.regs[Reg.GA] = 300
    cpu.regs[Reg.GB] = 0x1234

    execute(cpu, cpu.execute_set)

    assert cpu.memory[300] == 0x1234


def test_add_register_register_wraps_to_word():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["add"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_add)

    assert cpu.regs[Reg.GA] == 0x0001


def test_add_register_memory():
    cpu = cpu_with_instruction(0x00, 0x09, OPCODES["add"])
    cpu.regs[Reg.GA] = 0x0010
    cpu.regs[Reg.GB] = 300
    cpu.memory[300] = 0x0020

    execute(cpu, cpu.execute_add)

    assert cpu.regs[Reg.GA] == 0x0030


def test_add_memory_register():
    cpu = cpu_with_instruction(0x08, 0x01, OPCODES["add"])
    cpu.regs[Reg.GA] = 300
    cpu.regs[Reg.GB] = 0x0003
    cpu.memory[300] = 0x0004

    execute(cpu, cpu.execute_add)

    assert cpu.memory[300] == 0x0007


def test_sub_register_register_wraps_to_word():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["sub"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_sub)

    assert cpu.regs[Reg.GA] == WORD_MASK


def test_sub_register_memory():
    cpu = cpu_with_instruction(0x00, 0x09, OPCODES["sub"])
    cpu.regs[Reg.GA] = 0x0030
    cpu.regs[Reg.GB] = 300
    cpu.memory[300] = 0x0010

    execute(cpu, cpu.execute_sub)

    assert cpu.regs[Reg.GA] == 0x0020


def test_sub_memory_register():
    cpu = cpu_with_instruction(0x08, 0x01, OPCODES["sub"])
    cpu.regs[Reg.GA] = 300
    cpu.regs[Reg.GB] = 0x0004
    cpu.memory[300] = 0x0007

    execute(cpu, cpu.execute_sub)

    assert cpu.memory[300] == 0x0003


def test_and_register_register():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["and"])
    cpu.regs[Reg.GA] = 0b1100
    cpu.regs[Reg.GB] = 0b1010

    execute(cpu, cpu.execute_and)

    assert cpu.regs[Reg.GA] == 0b1000


def test_or_register_register():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["or"])
    cpu.regs[Reg.GA] = 0b1100
    cpu.regs[Reg.GB] = 0b1010

    execute(cpu, cpu.execute_or)

    assert cpu.regs[Reg.GA] == 0b1110


def test_xor_register_register():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["xor"])
    cpu.regs[Reg.GA] = 0b1100
    cpu.regs[Reg.GB] = 0b1010

    execute(cpu, cpu.execute_xor)

    assert cpu.regs[Reg.GA] == 0b0110


@pytest.mark.parametrize(
    ("mnemonic", "handler_name", "initial", "operand", "expected"),
    [
        ("and", "execute_and", 0b1100, 0b1010, 0b1000),
        ("or", "execute_or", 0b1100, 0b1010, 0b1110),
        ("xor", "execute_xor", 0b1100, 0b1010, 0b0110),
    ],
)
def test_bitwise_register_memory(mnemonic, handler_name, initial, operand, expected):
    cpu = cpu_with_instruction(0x00, 0x09, OPCODES[mnemonic])
    cpu.regs[Reg.GA] = initial
    cpu.regs[Reg.GB] = 300
    cpu.memory[300] = operand

    execute(cpu, getattr(cpu, handler_name))

    assert cpu.regs[Reg.GA] == expected


@pytest.mark.parametrize(
    ("mnemonic", "handler_name", "initial", "operand", "expected"),
    [
        ("and", "execute_and", 0b1100, 0b1010, 0b1000),
        ("or", "execute_or", 0b1100, 0b1010, 0b1110),
        ("xor", "execute_xor", 0b1100, 0b1010, 0b0110),
    ],
)
def test_bitwise_memory_register(mnemonic, handler_name, initial, operand, expected):
    cpu = cpu_with_instruction(0x08, 0x01, OPCODES[mnemonic])
    cpu.regs[Reg.GA] = 300
    cpu.regs[Reg.GB] = operand
    cpu.memory[300] = initial

    execute(cpu, getattr(cpu, handler_name))

    assert cpu.memory[300] == expected
