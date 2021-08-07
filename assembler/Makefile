prog: teste

teste:
	python3 main.py < "../tst/Example.a"

testes:
	for i in `seq 1` ; do echo "teste $$i" ; python3 main.py < "../tst/$$i.a" || break ; done

