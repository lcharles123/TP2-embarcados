import sys







#recebe uma tupla com a instrucao + operadores e retorna uma tupla com a linha atual a proxima do codigo de maquina
# formato das instrucoes:[inst][op1] + [op2]

def traduzir(inst):
    linha1 = instrucao[inst[0]] # pega os bits da instrucao
    linha2 = 0
    
    if inst in ["load","store","jmpz","jmpn"]: # formato [0,3] [0,127] # [0000_0][00][0 0000_0000]
        linha1 += 
        linha2 = inst[1] 
    elif inst in ["read", "write", "push", "pop", "copytop"]: # formato [0,3] # [0000_0][xx][x xxxx_xx00]
        linha2 = inst[1]
    elif inst in ["add", "subtract", "multiply", "divide", "move", "loadi", "storei"]: # formato [0,3] [0,3] # [0000_0][00][x xxxx_xx00]
        linha2 = inst[1]
    elif inst in ["jump", "call"]: # formato [0,127] # [0000_0][xx][0 0000_0000]
        linha2 = inst[1]
    elif inst in ["load_s", "store_s"]: # formato [0,3] [0,255] # [0000_0][00][0 0000_0000]
        linha2 = inst[1]
    elif inst in ["loadc"]: # formato [0,3] imm(9bits) # [0000_0][00][0 0000_0000]
        linha2 = inst[1]
    elif inst in ["return"]: # formato 0x8000 # [xxxx_xxxx][xxxx_xxxx] 
        linha2 = inst[1] # inserir pop aqui
    elif inst in ["stop"]: # formato 0 # [xxxx_xxxx][xxxx_xxxx]
        linha2 = inst[1]
    else:
        raise ValueError("Instrucao ilegal")
        
    
    
    return int(linha1, 2) , int(linha2, 2)


instrucao = {  # intervalos dos operandos, colocar na segunda linha, [0,3]-> regs [0,127]->mem, 0->nenhum
"stop": '00000',      # 0
"load": '00001',      # [0,3] [0,127]
"store": '00010',     # [0,3] [0,127]
"read": '00011',      # [0,3]
"write": '00100',     # [0,3]
"add": '00101',       # [0,3] [0,3]
"subtract": '00110',  # [0,3] [0,3]
"multiply": '00111',  # [0,3] [0,3]
"divide": '01000',    # [0,3] [0,3]
"jump": '01001',      # [0,127]
"jmpz": '01010',     # [0,3] [0,127]
"jmpn": '01011',     # [0,3] [0,127]
"move": '01100',     # [0,3] [0,3]
"push": '01101',     # [0,3]
"pop": '01110',      # [0,3]
"call": '01111',     # [0,127]
"return": '00000',# 0x8000 ??
"load_s": '10001',   # [0,3] [0,255]
"store_s": '10010',  # [0,3] [0,255]
"loadc": '10011',    # [0,3] imm(9bits)
"loadi": '10100',    # [0,3] [0,3]
"storei": '10101',   # [0,3] [0,3]
"copytop": '10110',  # [0,3]
}

registrador = {
"A0": '00',
"A1": '01',
"A2": '10',
"A3": '11'
}

#  :0100010024DA 
#  cada linha = 8 bits (1 byte) == na memoria, duas linhas para formar uma instrucao. int possui 2 bytes = 16 bits
# inicio + numbytes + end + tipo              +    dado + cks
#          sempre 01        00(data), 01(EOF)
#   :        01      0001    00                     24    DA 
#                                                  soma = 26
#   receber os dados como uma lista de 128 posicoes, em formato int, mas pode ser string tb
def imprimir(dados, arquivo='stdout', formato='hex'):
    
    if formato == 'hex':  
        cks = lambda e, t, d : h((~(e+t+d)) & 0xffff) # 2's da soma de end, tipo, data, retorna str
        h = lambda i : "{:02X}".format(i)[-2:]
        linhas = []
        for i in range(127):
            linhas.append(':0100' + h(i) + '00' + h(dados[i]) + cks(i,0, dados[i]) )
        
        linhas.append(':0100' + h(127) + '01' + '00' + cks(i,1, 0) )
        
        if arquivo == 'stdout':
            for linha in linhas:
                print(linha)
        else:
            with open(arquivo, 'w') as f:
                for linha in linhas:
                    print(linha, file=f, end="")
                    print("")
                print("", end="")
        
    else:
        raise NotImplemented('mif')






def main():
    argc = len(sys.argv)
    if argc not in [2,3]:
        if argc == 1:
            raise ValueError("ERRO: sem arquivos de entrada")
        elif argc > 3:
            raise ValueError("ERRO: excesso de argumentos")
        '''Forma de uso: python3 main.py asm_Swombat.a arqsaida(.hex)'''
        exit(1)
    
    formato = "hex"
    #saida = sys.argv[2]
    saida = "stdout"    
    linhas = [0] * 127 # linhas do codigo de maquina
    
    entrada = sys.argv[1]
    with open(entrada, 'r') as f:
        linha = f.readline()
        while linha:
            
            
            #print(linha.strip()) #aqui temos cada linha sem o newline pode ser processada uma a uma
            
            
            linha = f.readline()
    
    exit(0) 
    print(traduzir(('load','A1',133)))
    print(traduzir(()))
    print(traduzir(()))
    
    linhas = [10,36,12] #cada entrada representa uma linha no arquivo hex/mif
    linhas += [0] * 127
    imprimir(linhas)
   
   

main()
