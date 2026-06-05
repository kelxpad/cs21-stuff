import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import CPU, OPCODES, RAM_STACK_END, Reg


NEXT_PC = 1
NEXT_NEXT_PC = 3


def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def cpu_with_instruction(op1, op2, opcode):
    memory = [0] * 65536
    memory[0] = instruction_word(op1, op2, opcode)
    memory[NEXT_PC] = instruction_word(0x1E, 0x00, OPCODES["set"])
    return CPU(memory, 0)


def execute(cpu, handler):
    decoded = cpu.decode()
    handler(decoded)


def assert_branch_taken(cpu):
    assert cpu.regs[Reg.PC] == NEXT_PC


def assert_branch_not_taken(cpu):
    assert cpu.regs[Reg.PC] == NEXT_NEXT_PC


def test_jmp_to_register_pushes_next_pc_and_sets_pc():
    cpu = cpu_with_instruction(0x00, 0x00, OPCODES["jmp"])
    cpu.regs[Reg.GA] = 0x1234

    execute(cpu, cpu.execute_jmp)

    assert cpu.regs[Reg.PC] == 0x1234
    assert cpu.regs[Reg.SP] == RAM_STACK_END - 1
    assert cpu.memory[RAM_STACK_END - 1] == NEXT_PC


def test_jmp_to_literal_pushes_next_pc_and_sets_pc():
    cpu = cpu_with_instruction(0x1E, 0x00, OPCODES["jmp"])
    cpu.memory[1] = 0x2345

    execute(cpu, cpu.execute_jmp)

    assert cpu.regs[Reg.PC] == 0x2345
    assert cpu.regs[Reg.SP] == RAM_STACK_END - 1
    assert cpu.memory[RAM_STACK_END - 1] == 2


def test_ifany_branches_when_operands_share_a_bit():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifany"])
    cpu.regs[Reg.GA] = 0b1010
    cpu.regs[Reg.GB] = 0b0010

    execute(cpu, cpu.execute_ifany)

    assert_branch_taken(cpu)


def test_ifany_skips_when_operands_share_no_bits():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifany"])
    cpu.regs[Reg.GA] = 0b1000
    cpu.regs[Reg.GB] = 0b0010

    execute(cpu, cpu.execute_ifany)

    assert_branch_not_taken(cpu)


def test_ifnon_branches_when_operands_share_no_bits():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifnon"])
    cpu.regs[Reg.GA] = 0b1000
    cpu.regs[Reg.GB] = 0b0010

    execute(cpu, cpu.execute_ifnon)

    assert_branch_taken(cpu)


def test_ifnon_skips_when_operands_share_a_bit():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifnon"])
    cpu.regs[Reg.GA] = 0b1010
    cpu.regs[Reg.GB] = 0b0010

    execute(cpu, cpu.execute_ifnon)

    assert_branch_not_taken(cpu)


def test_ifeq_branches_when_operands_are_equal():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifeq"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0xBEEF

    execute(cpu, cpu.execute_ifeq)

    assert_branch_taken(cpu)


def test_ifeq_skips_when_operands_are_not_equal():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifeq"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0xCAFE

    execute(cpu, cpu.execute_ifeq)

    assert_branch_not_taken(cpu)


def test_ifne_branches_when_operands_are_not_equal():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifne"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0xCAFE

    execute(cpu, cpu.execute_ifne)

    assert_branch_taken(cpu)


def test_ifne_skips_when_operands_are_equal():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifne"])
    cpu.regs[Reg.GA] = 0xBEEF
    cpu.regs[Reg.GB] = 0xBEEF

    execute(cpu, cpu.execute_ifne)

    assert_branch_not_taken(cpu)


def test_ifgtu_branches_using_unsigned_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifgtu"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0001

    execute(cpu, cpu.execute_ifgtu)

    assert_branch_taken(cpu)


def test_ifgtu_skips_using_unsigned_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifgtu"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0xFFFF

    execute(cpu, cpu.execute_ifgtu)

    assert_branch_not_taken(cpu)


def test_ifgts_branches_using_signed_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifgts"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0xFFFF

    execute(cpu, cpu.execute_ifgts)

    assert_branch_taken(cpu)


def test_ifgts_skips_using_signed_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifgts"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0001

    execute(cpu, cpu.execute_ifgts)

    assert_branch_not_taken(cpu)


def test_ifltu_branches_using_unsigned_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifltu"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0xFFFF

    execute(cpu, cpu.execute_ifltu)

    assert_branch_taken(cpu)


def test_ifltu_skips_using_unsigned_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["ifltu"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0001

    execute(cpu, cpu.execute_ifltu)

    assert_branch_not_taken(cpu)


def test_iflts_branches_using_signed_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["iflts"])
    cpu.regs[Reg.GA] = 0xFFFF
    cpu.regs[Reg.GB] = 0x0001

    execute(cpu, cpu.execute_iflts)

    assert_branch_taken(cpu)


def test_iflts_skips_using_signed_comparison():
    cpu = cpu_with_instruction(0x00, 0x01, OPCODES["iflts"])
    cpu.regs[Reg.GA] = 0x0001
    cpu.regs[Reg.GB] = 0xFFFF

    execute(cpu, cpu.execute_iflts)

    assert_branch_not_taken(cpu)