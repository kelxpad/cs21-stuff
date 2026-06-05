import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import CPU, OPCODES, Reg, WORD_MASK


def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def cpu_with_instruction(op1, op2, opcode):
    memory = [0] * 65536
    memory[0] = instruction_word(op1, op2, opcode)
    return CPU(memory, 0)


def execute(cpu, handler):
    decoded = cpu.decode()
    handler(decoded)


def test_mulu_stores_low_word_and_high_word_in_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["mulu"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_mulu)

    assert cpu.regs[Reg.GA] == 0xFFFE
    assert cpu.regs[Reg.TM] == 0x0001


def test_muls_uses_signed_operands_and_stores_sign_extended_high_word():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["muls"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_muls)

    assert cpu.regs[Reg.GA] == 0xFFFE
    assert cpu.regs[Reg.TM] == WORD_MASK


def test_divu_stores_integer_quotient_and_fractional_word_in_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["divu"])
    cpu.regs[Reg.GA] = 7
    cpu.regs[Reg.GB] = 2

    execute(cpu, cpu.execute_divu)

    assert cpu.regs[Reg.GA] == 3
    assert cpu.regs[Reg.TM] == 0x8000


def test_divu_by_zero_clears_destination_and_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["divu"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0
    cpu.regs[Reg.TM] = 0xCAFE

    execute(cpu, cpu.execute_divu)

    assert cpu.regs[Reg.GA] == 0
    assert cpu.regs[Reg.TM] == 0


def test_divs_truncates_negative_quotient_toward_zero():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["divs"])
    cpu.regs[Reg.GA] = 0xFFF9
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_divs)

    assert cpu.regs[Reg.GA] == 0xFFFD
    assert cpu.regs[Reg.TM] == 0x8000


def test_divs_by_zero_clears_destination_and_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["divs"])
    cpu.regs[Reg.GA] = 0x8000
    cpu.regs[Reg.GB] = 0
    cpu.regs[Reg.TM] = 0x1234

    execute(cpu, cpu.execute_divs)

    assert cpu.regs[Reg.GA] == 0
    assert cpu.regs[Reg.TM] == 0


def test_modu_by_zero_clears_destination():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["modu"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0

    execute(cpu, cpu.execute_modu)

    assert cpu.regs[Reg.GA] == 0


def test_mods_keeps_remainder_sign_from_dividend():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["mods"])
    cpu.regs[Reg.GA] = 0xFFF9
    cpu.regs[Reg.GB] = 0x0002

    execute(cpu, cpu.execute_mods)

    assert cpu.regs[Reg.GA] == WORD_MASK


def test_mods_by_zero_clears_destination():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["mods"])
    cpu.regs[Reg.GA] = 0x8001
    cpu.regs[Reg.GB] = 0

    execute(cpu, cpu.execute_mods)

    assert cpu.regs[Reg.GA] == 0


def test_srl_stores_shifted_value_and_shifted_out_bits_in_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["srl"])
    cpu.regs[Reg.GA] = 0x1234
    cpu.regs[Reg.GB] = 4

    execute(cpu, cpu.execute_srl)

    assert cpu.regs[Reg.GA] == 0x0123
    assert cpu.regs[Reg.TM] == 0x4000


def test_sra_preserves_sign_bit_and_uses_unsigned_carry_out_bits():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["sra"])
    cpu.regs[Reg.GA] = 0x8001
    cpu.regs[Reg.GB] = 1

    execute(cpu, cpu.execute_sra)

    assert cpu.regs[Reg.GA] == 0xC000
    assert cpu.regs[Reg.TM] == 0x8000


def test_sll_stores_low_word_and_high_word_in_tm():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["sll"])
    cpu.regs[Reg.GA] = 0x8001
    cpu.regs[Reg.GB] = 1

    execute(cpu, cpu.execute_sll)

    assert cpu.regs[Reg.GA] == 0x0002
    assert cpu.regs[Reg.TM] == 0x0001
