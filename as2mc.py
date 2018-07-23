from encoding import get_reg_encode

class assembler:
    def __init__(self):
        self.reg = get_reg_encode()
        self.insn_opcode = dict()
        self.insn_type = dict()
        self.insn_func = dict()

    def add_insn(self, name, t, opcode, func):
        self.insn_opcode[name] = opcode << 0
        self.insn_func[name]   = func   << 12
        self.insn_type[name]   = t

    def add_zero_in_ahead(self, target, l):
        while len(target) < l:
            target = '0' + target
        return target

    def gen_code(self, insn):
        encode = 0b0
        apart = [i.strip(' ,') for i in insn.split(' ')]
        name = apart[0]
        if self.insn_type[name] == 'I':
            name, rd, rs1 = apart
        encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rd] << 7 | self.reg[rs1] << 15
        return encode

if __name__=='__main__':
    a = assembler()
    a.add_insn('setvl', 'I', 0b0001011, 0)
    a.add_insn('vld'  , 'I', 0b0001011, 1)
    a.add_insn('vadd' , 'I', 0b0001011, 2)
    a.add_insn('vst'  , 'I', 0b0001011, 3)
    code = []
    code.append('setvl a5, a5')
    code.append('vld v0, a0')
    code.append('vadd v0, v0')
    code.append('vst v0, a0')
    inline_asm = [hex(a.gen_code(i)) for i in code]
    print(inline_asm)
    