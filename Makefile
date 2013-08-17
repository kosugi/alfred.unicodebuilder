
.PHONY: all clean test install

all: dist.alfredworkflow

dist.alfredworkflow: icon.png info.plist build.py query.py lib.py db
	zip $@ $?

icon.png: icon.svg
	convert -background None $< $@

info.plist: main_build.py main_query.py info.plist.xml
	python make-info.plist.py

db: make-db.py
	python $<

clean:
	rm -f *.pyc icon.png info.plist dist.alfredworkflow db

test:
	python -m unittest test_build test_query test_lib

install: all
	open dist.alfredworkflow
