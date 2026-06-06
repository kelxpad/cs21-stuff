import sys
from pathlib import Path
from emulator import CPU, OPCODES, WORD_MASK

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))



def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def cpu_with_instruction(opcode):
    memory = [0] * 65536
    memory[0] = instruction_word(0x00, 0x01, opcode)
    return CPU(memory, 0)


def assert_step_dispatches_to_handler(mnemonic):
    opcode = OPCODES[mnemonic]
    cpu = cpu_with_instruction(opcode)
    calls = []

    def handler(decoded):
        calls.append(decoded)

    # manual edit: integrated tick counter and inst exec increment test here
    cpu.handlers[opcode] = handler
    prev_counter = cpu.tick_counter
    prev_instructions_executed = cpu.instructions_executed
    cpu.step()

    assert len(calls) == 1
    assert cpu.tick_counter == (prev_counter + 1)
    assert cpu.instructions_executed == (prev_instructions_executed + 1)
    assert calls[0].opcode == opcode
    assert calls[0].raw_word == instruction_word(0x00, 0x01, opcode)

def test_step_dispatches_jmp():
    assert_step_dispatches_to_handler("jmp")


def test_step_dispatches_set():
    assert_step_dispatches_to_handler("set")


def test_step_dispatches_add():
    assert_step_dispatches_to_handler("add")


def test_step_dispatches_sub():
    assert_step_dispatches_to_handler("sub")


def test_step_dispatches_mulu():
    assert_step_dispatches_to_handler("mulu")


def test_step_dispatches_muls():
    assert_step_dispatches_to_handler("muls")


def test_step_dispatches_divu():
    assert_step_dispatches_to_handler("divu")


def test_step_dispatches_divs():
    assert_step_dispatches_to_handler("divs")


def test_step_dispatches_modu():
    assert_step_dispatches_to_handler("modu")


def test_step_dispatches_mods():
    assert_step_dispatches_to_handler("mods")


def test_step_dispatches_and():
    assert_step_dispatches_to_handler("and")


def test_step_dispatches_or():
    assert_step_dispatches_to_handler("or")


def test_step_dispatches_xor():
    assert_step_dispatches_to_handler("xor")


def test_step_dispatches_srl():
    assert_step_dispatches_to_handler("srl")


def test_step_dispatches_sra():
    assert_step_dispatches_to_handler("sra")


def test_step_dispatches_sll():
    assert_step_dispatches_to_handler("sll")


def test_step_dispatches_ifany():
    assert_step_dispatches_to_handler("ifany")


def test_step_dispatches_ifnon():
    assert_step_dispatches_to_handler("ifnon")


def test_step_dispatches_ifeq():
    assert_step_dispatches_to_handler("ifeq")


def test_step_dispatches_ifne():
    assert_step_dispatches_to_handler("ifne")


def test_step_dispatches_ifgtu():
    assert_step_dispatches_to_handler("ifgtu")


def test_step_dispatches_ifgts():
    assert_step_dispatches_to_handler("ifgts")


def test_step_dispatches_ifltu():
    assert_step_dispatches_to_handler("ifltu")


def test_step_dispatches_iflts():
    assert_step_dispatches_to_handler("iflts")


def test_step_dispatches_addt():
    assert_step_dispatches_to_handler("addt")


def test_step_dispatches_subt():
    assert_step_dispatches_to_handler("subt")


def test_step_dispatches_seti():
    assert_step_dispatches_to_handler("seti")


def test_step_dispatches_setd():
    assert_step_dispatches_to_handler("setd")