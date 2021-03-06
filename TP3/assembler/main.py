import sys

#inicialmente temos a tabela de simbolos externos vazia, mas sera preenchida na forma endNoCod:(tipo,target) 
externos = {"tam" : 0, 0 : (None,) }

instrucao = {  #  intervalos dos operandos, colocar na segunda linha, [0,3]-> regs [0,127]->mem, 0->nenhum
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
"jmpz": '01010',      # [0,3] [0,127]
"jmpn": '01011',      # [0,3] [0,127]
"move": '01100',      # [0,3] [0,3]
"push": '01101',      # [0,3]
"pop": '01110',       # [0,3]
"call": '01111',      # [0,127]
"return": '10000',    # 0x8000
"load_s": '10001',    # [0,3] [0,255]
"store_s": '10010',   # [0,3] [0,255]
"load_c": '10011',    # [0,3] imm(9bits)
"load_i": '10100',    # [0,3] [0,3]
"store_i": '10101',   # [0,3] [0,3]
"copytop": '10110',   # [0,3]
".data": '00000',     # [0,3]

".externD":'ed',   #dado externo
".externT":'et',   #text externo
".globalD":'gd',   #dado acessivel a outros modulos
".globalT":'gt',   #procedimento acessivel a outros modulos

"x" : '00000'      #caso default: dont care
}

reg = {
"A0": '00',
"A1": '01',
"A2": '10',
"A3": '11',
"x" : '00' #caso default: dont care
}

'''funçao para salvar e carregar a tabela de simbolos para um arquivo'''
def salvar_dict(arq, dic):
    f = open(arq,'w')
    f.write(str(dic))
    f.close() 

'''recebe a instrucao e operadores e retorna 2 elementos: a linha atual a proxima do codigo de maquina'''
def traduzir(linha):
    inst = linha[0]
    op1 = linha[1]
    op2 = linha[2]
    
    linha1 = instrucao[inst] # pega os bits da instrucao
    linha2 = '00000000'
    
    b = lambda i : format(int(i), '016b') # transforma i sem sinal em binario 16 bits
    
    if inst == '.data':
        h = lambda i : "{:02b}".format(i) # converte um numero para string binaria
        op1 = int(op1)
        linha2 = b(int(op2) & 0xffff)[8:16]
        if op1 == 2: # tamanho do dado
            linha1 = b(int(op2) & 0xffff)[0:8]
        else:
            print(inst,op1,op2)
            raise ValueError("Tamanho do dado != 1 ou 2 bytes")
    elif inst in ["load","store","jmpz","jmpn"]: # formato [0,3] [0,127] # [0000_0][00][0 0000_0000]
        linha1 += reg[op1] + '0' 
        linha2 = b(op2)[8:16]
    elif inst in ["read", "write", "push", "pop", "copytop"]: # formato [0,3] # [0000_0][xx][x xxxx_xx00]
        linha1 += '000'
        linha2 = '000000'+ reg[op1]
    elif inst in ["add", "subtract", "multiply", "divide", "move", "load_i", "store_i"]: # formato [0,3] [0,3] # [0000_0][00][x xxxx_xx00]
        linha1 += reg[op1] + '0'
        linha2 = '000000' + reg[op2]
    elif inst in ["jump", "call"]: # formato [0,127] # [0000_0][xx][0 0000_0000]
        linha1 += '000'
        linha2 = b(op1)[8:16]
    elif inst in ["load_s", "store_s"]: # formato [0,3] [0,255] # [0000_0][00][0 0000_0000]
        linha1 += reg[op1] + '0'
        linha2 = '1'
    elif inst in ["load_c"]: # formato [0,3] imm(9bits) # [0000_0][00][0 0000_0000]
        bsinal = '0'
        if int(op2) < 0 :
            bsinal = '1'
        linha1 += reg[op1] + bsinal # este eh o bit de sinal, caso o imm(9bits) seja < 0
        linha2 = b(op2)[8:16]
    elif inst in ["return", "stop"]: # formato 0x8000 # [0000_0][xxx][xxxx_xxxx] 
        linha1 += '000'
    elif inst in [".globalT", ".externT"]: #caso seja text
        externos[int(op2)] = (linha1, op1) # externos[endNoCod] = (tipo -> target) 
        linha1 = '11111111' # esta instrucao diz ao ligador que o simbolo aponta para fora FF 00
    elif inst in [".globalD", ".externD"]: #caso seja dado
        externos[int(op2)] = (linha1, op1)  
        linha1 = '01111111' # equivalente a 7F 00
    else:
        print(linha)
        raise ValueError("Instrucao desconhecida.")
    
    return int(linha1, 2) , int(linha2, 2)

'''Recebe um vetor de ints que será tradizudo para o codigo de maquina'''
def imprimir(dados, arquivo='stdout', formato='hex'):
    
    if formato == 'hex':  
        cks = lambda e, t, d : h((~(e+t+d)) & 0xffff) # 2's da soma de end, tipo, data, retorna str
        h = lambda i : "{:02X}".format(i)[-2:]
        linhas = []
        for i in range(127):
            linhas.append(':0100' + h(i) + '00' + h(dados[i]) + cks(i,0, dados[i]) )
        linhas.append(':000000' + '01' + 'FF' )
        
        if arquivo == 'stdout':
            for linha in linhas:
                print(linha)
            print("Simbolos externos")
            print(externos)
            
        else:
            with open(arquivo, 'w') as f:
                for linha in linhas:
                    print(linha, file=f)
            salvar_dict(arquivo[:-4] + '.sym', externos)             
    else:
        raise NotImplemented('mif')


'''Função principal'''
def main():
    argc = len(sys.argv)
    if argc not in [2,3]:
        if argc == 1:
            raise ValueError("ERRO: sem arquivos de entrada")
        elif argc > 3:
            raise ValueError("ERRO: excesso de argumentos")
        exit(1)
    
    saida = sys.argv[2]
    codMaquina = [0] * 127 # linhas do codigo de maquina
    numLinha = 0 # ennumerar as linhas do codigo para substituir pelos labels
    codigoTratado = []
    refs = {}
    
    entrada = sys.argv[1]
    with open(entrada, 'r') as f:
        linha = f.readline()
        while linha:
            lin = linha.strip()
            if lin != '':
                if lin[0] != ';' :
                    lin = lin.split(";", 1)
                    linha = lin[0].split()
                    if linha[0] not in instrucao.keys(): 
                        refs[linha[0][:-1]] = numLinha
                        del linha[0] #deletar os labels para deixar apenas instrucoes
                    codigoTratado.append([str(numLinha)] + linha)
                    numLinha += 2 
            linha = f.readline()
            
    for i,inst in enumerate(codigoTratado):
        if inst[1] in ["load","store","jmpz","jmpn"]: 
            inst[3] = refs[inst[3]]                 
        elif inst[1] in ["jump","call"]:
            inst[2] = refs[inst[2]] 
        elif inst[1] in [".externD", ".externT", ".globalD", ".globalT"]: #caso o simbolo seja externo, colocar o rótulo como segundo operando
            codigoTratado[i].append(inst[0])
            if i == 0 and inst[1] == ".globalT" and inst[2] == "main": #indicar que é o programa principal
                externos[0] = ("main",)
                codigoTratado[0] = [0, "move", "A0", "A0"] # instrução equivalente a nop
    
    for i, inst in enumerate(codigoTratado): # agora basta traduzir as instrucoes 1:1     
        if len(inst) == 2: # inst tamanho 1
            l1, l2 = traduzir([inst[1], 'x', 'x'])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        elif len(inst) == 3: # inst de tamanho 2
            l1, l2 = traduzir([inst[1], inst[2], 'x'])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        elif len(inst) == 4: # inst de tamanho 3
            l1, l2 = traduzir(inst[1:])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        else:
            print(inst)
            raise ValueError("Instrucao desconhecida")
    
    codMaquina[2*len(codigoTratado)] = 254 #valor binario == '1111_1110', hex == 'FE' indica final do programa.
    codMaquina[2*len(codigoTratado)+1] = 254

    externos["tam"] = len(codigoTratado)*2+2 #tamanho do programa + a marcação de final
    
    imprimir(codMaquina, arquivo=saida)


main()


