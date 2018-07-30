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
        # Type classification by format below
        # 1 -> name imm20
        # 2 -> name rd, rs1
        # 3 -> name rd, rs1, rs2
        # 4 -> name rd, imm12(rs1) for load 
        # 5 -> name rd, rs1, imm12
        # 6 -> name rs1, imm12(rs2) for store
        self.insn_type[name]  = t

    def add_zero_in_ahead(self, target, l):
        while len(target) < l:
            target = '0' + target
        return target

    def gen_code(self, insn):
        encode = 0b0
        apart = [i.strip(' ,') for i in insn.split(' ')]
        name = apart[0]
        type_of_insn = self.insn_type[name] 

        if type_of_insn == 2:
            name, rd, rs1 = apart
            encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rd] << 7 | self.reg[rs1] << 15
        elif type_of_insn == 1:
            name, imm20 = apart
            encode = encode | self.insn_opcode[name] | int(imm20) << 12
        elif type_of_insn == 3:
            name, rd, rs1, rs2 = apart
            encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rd] << 7 | self.reg[rs1] << 15 | self.reg[rs2] << 20
        elif type_of_insn == 4:
            name, rd, target = apart
            imm12, rs1 = [i.strip(')') for i in target.split('(')]
            encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rd] << 7 | self.reg[rs1] << 15 | int(imm12) << 20
        elif type_of_insn == 5:
            name, rd, rs1, imm12 = apart
            encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rd] << 7 | self.reg[rs1] << 15 | int(imm12) << 20
        elif type_of_insn == 6:
            name, rs1, target = apart
            imm12, rs2 = [i.strip(')') for i in target.split('(')]
            imm12 = int(imm12)
            imm0_4 = imm12 & 0b11111
            imm5_12 = imm12 >> 5
            encode = encode | self.insn_opcode[name] | self.insn_func[name] | self.reg[rs1] << 15 | self.reg[rs2] << 20 | imm0_4 << 7 | imm5_12 << 25
        else:
            raise Exception('No this type')

        return encode

if __name__=='__main__':
    a = assembler()
    a.add_insn('setvl', 2, 0b0001011, 0)
    a.add_insn('vld'  , 2, 0b0001011, 1)
    a.add_insn('vadd' , 2, 0b0001011, 2)
    a.add_insn('vst'  , 2, 0b0001011, 3)
    code = []
    code.append('setvl a5, a5')
    code.append('vld v0, a0')
    code.append('vadd v0, v0')
    code.append('vst v0, a0')
    inline_asm = [hex(a.gen_code(i)) for i in code]
    