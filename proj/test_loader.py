# to be ran via pytest
from emulator import load_binary, ADDRESS_SPACE_WORDS

def test_sequential_words():
    memory = load_binary("test1.252bin")

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
    memory = load_binary("test2.252bin")

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
    memory = load_binary("test3.252bin")

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
        memory = load_binary(f"test{i}.252bin")

        for j in range(8, 65536):
            assert memory[j] == 0

def test_memory_size():
    for i in range(1, 4):
        memory = load_binary(f"test{i}.252bin")

        assert len(memory) == ADDRESS_SPACE_WORDS