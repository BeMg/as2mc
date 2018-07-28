import sys
from as2mc import assembler


if __name__=='__main__':
    a = assembler()
    a.add_insn('setvl', 2, 0b0001011, 0)
    a.add_insn('vld'  , 2, 0b0001011, 1)
    a.add_insn('vadd' , 2, 0b0001011, 2)
    a.add_insn('vst'  , 2, 0b0001011, 3)
    a.add_insn('vconfig', 1, 0b0101011, -1)
    a.add_insn('addi', 5, 0b0010011, 0)

    while True:
        command = input('> ')
        try:
            encode = a.gen_code(command)
            print(hex(encode))
        except:
            print('Bad Format')
