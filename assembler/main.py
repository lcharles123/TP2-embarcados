import sys

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
"return": '10000',# 0x8000
"load_s": '10001',   # [0,3] [0,255]
"store_s": '10010',  # [0,3] [0,255]
"load_c": '10011',    # [0,3] imm(9bits)
"load_i": '10100',    # [0,3] [0,3]
"store_i": '10101',   # [0,3] [0,3]
"copytop": '10110',  # [0,3]
".data": '00000',  # [0,3]
"x" : '00000'        # caso default: dont care
}

reg = {
"A0": '00',
"A1": '01',
"A2": '10',
"A3": '11',
"x" : '00' # caso default: dont care
}

#recebe uma tupla com a instrucao + operadores e retorna uma tupla com a linha atual a proxima do codigo de maquina
# formato das instrucoes:[inst][op1] + [op2]
def traduzir(linha):
    inst = linha[0]
    op1 = linha[1]
    op2 = linha[2]
    
    linha1 = instrucao[inst] # pega os bits da instrucao
    linha2 = 0
    
    b = lambda i : format(int(i), '016b') # transforma i sem sinal em binario 16 bits
    
    if inst == '.data':
        h = lambda i : "{:02b}".format(i) # converte um numero para string binaria
        op1 = int(op1)
        linha2 = b(int(op2) & 0xffff)[8:16]
        if op1 == 2: # tamanho do dado
            linha1 = b(int(op2) & 0xffff)[0:8]
        elif op1 == 1:
            linha1 = '00000000' # se o dado possui apenas 1 byte
        else:
            print(inst,op1,op2)
            raise ValueError("Tamanho do dado != 1 ou 2 bytes")
    elif inst in ["load","store","jmpz","jmpn"]: # formato [0,3] [0,127] # [0000_0][00][0 0000_0000]
        linha1 += reg[op1] + '0' # concatena com end registrador + 0 do end memoria, possivel pois so existem 127 pos na memoria
        linha2 = b(op2)[8:16]
    elif inst in ["read", "write", "push", "pop", "copytop"]: # formato [0,3] # [0000_0][xx][x xxxx_xx00]
        linha1 += '000' # concat para formar linha1
        linha2 = '000000'+ reg[op1]
    elif inst in ["add", "subtract", "multiply", "divide", "move", "load_i", "store_i"]: # formato [0,3] [0,3] # [0000_0][00][x xxxx_xx00]
        linha1 += reg[op1] + '0'
        linha2 = '000000' + reg[op2]
    elif inst in ["jump", "call"]: # formato [0,127] # [0000_0][xx][0 0000_0000]
        linha1 += '000'
        linha2 = b(op1)[8:16]
    elif inst in ["load_s", "store_s"]: # formato [0,3] [0,255] # [0000_0][00][0 0000_0000]
        linha1 += reg[op1] + '0'
        linha2 = '1' # TODO
    elif inst in ["load_c"]: # formato [0,3] imm(9bits) # [0000_0][00][0 0000_0000]
        bsinal = '0'
        if int(op2) < 0 :
            bsinal = '1'
        linha1 += reg[op1] + bsinal # este eh o bit de sinal, caso o imm(9bits) seja < 0
        linha2 = b(op2)[8:16]
    elif inst in ["return"]: # formato 0x8000 # [xxxx_xxxx][xxxx_xxxx] 
        linha1 += '000'
        linha2 = '00000000' # TODO
    elif inst in ["stop"]: # formato 0 # [xxxx_xxxx][xxxx_xxxx]
        linha1 += '000'
        linha2 = '00000000' # TODO
    else:
        print(linha)
        raise ValueError("Instrucao ilegal")
        
    
    
    return int(linha1, 2) , int(linha2, 2)
    return linha1 , linha2 #int(linha2, 2)

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
                    lin = lin.split(";", 1) # obtem a primeira parte da linha, sem o comentario
                    #print( lin[0].split()) # aqui temos a linha nao vazia e sem comentarios e com o endereco no programa
                    linha = lin[0].split()
                    if linha[0] not in instrucao.keys(): # guardar o endereco das referencias em um dict{'label': end} , passo 1
                        refs[linha[0][:-1]] = numLinha
                        del linha[0] #deletar os labels para deixar apenas instrucoes
                    
                    codigoTratado.append([str(numLinha)] + linha)
                    
                    numLinha += 2 
            #print(linha.strip()) #aqui temos cada linha sem o newline pode ser processada uma a uma
            linha = f.readline()
    #exit(0)
    for i in codigoTratado:
        print(i)
    #exit(0)
    for inst in codigoTratado: # segundo passo: substituir os labels pelos enderecos
        if inst[1] in ["load","store","jmpz","jmpn"]:  # se formato inst A0 label
            inst[3] = refs[inst[3]]                 # substitui o label pelo end
        elif inst[1] in ["jump","call"]:
            inst[2] = refs[inst[2]] 
        
    
    for i in codigoTratado:
        print(i)
    print("")
    print (refs)
    for i, inst in enumerate(codigoTratado): # agora basta traduzir as instrucoes 1:1     
        if len(inst) == 2: # inst tamanho 1
            #continue
            #print(inst)
            #print(traduzir([inst[1], 'x', 'x']))  
            l1, l2 = traduzir([inst[1], 'x', 'x'])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        elif len(inst) == 3: # inst de tamanho 2
            #continue
            #print(inst)
            #print(traduzir([inst[1], inst[2], 'x']))
            l1, l2 = traduzir([inst[1], inst[2], 'x'])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        elif len(inst) == 4: # inst de tamanho 3
            #continue
            #print(inst)
            #print(traduzir(inst[1:]))
            l1, l2 = traduzir(inst[1:])
            codMaquina[2*i] = l1
            codMaquina[2*i+1] = l2
        else:
            print(inst)
            raise ValueError("Instrucao fora do padrao")
       
    #exit(0)
    #h = lambda i : "{:02X}".format(i)[-2:] 
    for i in codMaquina:
        print(i)
    #exit(0)
    print(traduzir(('load','A1','133')))
    
    #codMaquina = [10,36,12] #cada entrada representa uma linha no arquivo hex/mif
    imprimir(codMaquina)
   
   

main()


