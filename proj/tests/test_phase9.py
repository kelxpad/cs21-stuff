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


def test_addt_uses_arbitrary_tm_without_overflow():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["addt"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0x0002
    cpu.regs[Reg.TM] = 0x1234

    execute(cpu, cpu.execute_addt)

    assert cpu.regs[Reg.GA] == 0x1237
    assert cpu.regs[Reg.TM] == 0x0000


def test_addt_uses_arbitrary_tm_and_sets_overflow():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["addt"])
    cpu.regs[Reg.GA] = 0xFF00
    cpu.regs[Reg.GB] = 0x0010
    cpu.regs[Reg.TM] = 0x0100

    execute(cpu, cpu.execute_addt)

    assert cpu.regs[Reg.GA] == 0x0010
    assert cpu.regs[Reg.TM] == 0x0001

# manual add
def test_addt_uses_previous_carry():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["addt"])

    cpu.regs[Reg.GA] = 5
    cpu.regs[Reg.GB] = 7
    cpu.regs[Reg.TM] = 1

    execute(cpu, cpu.execute_addt)

    assert cpu.regs[Reg.GA] == 13
    assert cpu.regs[Reg.TM] == 0

def test_subt_sets_borrow_on_underflow():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["subt"])
    cpu.regs[Reg.GA] = 0x0002
    cpu.regs[Reg.GB] = 0x0003
    cpu.regs[Reg.TM] = 0x0000

    execute(cpu, cpu.execute_subt)

    assert cpu.regs[Reg.GA] == WORD_MASK
    assert cpu.regs[Reg.TM] == WORD_MASK


def test_subt_clears_borrow_when_no_underflow():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["subt"])
    cpu.regs[Reg.GA] = 0x0005
    cpu.regs[Reg.GB] = 0x0003
    cpu.regs[Reg.TM] = 0x0000

    execute(cpu, cpu.execute_subt)

    assert cpu.regs[Reg.GA] == 0x0002
    assert cpu.regs[Reg.TM] == 0x0000

def test_subt_propagates_previous_borrow():
    # NOTE: ambiguous whether REG[tm] is supposed to be treated as a 
    # signed/unsigned value, assuming unsigned for now
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["subt"])
    cpu.regs[Reg.GA] = 0x0000
    cpu.regs[Reg.GB] = 0x0000
    cpu.regs[Reg.TM] = WORD_MASK

    execute(cpu, cpu.execute_subt)

    assert cpu.regs[Reg.GA] == WORD_MASK
    assert cpu.regs[Reg.TM] == 0

def test_subt_clears_previous_borrow_when_result_does_not_underflow():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["subt"])
    cpu.regs[Reg.GA] = 0x0005
    cpu.regs[Reg.GB] = 0x0003
    cpu.regs[Reg.TM] = WORD_MASK

    execute(cpu, cpu.execute_subt)

    assert cpu.regs[Reg.GA] == 0x0001
    assert cpu.regs[Reg.TM] == 0x0000


def test_seti_copies_operand_and_increments_gg_gh():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["seti"])
    cpu.regs[Reg.GA] = 0x0000
    cpu.regs[Reg.GB] = 0xBEEF

# manually added
def test_seti_wraps_gg_and_gh():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["seti"])

    cpu.regs[Reg.GG] = 0xFFFF
    cpu.regs[Reg.GH] = 0xFFFF
    cpu.regs[Reg.GB] = 123

    execute(cpu, cpu.execute_seti)

    assert cpu.regs[Reg.GG] == 0x0000
    assert cpu.regs[Reg.GH] == 0x0000

# manually added
def test_setd_wraps_gg_and_gh():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["setd"])

    cpu.regs[Reg.GG] = 0x0000
    cpu.regs[Reg.GH] = 0x0000
    cpu.regs[Reg.GB] = 123

    execute(cpu, cpu.execute_setd)

    assert cpu.regs[Reg.GG] == 0xFFFF
    assert cpu.regs[Reg.GH] == 0xFFFF