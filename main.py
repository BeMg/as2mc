import sys
from as2mc import assembler


if __name__=='__main__':
    a = assembler()
    a.add_insn('setvl', 'I', 0b0001011, 0)
    a.add_insn('vld'  , 'I', 0b0001011, 1)
    a.add_insn('vadd' , 'I', 0b0001011, 2)
    a.add_insn('vst'  , 'I', 0b0001011, 3)

    while True:
        command = input('> ')
        try:
            encode = a.gen_code(command)
            print(hex(encode))
        except:
            print('Bad Format')
