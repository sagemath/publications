.PHONY: clean build

SCRIPT = pubparse.py
RUN = python $(SCRIPT)

default: build

build: update publications-combinat.html publications-general.html publications-mupad.html

update:
	git fetch origin
	git reset --hard origin/master

publications-general.html: bibliography-sage.bib $(SCRIPT)
	$(RUN) sage

publications-combinat.html: Sage-Combinat.bib $(SCRIPT)
	$(RUN) combinat

publications-mupad.html: MuPAD-Combinat.bib $(SCRIPT)
	$(RUN) mupad

clean:
	- rm -f *.html
