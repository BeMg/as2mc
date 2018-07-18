from encoding import get_reg_encode

class assembler:
    def __init__(self):
        self.reg = get_reg_encode()
        self.insn_opcode = dict()
        self.insn_type = dict()
        self.insn_func = dict()

    def add_insn(self, name, t, opcode, func):
        self.insn_opcode[name] = opcode
        self.insn_func[name] = func
        self.insn_type[name] = t

    def add_zero_in_ahead(self, target, l):
        while len(target) < l:
            target = '0' + target
        return target

    def gen_code(self, insn):
        apart = [i.strip(' ,') for i in insn.split(' ')]
        name = apart[0]
        rd = ''
        rs1 = ''
        rs2 = ''
        imm12 = ''
        load_flag = False

        if self.insn_type[name] == 'I':
            name, rd, rs1 = apart
        if '(' in rs1 or ')' in rs1:
            load_flag = True
            imm12, rs1 = [i.strip('() ') for i in rs1.split('(')]
        
        imm12 = str(bin(int(imm12))[2:])
        imm12 = self.add_zero_in_ahead(imm12, 12)

        print(name)
        print(rd)
        print(rs1)
        print(imm12)

        represtion = list('0' * 32)
        represtion[25:32] = self.insn_opcode[name] # opcode [6:2]
        represtion[12:17] = self.add_zero_in_ahead(str(bin(self.reg[rs1])[2:]), 5)
        represtion[17:20] = self.insn_func[name] # func [14:12]
        represtion[20:25] = self.add_zero_in_ahead(str(bin(self.reg[rd])[2:]), 5)
        represtion[0:12] = imm12 # imm12 [31:20]

        print(''.join(represtion))


if __name__=='__main__':
    a = assembler()
    a.add_insn('vld', 'I', '0001011', '001')
    a.gen_code('vld v0, 0(a0)')