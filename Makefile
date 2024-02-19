venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate;pip install --upgrade pip;pip install -Ur requirements.txt
	touch .venv/touchfile

test:
	coverage3 run pmtAV_test.py && coverage3 run -a fsv_test.py && coverage3 run -a encryption_test.py && coverage3 report -m

package:
	pyinstaller pmtAV.spec

clean:
	find -iname "*.pyc" -delete
	rm -rf output
	rm -f spam.log
	rm -rf dist
	rm -rf build
	rm -f *.spec