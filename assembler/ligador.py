import sys
import os.path

'''funcao para carregar a tabela de simbolos para uma variavel'''
def carregar_dict(arq):
    f = open(arq,'r')
    data=f.read()
    f.close()
    return eval(data)

'''Recebe um vetor de ints que serao tradizudos para o codigo de maquina'''
def imprimir(dados, arquivo='stdout', formato='hex'):
    
    dadosAux = [0] * 127
    for i,d in enumerate(dados[:-1]):
        dadosAux[i] = int(d[1], 16) #converte dados em base16 para base10, para aproveitar a função abaixo do montador
    dados = dadosAux

    if formato == 'hex':  
        cks = lambda e, t, d : h((~(e+t+d)) & 0xffff) # 2's da soma de end, tipo, data, retorna str
        h = lambda i : "{:02X}".format(i)[-2:]
        linhas = []
        for i in range(127):
            linhas.append(':0100' + h(i) + '00' + h(dados[i]) +''+ cks(i,0, dados[i]) )
        linhas.append(':000000' + '01' + 'FF' )
        
        if arquivo == 'stdout':
            for linha in linhas:
                print(linha)
        else:
            with open(arquivo, 'w') as f:
                for linha in linhas:
                    print(linha, file=f)
    else:
        raise NotImplemented('mif')


def jump_de_volta(prog):
    for i in range(len(prog[:-1])):
        if prog[i][1] == 'FE' and prog[i+1][1] == 'FE':
            return prog[i][0]       
    else:
        raise Exception("ERRO o programa não possui marcação de parada")
    

'''Forma de uso: python3 main.py asm_Swombat.a arqsaida'''
def main():
    argc = len(sys.argv)
    if argc < 3:
        if argc == 1:
            raise ValueError("ERRO: quantidade de argumentos < 3")
    
    saidaFinal = sys.argv[-1] #arquivo de saida
    del sys.argv[-1]
    entradas = [] 
    
    for ent in sys.argv[1:]:
        if os.path.isfile(ent[:-3] + "sym") is False:
            raise Exception("ERRO ao abrir arquivo de símbolos: "+ arqTabela)
        entradas.append(ent)
    
    progs = []      #carregar todos os programas em uma lista
    tabelas = []    #carregar todos os dicionários de símbolos aqui
    
    for i, arq in enumerate(entradas):
        progs.append([])
        tab = carregar_dict(arq[:-3] + "sym")
        tabelas.append(tab) #carrega as respectivas tabelas
        tam = tab["tam"]
        cont = 0
        with open(arq, 'r') as f:
            linha = f.readline()
            while linha and cont != tam:
                lin = linha.strip()
                #print(linha.strip())
                progs[i].append(linha.strip()) #carrega programas
                linha = f.readline()
                cont += 1
    
    main = None
    for i, tab in enumerate(tabelas):#procura a main e coloca ela em primeiro lugar nos vetores com o código
        if tab[0][0] == "main":
            if main is not None:
                raise Exception("ERRO: Múltiplas main.") 
            main = i # indica que a main encontra no programa de indice i          
    if main is None:
        raise Exception('ERRO: ".globalT main" não está presente na entrada.')
    #print(tabelas)
    progs.insert(0, progs.pop(main)) # colocar o programa principal no início do código
    tabelas.insert(0, tabelas.pop(main))  
    #print(progs)
    #exit(0)
    progsCat = [[]]
    tabjumps = {}
    cont = 0
    for p, prog in enumerate(progs):     # itera entre os progs da entrada
        for l,lin in enumerate(prog): #itera entre as linhas de cada prog
            if prog[l][-4:-2] == 'FF' and prog[l+1][-4:-2] == '00':
                #print(tabelas[p][l],cont, lin)
                if tabelas[p][l][0] == 'et':
                    tabjumps[cont] = tabelas[p][l][1]
                elif tabelas[p][l][0] == 'gt':
                    tabjumps[ tabelas[p][l][1] ] = cont
                else:
                    raise Exception("ERRO: Símbolo desconhecido.")
            elif prog[l][-4:-2] == '7F' and prog[l+1][-4:-2] == '00':
                if tabelas[p][l][0] == 'ed':
                    raise NotImplemented('.externD')
                elif tabelas[p][l][0] == 'gd':
                    raise NotImplemented('.globalD')
                else:
                    raise Exception("ERRO: Símbolo desconhecido.")
            progsCat[cont].append(cont)
            progsCat[cont].append(lin[-4:-2])
            progsCat.append([])
            cont += 1
    
    for p in range(len(progsCat[:-1])) :
        if progsCat[p][0] in tabjumps.keys(): #checa se o endereço tem um rótulo
            rotulo = tabjumps[progsCat[p][0]] #obtem o endereço para o qual o rótulo aponta
            if rotulo in tabjumps.keys(): #colocar o jump para o rótulo
                
                dest = tabjumps[rotulo]
                progsCat[p][1] = format(int('01001000', 2), '02X') #colocar o jump (em base16)
                progsCat[p+1][1] = format(int(dest), '02X')    #colocar o rótulo dest
                
                progsCat[dest][1] = format(int('01100000', 2), '02X') #coloca um nop no início do rótulo
                progsCat[dest+1][1] = format( 0 , '02X')        # move A0 A0

                volta = jump_de_volta(progsCat[dest:]) # retorna o endereço do final do módulo para qual o jump aponta
                #print(volta)        
                progsCat[volta][1] =  format(int('01001000', 2), '02X') #colocar o jump (em base16)
                progsCat[volta+1][1] = format(int(p+2), '02X')    #colocar o rótulo dest

            else:
                raise Exception("ERRO: Símbolo não referencia nenhum endereço: \""+str(rotulo)+"\"" )
    
    #procurar o marcador de final do programa e remover os FE FE, coloca a instrução stop
    for i in range(len(progsCat[:-1])):
        if progsCat[i][1] == 'FE' and progsCat[i+1][1] == 'FE':
            progsCat[i][1] = '00'
            progsCat[i+1][1] = '00'
    
    #imprimir(progsCat, arquivo='stdout')   
    imprimir(progsCat, arquivo=saidaFinal)

main()


