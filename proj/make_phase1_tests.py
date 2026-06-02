# make_phase1_tests.py

def write_bin(filename, words):
    with open(filename, "wb") as f:
        for w in words:
            f.write(w.to_bytes(2, "little"))

# test 1: sequential values
test1 = [
    0x0001,
    0x0203,
    0x0405,
    0x0607,
    0x0809,
    0x0A0B,
    0x0C0D,
    0x0E0F,
]

write_bin("test1.252bin", test1)

# test 2: edge values
test2 = [
    0x0000,
    0xFFFF,
    0x00FF,
    0xFF00,
    0x1234,
    0x8000,
    0x7FFF,
]

write_bin("test2.252bin", test2)

# test 3: mixed
test3 = [
    0xAAAA,
    0x5555,
    0x0F0F,
    0xF0F0,
    0x1357,
    0x2468,
    0xBEEF,
    0xC0DE,
]

write_bin("test3.252bin", test3)