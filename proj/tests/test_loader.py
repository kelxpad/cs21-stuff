import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import load_binary, ADDRESS_SPACE_WORDS, CPU, Reg


TEST_BIN_DIR = Path(__file__).parent / "test_bins"


def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def test_sequential_words():
    memory = load_binary(
        TEST_BIN_DIR / "test1.252bin"
    )

    expected = [
        0x0001,
        0x0203,
        0x0405,
        0x0607,
        0x0809,
        0x0A0B,
        0x0C0D,
        0x0E0F,
    ]

    for i, word in enumerate(expected):
        assert memory[i] == word


def test_edge_values():
    memory = load_binary(
        TEST_BIN_DIR / "test2.252bin"
    )

    expected = [
        0x0000,
        0xFFFF,
        0x00FF,
        0xFF00,
        0x1234,
        0x8000,
        0x7FFF,
    ]

    for i, word in enumerate(expected):
        assert memory[i] == word


def test_mixed_pattern():
    memory = load_binary(
        TEST_BIN_DIR / "test3.252bin"
    )

    expected = [
        0xAAAA,
        0x5555,
        0x0F0F,
        0xF0F0,
        0x1357,
        0x2468,
        0xBEEF,
        0xC0DE,
    ]

    for i, word in enumerate(expected):
        assert memory[i] == word

def test_unused_memory_is_zero():
    for i in range(1, 4):
        memory = load_binary( TEST_BIN_DIR / f"test{i}.252bin")

        for j in range(8, 65536):
            assert memory[j] == 0

def test_memory_size():
    for i in range(1, 4):
        memory = load_binary( TEST_BIN_DIR / f"test{i}.252bin")

        assert len(memory) == ADDRESS_SPACE_WORDS

def test_register_count():
    cpu = CPU([0] * 65536, 123)

    assert len(cpu.regs) == len(Reg)

def test_init_tick_counter_initial_value():
    cpu = CPU([0] * 65536, 123)

    assert cpu.tick_counter == 0

def test_read_register_indirect():
    memory = [0] * 65536
    cpu = CPU(memory, 67)
    cpu.regs[Reg.GA] = 123
    memory[0] = instruction_word(0x08)
    memory[123] = 0xBEEF
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0xBEEF

def test_read_literal():
    memory = [0] * 65536
    cpu = CPU(memory, 67)
    cpu.regs[Reg.PC] = 100
    memory[100] = instruction_word(0x1E)
    memory[101] = 0xCAFE
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0xCAFE

def test_read_at_literal():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.PC] = 100
    memory[100] = instruction_word(0x1F)
    memory[101] = 500
    memory[500] = 0x1234
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0x1234

# immediate helper unit tests
def test_op1_immediate_offset():
    memory = [0] * 65536

    opcode = 0x02

    op1 = 0x10
    op2 = 0x00

    memory[0] = instruction_word(op1, op2, opcode)

    cpu = CPU(memory, 0)
    decoded = cpu.decode()

    assert (cpu.operand_immediate_offset(decoded, 1) == 1)

def test_op2_immediate_offset():
    memory = [0] * 65536

    opcode = 0x02

    op1 = 0x00
    op2 = 0x10

    memory[0] = instruction_word(op1, op2, opcode)

    cpu = CPU(memory, 0)
    decoded = cpu.decode()

    assert cpu.operand_immediate_offset(decoded, 2) == 1

def test_dual_immediate_offsets():
    memory = [0] * 65536

    opcode = 0x02

    op1 = 0x10
    op2 = 0x11

    memory[0] = instruction_word(op1, op2, opcode)

    cpu = CPU(memory, 0)
    decoded = cpu.decode()

    assert (cpu.operand_immediate_offset(decoded, 1) == 1)
    assert (cpu.operand_immediate_offset(decoded, 2) == 2)

def test_dual_immediate_values_2():
    memory = [0] * 65536

    memory[0] = instruction_word(0x10, 0x11, 0x02)

    memory[1] = 0x1234
    memory[2] = 0x5678

    cpu = CPU(memory, 0)
    decoded = cpu.decode()

    assert cpu.operand_immediate(decoded, 1) == 0x1234
    assert cpu.operand_immediate(decoded, 2) == 0x5678
def test_read_register_plus_k():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.GA] = 100
    cpu.regs[Reg.PC] = 50
    memory[50] = instruction_word(0x10)
    memory[51] = 20
    memory[120] = 0xBEEF
    decoded = cpu.decode()

    assert (cpu.read_operand(decoded, 1) == 0xBEEF)

def test_duplicate_immediate_operands_use_operand_index():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.GA] = 100
    cpu.regs[Reg.PC] = 50
    memory[50] = instruction_word(0x10, 0x10)
    memory[51] = 20
    memory[52] = 30
    memory[120] = 0xAAAA
    memory[130] = 0xBBBB
    decoded = cpu.decode()

    assert cpu.operand_immediate(decoded, 1) == 20
    assert cpu.operand_immediate(decoded, 2) == 30
    assert cpu.read_operand(decoded, 1) == 0xAAAA
    assert cpu.read_operand(decoded, 2) == 0xBBBB

# push-pop-peek tests

def test_write_push():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFFE
    memory[0] = instruction_word(0x18)
    decoded = cpu.decode()

    cpu.write_operand(decoded, 1, 0xBEEF)

    assert cpu.regs[Reg.SP] == 0xFFFD
    assert memory[0xFFFD] == 0xBEEF

def test_read_pop():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFFD
    memory[0] = instruction_word(0x18)
    memory[0xFFFD] = 0xBEEF
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0xBEEF
    assert cpu.regs[Reg.SP] == 0xFFFE

def test_read_peek():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFFD
    memory[0] = instruction_word(0x19)
    memory[0xFFFD] = 0xCAFE
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0xCAFE
    assert cpu.regs[Reg.SP] == 0xFFFD

def test_write_peek():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFFD
    memory[0] = instruction_word(0x19)
    decoded = cpu.decode()

    cpu.write_operand(decoded, 1, 0xCAFE)

    assert cpu.regs[Reg.SP] == 0xFFFD
    assert memory[0xFFFD] == 0xCAFE

def test_read_peek_plus_k():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFF0
    cpu.regs[Reg.PC] = 50
    memory[50] = instruction_word(0x1A)
    memory[51] = 3
    memory[0xFFF3] = 0x1234
    decoded = cpu.decode()

    assert cpu.read_operand(decoded, 1) == 0x1234
    assert cpu.regs[Reg.SP] == 0xFFF0

def test_write_peek_plus_k():
    memory = [0] * 65536
    cpu = CPU(memory, 0)
    cpu.regs[Reg.SP] = 0xFFF0
    cpu.regs[Reg.PC] = 50
    memory[50] = instruction_word(0x1A)
    memory[51] = 3
    decoded = cpu.decode()

    cpu.write_operand(decoded, 1, 0x1234)

    assert cpu.regs[Reg.SP] == 0xFFF0
    assert memory[0xFFF3] == 0x1234
