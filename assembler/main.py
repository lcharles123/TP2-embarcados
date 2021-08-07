import sys






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
    
    entrada = sys.argv[1]
    with open(entrada, 'r') as f:
        linha = f.readline()
        while linha:
            
            
            #print(linha.strip()) #aqui temos cada linha sem o newline pode ser processada uma a uma
            
            
            linha = f.readline()
    
    exit(0) 
    
    
    linhas = [10,36,12] #cada entrada representa uma linha no arquivo hex/mif
    linhas += [0] * 127
    imprimir(linhas)
   
   

main()
