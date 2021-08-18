prog: testes

teste:
	python3 main.py "../Example.a" "../ExampleMont.hex"
	#cat ../ExampleMont.hex
	#diff ../ExampleMont.hex ../Example.hex
	#rm ../ExampleMont.hex

testes:
	@echo "============================================"
	@echo "Executando todos os testes da pasta tst/ ..."
	@echo "============================================"
	for i in `seq 1 4` ; do echo "teste $$i" ; python3 main.py "../tst/teste"$$i".a" "../tst/teste"$$i"Mont.hex" || break ; done
	@echo "================================================================="
	@echo "Comparando os arquivos do montador implementado com do CPUsim ..."
	@echo "================================================================="
	for i in `seq 1 4` ; do echo "teste $$i" ; diff "../tst/teste"$$i".hex" "../tst/teste"$$i"Mont.hex"  ; done
