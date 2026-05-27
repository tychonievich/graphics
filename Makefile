SRC := $(shell find md/ -type f -name '*.md')
DST := $(patsubst md/%.md,html/%.html, $(SRC))
SRCDIR := $(shell find md/ -type d)
DSTDIR := $(patsubst md/%,html/%, $(SRCDIR))
TEXT_SRC := $(shell find md/text/ -type f -name '*.md' | grep -v index.md)
COURSE := cs418
TERM := fa2026
REMOTE := 

.PHONY: all clean html post

all: $(DST) html

debug:
	echo $(SRC)
	echo $(DST)
	echo $(SRCDIR)
	echo $(DSTDIR)

clean:
	rm -f $(DST) node_modules package-lock.json

node_modules/temml/dist/Temml.woff2:
	npm upgrade

post: all
	git switch fa2026
	git pull
	git add $(SRC)
	git add support/
	git commit -am 'autocommit' && git pull && git push || true
	find html -name '*-e' | xargs rm -f
#	rsync -rltvu --copy-links \
#		html/ \
#		"$(shell ./connect.sh $(COURSE) $(TERM))"
	rsync -rltvu \
		html/ \
		luthert@cs418.cs.illinois.edu:/var/www/html/redo
#	scp tasks.json luthert@cs418.cs.illinois.edu:/var/www/html/submit/course/tasks.json
#	scp tasks.json luthert@cs418-adm.cs.illinois.edu:tasks.json
	git push

html/%.html: md/%.md sstemml.js sidenotes.lua html5.template pikchr breadcrumber.py temml.cjs
	mkdir -p $(@D)
	pandoc $< \
		-t html5 --columns 4095 \
		--html-q-tags \
		--metadata basedir=$(shell dirname $< | sed -e 's;[^/];;g' -e 's;/;../;g') \
		--css $(shell dirname $< | sed -e 's;//;/;g' -e 's;[^/];;g' -e 's;/;../;g')Temml-Latin-Modern.css \
		--css $(shell dirname $< | sed -e 's;//;/;g' -e 's;[^/];;g' -e 's;/;../;g')layout.css \
		--css $(shell dirname $< | sed -e 's;//;/;g' -e 's;[^/];;g' -e 's;/;../;g')sidenotes.css \
		--template=html5.template \
		--standalone --section-divs \
		--number-sections \
		--table-of-contents --toc-depth=2 \
		--strip-comments \
		--filter ./sstemml.js \
		--lua-filter=sidenotes.lua \
		--lua-filter=pikchr.lua \
		--lua-filter=licenses.lua \
		--lua-filter=nocolgroup.lua \
		$(shell grep -q '^date: ' $< || echo --metadata date="$(shell date -Idate --date="$(shell stat -c'%y' $<)")") \
		--metadata datetime="$(shell date -Iseconds --date="$(shell stat -c'%y' $<)")" \
		$(shell grep -q '^author:' $< || echo "--metadata author='Luther Tychonievich'") \
		-o $@
	python3 breadcrumber.py "$@"
	sed -i -e 's;<table style="[^"]*">;<table>;g' $@

temml.cjs: node_modules/temml/dist/Temml.woff2
	cp node_modules/temml/dist/temml.cjs ./

html:
	rsync -avu \
	  node_modules/temml/dist/Temml-Latin-Modern.css \
	  node_modules/temml/dist/Temml.woff2 \
		support/ \
		html/

md/text/index.md: $(TEXT_SRC) text-index.sh
	bash text-index.sh

pikchr: pikchr.c
	clang -Os -DPIKCHR_SHELL -lm pikchr.c -o pikchr






