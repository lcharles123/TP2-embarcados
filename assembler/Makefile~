prog: teste

teste:
	python3 main.py "../tst/Example.a" 

testes:
	for i in `seq 1 4` ; do echo "teste $$i" ; python3 main.py "../tst/teste$$i.a" || break ; done

