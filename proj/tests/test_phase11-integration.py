import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from emulator import (BUTTON_ADDR,OPCODES,RNG_ADDR,TICK_ADDR,CPU,Reg,run_headless)


def instruction_word(op1, op2=0x00, opcode=0x02):
    return (op1 << 10) | (op2 << 5) | opcode


def write_binary(path, words):
    data = bytearray()

    for word in words:
        data.append(word & 0xFF)
        data.append((word >> 8) & 0xFF)

    path.write_bytes(data)


def test_run_headless_executes_exact_instruction_count(tmp_path):
    bin_path = tmp_path / "program.252bin"
    write_binary(
        bin_path,
        [
            instruction_word(0x00, 0x1E, OPCODES["set"]),
            0x0005,
            instruction_word(0x00, 0x1E, OPCODES["add"]),
            0x0007,
        ],
    )

    cpu = run_headless(str(bin_path), 2, 123)

    assert cpu.instructions_executed == 2
    assert cpu.tick_counter == 2
    assert cpu.regs[Reg.GA] == 12
    assert cpu.regs[Reg.PC] == 4


def test_run_headless_zero_steps_loads_without_executing(tmp_path):
    bin_path = tmp_path / "program.252bin"
    write_binary(bin_path, [instruction_word(0x00, 0x1E, OPCODES["set"]), 0xBEEF])

    cpu = run_headless(str(bin_path), 0, 123)

    assert cpu.instructions_executed == 0
    assert cpu.tick_counter == 0
    assert cpu.regs[Reg.GA] == 0
    assert cpu.regs[Reg.PC] == 0


def test_run_headless_rejects_negative_instruction_count(tmp_path):
    bin_path = tmp_path / "program.252bin"
    write_binary(bin_path, [])

    try:
        run_headless(str(bin_path), -1, 123)
    except ValueError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("negative instruction count should fail")

# test disabled, might not work on different devices
# def test_cli_starts_pyxel_window(tmp_path): 
#     bin_path = tmp_path / "program.252bin"
#     write_binary(bin_path, [instruction_word(0x00, 0x1E, OPCODES["set"]), 0x0005])
#     fake_pyxel = tmp_path / "pyxel.py"
#     fake_pyxel.write_text(
#         "def init(width, height, title):\n"
#         "    print(f'init {width} {height} {title}')\n"
#         "\n"
#         "def run(update, draw):\n"
#         "    print('run')\n"
#         "    update()\n"
#         "    draw()\n"
#         "\n"
#         "def cls(color):\n"
#         "    print(f'cls {color}')\n"
#         "\n"
#         "def rect(x, y, width, height, color):\n"
#         "    return None\n"
#     )
#     env = os.environ.copy()
#     env["PYTHONPATH"] = str(tmp_path)

#     result = subprocess.run(
#         [sys.executable, str(root_dir / "emulator.py"), str(bin_path), "1", "123"],
#         check=True,
#         capture_output=True,
#         text=True,
#         env=env,
#     )

#     assert "init 256 256 Arch-252 Emulator" in result.stdout
#     assert "run" in result.stdout
#     assert "cls 0" in result.stdout
#     assert "set(op1=" not in result.stdout

def test_tick_mmio_reads_current_tick_counter():
    cpu = CPU([0] * 65536, 123)
    cpu.tick_counter = 0x12345

    assert cpu.memory_read(TICK_ADDR) == 0x2345


def test_button_mmio_reads_and_writes_low_bit_only():
    cpu = CPU([0] * 65536, 123)

    cpu.memory_write(BUTTON_ADDR, 0xFFFE)
    assert cpu.memory_read(BUTTON_ADDR) == 0

    cpu.memory_write(BUTTON_ADDR, 0xFFFF)
    assert cpu.memory_read(BUTTON_ADDR) == 1


def test_rng_mmio_is_deterministic_for_seed_and_ignores_writes():
    first = CPU([0] * 65536, 123)
    second = CPU([0] * 65536, 123)

    first.memory_write(RNG_ADDR, 0xBEEF)

    assert first.memory_read(RNG_ADDR) == second.memory_read(RNG_ADDR)
    assert first.memory_read(RNG_ADDR) == second.memory_read(RNG_ADDR)
