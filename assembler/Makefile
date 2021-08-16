prog: teste

teste:
	python3 main.py "../tst/Example.a" "../tst/ExampleMont.hex"
	#cat ../tst/ExampleMont.hex
	#diff ../tst/ExampleMont.hex ../tst/Example.hex
	#rm ../tst/ExampleMont.hex

testes:
	for i in `seq 3 3` ; do echo "teste $$i" ; python3 main.py "../tst/teste$$i.a" "../tst/teste"$$i"Mont.hex" || break ; done
	for i in `seq 3 3` ; do echo "teste $$i" ; diff "../tst/$$i.hex" "../tst/teste"$$i"Mont.hex"  ; done
