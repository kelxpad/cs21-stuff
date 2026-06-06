import sys
import random
import pyxel

from enum import IntEnum, auto
from dataclasses import dataclass

# useful constants
ADDRESS_SPACE_WORDS = 65536
DISPLAY_WIDTH = DISPLAY_HEIGHT = 32
DISPLAY_PIXELS = DISPLAY_WIDTH * DISPLAY_HEIGHT # 1024
WORD_MASK = 0xFFFF

# memory mapping
RAM_INSTDATA_START = 0x0000
RAM_INSTDATA_END   = 0x8FFF

DISPLAY_START      = 0X9000
DISPLAY_END        = 0x9800

BUTTON_ADDR        = 0x9801
TICK_ADDR          = 0x9802
RNG_ADDR           = 0x9803

RAM_STACK_START     = 0xA000
RAM_STACK_END       = 0xFFFF

@dataclass
class DecodedInstruction:
    raw_word: int
    opcode: int
    op1_encoding: int
    op2_encoding: int

type Buffer = list[int
                   ]
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

        # initialize register values
        self.regs[Reg.SP] = RAM_STACK_END

        self.button = 0
        self.tick_counter = 0
        self.rng = random.Random(seed)
        self.instructions_executed = 0

        self.handlers = {
            opcode: getattr(self, f"execute_{name}") 
            for opcode, name in INSTRUCTIONS.items()
        }

        self.buffer0 = [0] * DISPLAY_PIXELS
        self.buffer1  = [0] * DISPLAY_PIXELS
        self.active_buffer = 0

        # self.back_buffer[0] = 0xFFFF # checking if i hooked up the MMIO correctly, top-left pixel should become non-black
        # self.swap_buffers()

    @property
    def front_buffer(self) -> Buffer:
        return self.buffer0 if self.active_buffer == 0 else self.buffer1
    
    @property
    def back_buffer(self) -> Buffer:
        return self.buffer1 if self.active_buffer == 0 else self.buffer0
    
    def swap_buffers(self) -> None:
        self.active_buffer ^= 1 # toggle, when 0x9800 is written to, this triggers the swap

    def set_input_button(self, pressed: bool) -> None:
        self.button = 0x0001 if pressed else 0x0000

    def decode(self) -> DecodedInstruction:
        pc = self.regs[Reg.PC]

        instr_word = self.memory_read(pc)

        # bits 4-0 = opcode
        opcode = instr_word & 0x1F
        # bits 9-5 = op2
        op2 = (instr_word >> 5) & 0x1F
        # bits 15-10 = op1
        op1 = (instr_word >> 10) & 0x3F

        return DecodedInstruction(raw_word=instr_word, opcode=opcode, op1_encoding=op1, op2_encoding=op2)
    
    def operand_encoding(self, decoded: DecodedInstruction, operand_index: int) -> int:
        if operand_index == 1:
            return decoded.op1_encoding

        if operand_index == 2:
            return decoded.op2_encoding

        raise ValueError(f"operand index must be 1 or 2, got {operand_index}")

    def operand_immediate_offset(self, decoded: DecodedInstruction, operand_index: int) -> int:
        encoding = self.operand_encoding(decoded, operand_index)

        if not operand_has_immediate(encoding):
            return 0

        if operand_index == 1:
            return 1

        if operand_has_immediate(decoded.op1_encoding):
            return 2

        return 1

    def instruction_width(self, decoded: DecodedInstruction) -> int:
        # how many bytes wide is the instruction?
        # use amount of immediates as basis

        immediates = 0

        if operand_has_immediate(decoded.op1_encoding):
            immediates += 1

        if operand_has_immediate(decoded.op2_encoding):
            immediates += 1
        
        if immediates == 0:
            return 2
        
        if immediates == 1:
            return 4
        
        # imm == 2
        return 6
    
    def advance_pc(self) -> None:
        self.regs[Reg.PC] = self.next_pc()

    def next_pc(self) -> int:
        # word-addressed memory so divide by 2
        decoded = self.decode()

        return (
            self.regs[Reg.PC] 
            + self.instruction_width(decoded) // 2
        )
    
    def next_next_pc(self) -> int:
        pc = self.regs[Reg.PC]
        first = self.decode()

        next_pc = (pc + self.instruction_width(first) // 2)
        next_word = self.memory_read(next_pc)

        opcode = next_word & 0x1F
        op2 = (next_word >> 5) & 0x1F
        op1 = (next_word >> 10) & 0x3F

        second = DecodedInstruction(
            raw_word=next_word,
            opcode=opcode,
            op1_encoding=op1,
            op2_encoding=op2
        )

        return (next_pc + self.instruction_width(second) // 2)

    def memory_read(self, addr):
        addr &= WORD_MASK

        if DISPLAY_START <= addr <= DISPLAY_END:
            # Read operations directed to display device are ignored.
            return 0
        
        if addr == BUTTON_ADDR:
            return self.button & 0x0001
        
        if addr == TICK_ADDR:
            return self.tick_counter & WORD_MASK
        
        if addr == RNG_ADDR:
            return self.rng.randrange(0x10000)
        
        return self.memory[addr] & WORD_MASK
    
    def memory_write(self, addr, value):
        addr &= WORD_MASK
        value &= WORD_MASK

        # Display MMIO
        """
        For this emulator, the display occupies addresses 0x9000-0x97FF.
        From the specs, Arch-252 pixels are 32-bit values (e.g. 0x00RRGGBB).
        But since the architecture is word-addressed, each memory write is
        only 16 bits wide.

        Therefore, each pixel occupies TWO consecutive display addresses:
        Examples:
        pixel 0:
            0x9000 = low word (bits 15-0)
            0x9001 = high word (bits 31-16)

        pixel 1:
            0x9002 = low word (bits 15-0)
            0x9003 = high word

        ...

        pixel 1023:
            0x97FE = low word
            0x97FF = high word

        Since 1024 pixels * 2 words/pixel = 2048 words,
        the display MMIO region consumes exactly 0x800 == 2048 words.

        By the project specs (as of June 6, 2026, 6:09 PM), all pixel
        writes modify the INACTIVE display buffer, the back buffer.
        """
        if DISPLAY_START <= addr < DISPLAY_END:
            offset = addr - DISPLAY_START

            pixel_index = offset // 2
            high_word = (offset % 2) == 1
            pixel = self.back_buffer[pixel_index]

            if high_word:
                # replace bits 31-16
                pixel = ((pixel & 0x0000FFFF) | (value << 16))
            else: # low word
                # replace bits 15-0
                pixel = ((pixel & 0xFFFF0000) | value)
            self.back_buffer[pixel_index] = pixel
            return
        
        # Writing to 0x9800 swaps the active/inactive display buffers
        if addr == DISPLAY_END:
            self.swap_buffers()
            return

        if addr in {BUTTON_ADDR, TICK_ADDR, RNG_ADDR}:
            return
        
        self.memory[addr] = value
    
    def operand_immediate(self, decoded: DecodedInstruction, operand_index: int) -> int:
        pc = self.regs[Reg.PC]
        offset = self.operand_immediate_offset(decoded, operand_index)
        return self.memory_read(pc + offset)
    
    def read_operand(self, decoded: DecodedInstruction, operand_index: int):
        encoding = self.operand_encoding(decoded, operand_index)

        # pop
        if encoding == 0x18:
            addr = self.regs[Reg.SP]
            value = self.memory_read(addr)
            self.regs[Reg.SP] = (self.regs[Reg.SP] + 1) & WORD_MASK
            return value
        
        # peek
        if encoding == 0x19:
            return self.memory_read(self.regs[Reg.SP])
        
        # @peek+k
        if encoding == 0x1A:
            k = self.operand_immediate(decoded, operand_index)
            addr = (self.regs[Reg.SP] + k) & WORD_MASK
            return self.memory_read(addr)
        
        # register
        if encoding in OPERAND_TO_REGISTER:
            reg = OPERAND_TO_REGISTER[encoding]
            return self.regs[reg]
        
        # @register
        if encoding in REGISTER_INDIRECT:
            reg = REGISTER_INDIRECT[encoding]
            addr = self.regs[reg]
            return self.memory_read(addr)

        # literal
        if encoding == 0x1E:
            return self.operand_immediate(decoded, operand_index)
        
        # @literal
        if encoding == 0x1F:
            addr = self.operand_immediate(decoded, operand_index)

            return self.memory_read(addr)
        
        if encoding in REGISTER_PLUS_K:
            reg = REGISTER_PLUS_K[encoding]
            k = self.operand_immediate(decoded, operand_index)
            addr = (self.regs[reg] + k) & WORD_MASK
            return self.memory_read(addr)
        
        raise NotImplementedError(f"read operand {encoding:#x}")
    
    def write_operand(self, decoded: DecodedInstruction, operand_index: int, value):
        encoding = self.operand_encoding(decoded, operand_index)
        value &= WORD_MASK

        # push
        if encoding == 0x18:
            self.regs[Reg.SP] = (self.regs[Reg.SP] - 1) & WORD_MASK
            self.memory_write(self.regs[Reg.SP], value)
            return
        
        # peek
        if encoding == 0x19:
            self.memory_write(self.regs[Reg.SP], value)
            return
        
        # @peek+k
        if encoding == 0x1A:
            k = self.operand_immediate(decoded, operand_index)
            addr = (self.regs[Reg.SP] + k) & WORD_MASK
            self.memory_write(addr, value)
            return
        
        # register
        if encoding in OPERAND_TO_REGISTER:
            reg = OPERAND_TO_REGISTER[encoding]
            self.regs[reg] = value
            return
        
        # @register
        if encoding in REGISTER_INDIRECT:
            reg = REGISTER_INDIRECT[encoding]
            addr = self.regs[reg]
            self.memory_write(addr, value)
            return
        
        # @literal
        if encoding == 0x1F:
            addr = self.operand_immediate(decoded, operand_index)
            self.memory_write(addr, value) 
            return
        
        if encoding in REGISTER_PLUS_K:
            reg = REGISTER_PLUS_K[encoding]
            k = self.operand_immediate(decoded, operand_index)
            addr = (self.regs[reg] + k) & WORD_MASK
            self.memory_write(addr, value)
            return
        
        raise NotImplementedError(f"write operand {encoding:#x}")

    # ALU-type operations
    def execute_set(self, decoded: DecodedInstruction) -> None:
        """op1 = op2"""
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, b & WORD_MASK)
        self.advance_pc()
    
    def execute_and(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 & op2 """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, (a & b) & WORD_MASK)
        self.advance_pc()

    def execute_or(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 | op2"""
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, (a | b) & WORD_MASK)
        self.advance_pc()

    def execute_xor(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 ^ op2"""
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, (a ^ b) & WORD_MASK)
        self.advance_pc()

    def execute_add(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 + op2, REG[tm] = 0x0001 if overflow else 0x0"""
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)

        result = a + b
        self.regs[Reg.TM] = (0x0001 if result > WORD_MASK else 0x0000)

        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    def execute_sub(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 - op2, REG[tm] = 0xffff if underflow else 0x0"""
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)

        result = a - b
        self.regs[Reg.TM] = 0xFFFF if result < 0 else 0x0000
        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()
    
    def execute_mulu(self, decoded: DecodedInstruction) -> None:
        """op1 = op1 * op2 (unsigned), REG[tm] = ((op1 * op2) >> 16) & 0xffff (unsigned)"""
        a = self.read_operand(decoded, 1) & WORD_MASK
        b = self.read_operand(decoded, 2) & WORD_MASK
        product = a * b
        self.regs[Reg.TM] = (product >> 16) & WORD_MASK
        self.write_operand(decoded, 1, product & WORD_MASK)
        self.advance_pc()

    def execute_muls(self, decoded: DecodedInstruction) -> None:
        """mulu but signed"""
        a = to_signed16(self.read_operand(decoded, 1))
        b = to_signed16(self.read_operand(decoded, 2))
        product = a * b
        self.regs[Reg.TM] = (product >> 16) & WORD_MASK
        self.write_operand(decoded, 1, product & WORD_MASK)
        self.advance_pc()

    def execute_divu(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op1 / op2 (unsigned), 
        WORKING ASSUMPTION: REG[tm] = ((op1 << 16) / op2) & 0xffff
        if op2 != 0 else 0x0
        """
        dividend = self.read_operand(decoded, 1) & WORD_MASK
        divisor = self.read_operand(decoded, 2) & WORD_MASK

        if divisor == 0:
            self.regs[Reg.TM] = 0
            self.write_operand(decoded, 1, 0)
            self.advance_pc()
            return
        
        quotient = dividend // divisor
        remainder = dividend % divisor

        self.regs[Reg.TM] = ((remainder << 16) // divisor) & WORD_MASK
        self.write_operand(decoded, 1, quotient & WORD_MASK) # word mask
        self.advance_pc()
 
    def execute_divs(self, decoded: DecodedInstruction) -> None:
        """divu but signed, note that // rounds toward negative infinity
        so we use int(dividend / divisor) instead"""
        dividend = to_signed16(self.read_operand(decoded, 1))
        divisor = to_signed16(self.read_operand(decoded, 2))

        if divisor == 0:
            self.regs[Reg.TM] = 0
            self.write_operand(decoded, 1, 0)
            self.advance_pc()
            return
        
        quotient = int(dividend / divisor) # truncates towards zero
        remainder = dividend - quotient * divisor
        self.regs[Reg.TM] = (((remainder << 16) // abs(divisor)) & WORD_MASK)
        self.write_operand(decoded, 1, quotient & WORD_MASK)
        self.advance_pc()

    def execute_modu(self, decoded: DecodedInstruction) -> None:
        """op1 = (op1 % op2) if op2 != 0 else 0"""
        a = self.read_operand(decoded, 1) & WORD_MASK
        b = self.read_operand(decoded, 2) & WORD_MASK

        if b == 0:
            self.write_operand(decoded, 1, 0)
            self.advance_pc()
            return

        result = a % b
        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    def execute_mods(self, decoded: DecodedInstruction) -> None:
        """modu and we also take note of that // quirk from divs"""
        sa = to_signed16(self.read_operand(decoded, 1))
        sb = to_signed16(self.read_operand(decoded, 2))

        if sb == 0:
            self.write_operand(decoded, 1, 0)
            self.advance_pc()
            return
        
        q = int(sa / sb) # truncates towards zero
        r = sa - q * sb
        
        self.write_operand(decoded, 1, r & WORD_MASK)
        self.advance_pc()

    def execute_srl(self, decoded: DecodedInstruction) -> None:
        """
        WORKING ASSUMPTION: 
        original_op1 = x
        result = x >> shift
        tm = ((x << 16) >> shift) & 0xffff
        instead of project specs, so tm can act as carry-out bits
        """
        a = self.read_operand(decoded, 1) & WORD_MASK
        shift = self.read_operand(decoded, 2) & WORD_MASK

        result = a >> shift

        self.regs[Reg.TM] = ((a << 16) >> shift) & WORD_MASK

        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    def execute_sra(self, decoded: DecodedInstruction) -> None:
        """srl with signed interpretation"""
        unsigned_a = self.read_operand(decoded, 1) & WORD_MASK
        signed_a = to_signed16(unsigned_a)
        shift = self.read_operand(decoded, 2) & WORD_MASK
        result = signed_a >> shift

        self.regs[Reg.TM] = ((unsigned_a << 16) >> shift) & WORD_MASK
        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    def execute_sll(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op1 << op2
        REG[tm]  = ((op1 << op2) >> 16) & 0xffff
        """
        a = self.read_operand(decoded, 1) & WORD_MASK
        shift = self.read_operand(decoded, 2) & WORD_MASK

        full = a << shift

        self.regs[Reg.TM] = (full >> 16) & WORD_MASK

        self.write_operand(decoded, 1, full & WORD_MASK)
        self.advance_pc()

    # Branch-Control Flow-type operations

    # the branch helper
    def branch(self, condition: bool) -> None:
        self.regs[Reg.PC] = (self.next_pc() if condition else self.next_next_pc())

    def execute_jmp(self, decoded: DecodedInstruction) -> None:
        """
        REG[sp] -= 1
        MEM[REG[sp]] = NextPC
        PC = op1
        """
        target = self.read_operand(decoded, 1) & WORD_MASK
        self.regs[Reg.SP] = (self.regs[Reg.SP] - 1) & WORD_MASK
        self.memory_write(self.regs[Reg.SP], self.next_pc())
        self.regs[Reg.PC] = target
    
    def execute_ifany(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 & op2 != 0) else PC = NextNextPC
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.branch((a & b) != 0)
    
    def execute_ifnon(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 & op2 == 0) else PC = NextNextPC
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.branch((a & b) == 0)


    def execute_ifeq(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 == op2) else PC = NextNextPC
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.branch(a == b)
    
    def execute_ifne(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 != op2) else PC = NextNextPC
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)
        self.branch(a != b)

    def execute_ifgtu(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 > op2) else PC = NextNextPC (unsigned)
        """
        a = self.read_operand(decoded, 1) & WORD_MASK
        b = self.read_operand(decoded, 2) & WORD_MASK
        self.branch(a > b)

    def execute_ifgts(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 > op2) else PC = NextNextPC (signed)
        """
        a = to_signed16(self.read_operand(decoded, 1))
        b = to_signed16(self.read_operand(decoded, 2))
        self.branch(a > b)
    
    def execute_ifltu(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 < op2) else PC = NextNextPC (unsigned)
        """
        a = self.read_operand(decoded, 1) & WORD_MASK
        b = self.read_operand(decoded, 2) & WORD_MASK
        self.branch(a < b)
    
    def execute_iflts(self, decoded: DecodedInstruction) -> None:
        """
        PC = NextPC if (op1 < op2) else PC = NextNextPC (signed)
        """
        a = to_signed16(self.read_operand(decoded, 1))
        b = to_signed16(self.read_operand(decoded, 2))
        self.branch(a < b)

    # Other Instructions

    def execute_addt(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op1 + op2 + REG[tm]
        REG[tm] = 0x0001 if overflow else 0x0
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)

        # make sure TM is a 16-bit register
        tm = self.regs[Reg.TM] & WORD_MASK
        result = a + b + tm
        self.regs[Reg.TM] = (0x0001 if result > WORD_MASK else 0x0000)

        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    
    def execute_subt(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op1 - op2 + REG[tm]
        REG[tm] = 0xffff if underflow else 0x0
        """
        a = self.read_operand(decoded, 1)
        b = self.read_operand(decoded, 2)

        # NOTE: ambiguous whether REG[tm] is supposed to be treated as a 
        # signed/unsigned value, assuming unsigned for now
        tm = self.regs[Reg.TM] & WORD_MASK

        result = a - b + tm
        self.regs[Reg.TM] = (0xFFFF if result < 0 else 0x0000)
        self.write_operand(decoded, 1, result & WORD_MASK)
        self.advance_pc()

    def execute_seti(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op2
        REG[gg] += 1
        REG[gh] += 1
        """
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, b & WORD_MASK)
        self.regs[Reg.GG] = (self.regs[Reg.GG] + 1) & WORD_MASK
        self.regs[Reg.GH] = (self.regs[Reg.GH] + 1) & WORD_MASK
        self.advance_pc()


    def execute_setd(self, decoded: DecodedInstruction) -> None:
        """
        op1 = op2
        REG[gg] -= 1
        REG[gh] -= 1
        """
        b = self.read_operand(decoded, 2)
        self.write_operand(decoded, 1, b & WORD_MASK)
        self.regs[Reg.GG] = (self.regs[Reg.GG] - 1) & WORD_MASK
        self.regs[Reg.GH] = (self.regs[Reg.GH] - 1) & WORD_MASK
        self.advance_pc()

    def step(self):
        """
        Executes one Arch-252 instruction.
        """
        decoded = self.decode()
        # print(f"pc={self.regs[Reg.PC]:04X}", disassemble(decoded))        
        handler = self.handlers.get(decoded.opcode)

        if handler is None:
            raise NotImplementedError(
                f"opcode {decoded.opcode:#x}"
                f"({INSTRUCTIONS.get(decoded.opcode, '???')})"
            )
        
        handler(decoded)

        self.instructions_executed += 1
        self.tick_counter = (self.tick_counter + 1) & WORD_MASK # 16-bit value

class Display:
    def __init__(self, cpu: CPU, seed: int, ipf: int, cell_size: int = 8) -> None: # 8 chosen as cell_size
        self.cpu = cpu
        self.cell_size = cell_size
        self.instructions_per_frame = ipf
        self.width = DISPLAY_WIDTH * cell_size
        self.height = DISPLAY_HEIGHT * cell_size

        # initialize dawnbringer hex codes here
        # split into triples for easier quantization
        self.DAWNBRINGER16 = [
            (0x4e,0x4a,0x4e),	 # emperor	
            (0x44,0x24,0x34),	 # livid brown	
            (0x30,0x34,0x6d),	 # rhino	
            (0x85,0x4c,0x30),	 # mule fawn
            (0x34,0x65,0x24),	 # woodland	
            (0x75,0x71,0x61),	 # pablo	
            (0xd0,0x46,0x48),	 # flush mahogany	
            (0x59,0x7d,0xce),	 # danube	
            (0xd2,0x7d,0x2c),	 # brandy punch	
            (0x6d,0xaa,0x2c),	 # olive drab	
            (0x85,0x95,0xa1),	 # regent gray	
            (0xd2,0xaa,0x99),	 # eunry	
            (0x6d,0xc2,0xca),	 # downy	
            (0xda,0xd4,0x5e),	 # tacha	
            (0x14,0x0c,0x1c),	 # ebony	
            (0xde,0xee,0xd6),	 # zanah
        ]
        rng = random.Random(seed)
        self.random_grid = [
            rng.randrange(16)
            for _ in range(DISPLAY_PIXELS)
        ]

        pyxel.init(
            self.width,
            self.height,
            title="Arch-252 Emulator",
        )

        for i, (r, g, b) in enumerate(self.DAWNBRINGER16):
            pyxel.colors[i] = (r << 16) | (g << 8) | b
        
        for y in range(DISPLAY_HEIGHT):
            for x in range(DISPLAY_WIDTH):
                pixel = cpu.front_buffer[y * 32 + x]
                color = self.quantize(pixel)
                pyxel.pset(x, y, color)
    
    def unpack_rgb(self, pixel: int) -> tuple[int, int, int]:
        # given a 32-bit value 0x00RRGGBB, get (RR, GG, BB)
        r = (pixel >> 16) & 0xFF
        g = (pixel >>  8) & 0xFF
        b = pixel & 0xFF
        return r, g, b

    def update(self) -> None:
        self.cpu.set_input_button(pyxel.btn(pyxel.KEY_SPACE))

        for _ in range(self.instructions_per_frame):
            self.cpu.step()

    def draw(self) -> None:
        pyxel.cls(0)

        for y in range(DISPLAY_HEIGHT):
            for x in range(DISPLAY_WIDTH):
                pixel = self.cpu.front_buffer[y * DISPLAY_WIDTH + x]
                color = self.quantize(pixel)
                # color = self.random_grid[y * DISPLAY_WIDTH + x] # for random colors
                pyxel.rect(
                    x * self.cell_size, 
                    y * self.cell_size, 
                    self.cell_size, 
                    self.cell_size, 
                    color
                )

    def run(self) -> None:
        pyxel.run(self.update, self.draw)
    
    def quantize(self, pixel) -> int:
        r, g, b = self.unpack_rgb(pixel)

        best_index = 0
        best_dist = float("inf")

        for i, (pr, pg, pb) in enumerate(self.DAWNBRINGER16):
            dist = (
                (r - pr)**2 +
                (g - pg)**2 + 
                (b - pb)**2
            )

            if dist < best_dist:
                best_dist = dist
                best_index = i
            
        return best_index # 16-bit value

    def draw_information_panel(self):
        # function saved for phases 16-17
        ...

# mapping for @register+k
REGISTER_PLUS_K = {
    0x10: Reg.GA,
    0x11: Reg.GB,
    0x12: Reg.GC,
    0x13: Reg.GD,
    0x14: Reg.GE,
    0x15: Reg.GF,
    0x16: Reg.GG,
    0x17: Reg.GH,
}

# mapping for indirect-register operands
REGISTER_INDIRECT = {
    0x08: Reg.GA,
    0x09: Reg.GB,
    0x0a: Reg.GC,
    0x0b: Reg.GD,
    0x0c: Reg.GE,
    0x0d: Reg.GF,
    0x0e: Reg.GG,
    0x0f: Reg.GH,
}

# mapping for actual register operands
OPERAND_TO_REGISTER = {
    0x1c: Reg.PC,
    0x1b: Reg.SP,
    0x1d: Reg.TM,
    0x00: Reg.GA,
    0x01: Reg.GB,
    0x02: Reg.GC,
    0x03: Reg.GD,
    0x04: Reg.GE,
    0x05: Reg.GF,
    0x06: Reg.GG,
    0x07: Reg.GH,
}

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

def operand_has_immediate(operand_encoding: int) -> bool:
    return operand_encoding in {
        0x10, # @ga+k
        0x11, # @gb+k
        0x12, # @gc+k
        0x13, # @gd+k
        0x14, # @ge+k
        0x15, # @gf+k
        0x16, # @gg+k
        0x17, # @gh+k
        0x1A, # @peek+k
        0x1E, # literal
        0x1F, # @literal
    }


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

def to_signed16(x: int) -> int:
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x

# debug functions
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

def run_headless(bin_path: str, instruction_count: int, seed: int) -> CPU:
    if instruction_count < 0:
        raise ValueError("ipf must be non-negative")

    memory = load_binary(bin_path)
    cpu = CPU(memory, seed)

    for _ in range(instruction_count):
        cpu.step()

    return cpu

def print_run_summary(bin_path: str, ipf: int, seed: int, cpu: CPU) -> None:
    print(f"bin file = {bin_path}")
    print(f"ipf      = {ipf}")
    print(f"seed     = {seed}")
    print(f"executed = {cpu.instructions_executed}")
    print(f"tick     = {cpu.tick_counter:04X}")
    print(f"pc       = {cpu.regs[Reg.PC]:04X}")
    dump_registers(cpu)

def disassemble(decoded: DecodedInstruction) -> str:
    mnemonic = INSTRUCTIONS.get(
        decoded.opcode,
        f"unknown_{decoded.opcode:02X}"
    )
    return (
        f"{mnemonic}"
        f"(op1={decoded.op1_encoding:04X})"
        f"(op2={decoded.op2_encoding:04X})"
    )

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 emulator.py <bin-filepath> <ipf> <seed>")
        sys.exit(1)

    bin_path = sys.argv[1]
    ipf = int(sys.argv[2])
    seed = int(sys.argv[3])

    if ipf < 0:
        raise ValueError("ipf must be non-negative")

    memory = load_binary(bin_path)
    cpu = CPU(memory, seed)
    Display(cpu=cpu, seed=seed, ipf=ipf).run()

if __name__ == "__main__":
    main()
