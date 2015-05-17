
.PHONY: all clean test install

OBJDIR=./build

all: $(OBJDIR)/dist.alfredworkflow

$(OBJDIR)/dist.alfredworkflow: $(OBJDIR)/icon.png $(OBJDIR)/info.plist build.py query.py lib.py $(OBJDIR)/db
	zip -j -D $@ $?

$(OBJDIR)/icon.png: icon.svg
	@[ -d $(OBJDIR) ] || mkdir -p $(OBJDIR)
	convert -background None icon.svg $@

$(OBJDIR)/info.plist: main_build.py main_query.py info.plist.xml make-info.plist.py
	@[ -d $(OBJDIR) ] || mkdir -p $(OBJDIR)
	python make-info.plist.py

$(OBJDIR)/NamesList.txt:
	wget -O $(OBJDIR)/$(@F) http://unicode.org/Public/UNIDATA/NamesList.txt

$(OBJDIR)/db: $(OBJDIR)/NamesList.txt make-db.py
	python make-db.py

clean:
	rm -f *.pyc $(OBJDIR)/*

test:
	python -m unittest test_build test_query test_lib

install: all
	open $(OBJDIR)/dist.alfredworkflow
