import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import CPU

def test_decode_fields():
    memory = [0] * 65536

    opcode = 2
    op1 = 5
    op2 = 3

    memory[0] = ((op1 << 10) | (op2 << 5) | opcode)
    cpu = CPU(memory, 67)

    decoded = cpu.decode()
    
    assert decoded.opcode == opcode
    assert decoded.op1_encoding == op1
    assert decoded.op2_encoding == op2

def test_decode_max_values():
    memory = [0] * 65536
    opcode = 0x1F
    op2 = 0x1F
    op1 = 0x3F

    memory[0] = ((op1 << 10) | (op2 << 5) | opcode)

    cpu = CPU(memory, 67)
    decoded = cpu.decode()

    assert decoded.opcode == 0x1F
    assert decoded.op2_encoding == 0x1F
    assert decoded.op1_encoding == 0x3F

# instruction widths section
def test_type1_width():
    memory = [0] * 65536
    memory[0] = (0x00 << 10) | (0x01 << 5) | 0x02
    cpu = CPU(memory, 67)
    decoded = cpu.decode()
    assert cpu.instruction_width(decoded) == 2

def test_type2_width():
    memory = [0] * 65536
    memory[0] = (0x1E << 10) | (0x01 << 5) | 0x02
    cpu = CPU(memory, 67)
    decoded = cpu.decode()
    assert cpu.instruction_width(decoded) == 4

def test_type3_width():
    memory = [0] * 65536
    memory[0] = (0x1E << 10) | (0x1F << 5) | 0x02
    cpu = CPU(memory, 67)
    decoded = cpu.decode()
    assert cpu.instruction_width(decoded) == 6

def test_next_pc_type3():
    memory = [0] * 65536
    memory[0] = (0x1E << 10) | (0x1F << 5) | 0x02
    cpu = CPU(memory, 67)
    assert cpu.next_pc() == 3