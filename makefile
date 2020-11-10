.PHONY: clean build

SCRIPT = pubparse.py
RUN = python3 $(SCRIPT)

default: build

build: update publications-combinat.html publications-general.html publications-mupad.html publications-mathscinet.html

update:
	git fetch origin
	git pull origin master

publications-general.html: bibliography-sage.bib $(SCRIPT)
	$(RUN) sage

publications-combinat.html: Sage-Combinat.bib $(SCRIPT)
	$(RUN) combinat

publications-mupad.html: MuPAD-Combinat.bib $(SCRIPT)
	$(RUN) mupad

publications-mathscinet.html: mathscinet.bib $(SCRIPT)
	$(RUN) mathscinet

clean:
	- rm -f *.html
