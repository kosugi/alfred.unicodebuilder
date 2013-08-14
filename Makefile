
.PHONY: all clean test install

all: dist.alfredworkflow

dist.alfredworkflow: icon.png info.plist preprocess.py db
	zip $@ $?

icon.png: icon.svg
	convert -background None $< $@

info.plist: main_build.py info.plist.xml
	python make-info.plist.py

db: make-db.py
	python $<

clean:
	rm -f *.pyc icon.png info.plist dist.alfredworkflow db

test:
	python test_preprocess.py

install:
	open dist.alfredworkflow
