.PHONY: venv test package clean

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt
	touch .venv/touchfile

test:
	. .venv/bin/activate; coverage3 run --omit='test/*' -m pytest --junitxml=junitreport.xml test/test_integration.py
	coverage3 report -m

package:
	pyinstaller pmtAV.spec

clean:
	find . -iname "*.pyc" -delete
	rm -rf output
	rm -f spam.log
	rm -rf dist
	rm -rf build
	rm -f *.spec
