.PHONY: clean build

SCRIPT = pubparse.py
RUN = python $(SCRIPT)

default: build

build: publications-combinat.html publications-general.html publications-mupad.html

publications-general.html: bibliography-sage.bib $(SCRIPT)
	$(RUN)

publications-combinat.html: Sage-Combinat.bib $(SCRIPT)
	$(RUN)

publications-mupad.html: MuPAD-Combinat.bib $(SCRIPT)
	$(RUN)

clean:
	- rm -f *.html
