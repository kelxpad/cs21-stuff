import sys
from pathlib import Path
from emulator import CPU

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

def test_display_starts_black():
    cpu = CPU([0] * 65536, 0)

    assert all(pixel == 0 for pixel in cpu.buffer0)
    assert all(pixel == 0 for pixel in cpu.buffer1)

def test_swap_toggles_active_buffer():
    cpu = CPU([0] * 65536, 0)

    assert cpu.active_buffer == 0

    cpu.swap_buffers()

    assert cpu.active_buffer == 1

    cpu.swap_buffers()

    assert cpu.active_buffer == 0

def test_swap_reveals_back_buffer():
    cpu = CPU([0] * 65536, 0)

    cpu.back_buffer[0] = 0x00FF0000

    cpu.swap_buffers()

    assert cpu.front_buffer[0] == 0x00FF0000