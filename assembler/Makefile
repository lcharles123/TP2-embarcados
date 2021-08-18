prog: testes

teste:
	python3 main.py "../Example.a" "../ExampleMont.hex"
	#cat ../ExampleMont.hex

testes:
	@echo "============================================"
	@echo "Executando todos os testes da pasta tst/ ..."
	@echo "============================================"
	for i in `seq 1 4` ; do echo "teste $$i" ; python3 main.py "../tst/teste"$$i".a" "../tst/teste"$$i"Mont.hex" || break ; done
	@echo "================================================================="
	@echo "Comparando os arquivos do montador implementado com do CPUsim ..."
	@echo "================================================================="
	for i in `seq 1 4` ; do echo "teste $$i" ; diff "../tst/teste"$$i".hex" "../tst/teste"$$i"Mont.hex"  ; done


clean:
	rm -rf ../tst/*Mont.hex # removeu apenas os arquivos do montador implementado

help:
	@echo "================================================================"
	@echo "Bem vindo ao TP2 de Embarcados"
	@echo "Este makefile contem os seguintes targets:"
	@echo "\tteste: monta 1 programa"
	@echo "\ttestes: monta 4 programas"
	@echo "\tlimpar: limpa os arquivos gerados com o montador implementado"
	@echo "================================================================"

	
