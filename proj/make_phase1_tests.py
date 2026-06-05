from pathlib import Path

TEST_DIR = Path("tests/test_bins")
TEST_DIR.mkdir(parents=True, exist_ok=True)


def write_bin(filename, words):
    with open(TEST_DIR / filename, "wb") as f:
        for w in words:
            f.write(w.to_bytes(2, "little"))


write_bin(
    "test1.252bin",
    [
        0x0001,
        0x0203,
        0x0405,
        0x0607,
        0x0809,
        0x0A0B,
        0x0C0D,
        0x0E0F,
    ],
)

write_bin(
    "test2.252bin",
    [
        0x0000,
        0xFFFF,
        0x00FF,
        0xFF00,
        0x1234,
        0x8000,
        0x7FFF,
    ],
)

write_bin(
    "test3.252bin",
    [
        0xAAAA,
        0x5555,
        0x0F0F,
        0xF0F0,
        0x1357,
        0x2468,
        0xBEEF,
        0xC0DE,
    ],
)

print("Generated test binaries.")