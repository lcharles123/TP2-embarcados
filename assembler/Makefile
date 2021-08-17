prog: teste

teste:
	python3 main.py "../Example.a" "../ExampleMont.hex"
	#cat ../ExampleMont.hex
	#diff ../ExampleMont.hex ../Example.hex
	#rm ../ExampleMont.hex

testes:
	for i in `seq 3 3` ; do echo "teste $$i" ; python3 main.py "../tst/teste$$i.a" "../tst/teste"$$i"Mont.hex" || break ; done
	for i in `seq 3 3` ; do echo "teste $$i" ; diff "../tst/$$i.hex" "../tst/teste"$$i"Mont.hex"  ; done
