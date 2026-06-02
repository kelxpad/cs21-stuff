import sys
import random
from enum import IntEnum, auto

ADDRESS_SPACE_WORDS = 65536
WORD_MASK = 0xFFFF

# register stuff
class Reg(IntEnum):
    PC = 0
    SP = auto()
    TM = auto()
    GA = auto()
    GB = auto()
    GC = auto()
    GD = auto()
    GE = auto()
    GF = auto()
    GG = auto()
    GH = auto()

class CPU:
    def __init__(self, memory: list[int], seed: int) -> None:
        self.memory = memory
        self.regs = [0] * len(Reg)

        # initialize register values (if applicable) here
        # self.regs[Reg.SP] = 0xFFFF

        self.tick_counter = 0
        self.rng = random.Random(seed)
        self.instructions_executed = 0

    def step(self):
        """
        Executes one Arch-252 instruction.
        """
        ...

REGISTER_NAMES = {
    Reg.PC: "pc",
    Reg.SP: "sp",
    Reg.TM: "tm",
    Reg.GA: "ga",
    Reg.GB: "gb",
    Reg.GC: "gc",
    Reg.GD: "gd",
    Reg.GE: "ge",
    Reg.GF: "gf",
    Reg.GG: "gg",
    Reg.GH: "gh",
}

# memory mapping
RAM_INSTDATA_START = 0x0000
RAM_INSTDATA_END   = 0x8fff

DISPLAY_START      = 0X9000
DISPLAY_END        = 0x9800

BUTTON_ADDR        = 0x9801
TICK_ADDR          = 0x9802
RNG_ADDR           = 0x9803

RAM_STACK_START     = 0xA000
RAM_STACK_END       = 0xFFFF

# instructions <-> opcodes
INSTRUCTIONS = {
    0x00: "jmp",
    0x01: "set",
    0x02: "add",
    0x03: "sub",
    0x04: "mulu",
    0x05: "muls",
    0x06: "divu",
    0x07: "divs",
    0x08: "modu",
    0x09: "mods",
    0x0A: "and",
    0x0B: "or",
    0x0C: "xor",
    0x0D: "srl",
    0x0E: "sra",
    0x0F: "sll",
    0x10: "ifany",
    0x11: "ifnon",
    0x12: "ifeq",
    0x13: "ifne",
    0x14: "ifgtu",
    0x15: "ifgts",
    0x16: "ifltu",
    0x17: "iflts",
    0x18: "addt",
    0x19: "subt",
    0x1A: "seti",
    0x1B: "setd",
}

# reverse lookup
OPCODES = {name: opcode for opcode, name in INSTRUCTIONS.items()}

# TODO: MMIO handled through functions cpu.memory_read(addr), cpu.memory_write(addr, value), class CPU

def load_binary(path: str) -> list[int]:
    memory = [0] * ADDRESS_SPACE_WORDS

    with open(path, "rb") as f:
        data = f.read()
    
    if len(data) % 2 != 0:
        raise ValueError("Binary size must be a multiple of 2 bytes!")

    word_count = len(data) // 2

    if word_count > ADDRESS_SPACE_WORDS:
        raise ValueError("Binary exceeds address space!")
    
    for addr in range(word_count):
        low = data[2 * addr]
        high = data[2 * addr + 1]

        # file stores words as [low_byte, high_byte] (little-endian)
        # 0x34 0x12 becomes 0x1234
        memory[addr] = low | (high << 8)
    
    return memory

def dump_memory(memory, count=16):
    print("First words loaded:")

    for addr in range(count):
        print(
            f"{addr:04X}: {memory[addr]:04X}"
        )

def dump_registers(cpu: CPU):
    for reg in Reg:
        print(
            f"{REGISTER_NAMES[reg]} : "
            f"{cpu.regs[reg]:04X}"
        )

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 emulator.py <bin-filepath> <ipf> <seed>")
        sys.exit(1)

    bin_path = sys.argv[1]
    ipf = int(sys.argv[2])
    seed = int(sys.argv[3])

    memory = load_binary(bin_path)
    cpu = CPU(memory, seed)

    print(f"bin file = {bin_path}")
    print(f"ipf      = {ipf}")
    print(f"seed     = {seed}")

    # dump_memory(memory)
    # dump_registers(cpu)

if __name__ == "__main__":
    main()