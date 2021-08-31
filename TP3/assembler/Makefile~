

prog: t1 t2


mod1:
	python3 main.py "../Example.a" "../Example.hex"
	#cat ../Example.hex
	#rm ../Example.hex

mod2:
	python3 main.py "../Procedimento.a" "../Procedimento.hex"
	cat ../Procedimento.hex

ligar: 
	python3 ligador.py "../Example.hex" "../Procedimento.hex" "../ProgramaFinal.hex"
	#cat ../ProgramaFinal.hex
	#rm ../ProgramaFinal.hex

t1:	
	@echo "==================================================="
	@echo "teste1: main -> teste1.a , módulo externo -> proc.a"
	@echo "==================================================="
	python3 main.py "../tst/teste1.a" "../tst/teste1.hex"
	python3 main.py "../tst/proc.a" "../tst/proc.hex"
	python3 ligador.py "../tst/teste1.hex" "../tst/proc.hex" "../tst/prog1Final.hex"
	@echo ""

t2:
	@echo "================================================================="
	@echo "teste2: main -> teste2.a , módulo externo -> proc.a pré compilado"
	@echo "================================================================="
	python3 main.py "../tst/teste2.a" "../tst/teste2.hex"
	python3 ligador.py "../tst/teste2.hex" "../tst/proc.hex" "../tst/prog2Final.hex"




clean:
	rm -rf ../tst/*.hex ../tst/*.sym    # removeu todos os arquivos .hex e .sym

help:
	@echo "================================================================"
	@echo "Bem vindo ao TP3 de Embarcados"
	@echo "Este makefile contem os seguintes targets:"
	@echo "\t\"\": monta e liga todos os programas"
	@echo "\tclean: limpa os arquivos gerados por este makefile"
	@echo "================================================================"


