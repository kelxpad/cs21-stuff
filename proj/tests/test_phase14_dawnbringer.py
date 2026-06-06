import sys
from pathlib import Path
from emulator import Display, CPU

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))


def test_quantize_exact_palette_colors():
    seed = 67
    ipf = 67 # arbitrary for this test
    cpu = CPU([0] * 65536, seed)
    display = Display(cpu=cpu, seed=seed, ipf=ipf)
    for i, (r,g,b) in enumerate(display.DAWNBRINGER16):
        pixel = (r << 16) | (g << 8) | b

        assert display.quantize(pixel) == i

