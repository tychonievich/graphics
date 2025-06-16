SRC := $(shell find md/ -type f -name '*.md')
DST := $(patsubst md/%.md,html/%.html, $(SRC))
SRCDIR := $(shell find md/ -type d)
DSTDIR := $(patsubst md/%,html/%, $(SRCDIR))
TEXT_SRC := $(shell find md/text/ -type f -name '*.md' | grep -v index.md)
COURSE := cs418
TERM := fa2025
REMOTE := 

.PHONY: all clean html post

all: $(DST) html

debug:
	echo $(SRC)
	echo $(DST)
	echo $(SRCDIR)
	echo $(DSTDIR)

clean:
	rm -rf $(DST) node_modules pikchr package-lock.json

node_modules/katex/dist/katex.css:
	npm upgrade
	sed -i -e 's;font: normal [0-9.]*em KaTeX;font: normal 1.0em KaTeX;g' node_modules/katex/dist/katex.css


post: all
	git pull
	git add $(SRC)
	git add support/
	git commit -am 'autocommit' && git pull && git push || true
	find html -name '*-e' | xargs rm -f
	rsync -rltvu --copy-links \
		html/ \
		"$(shell ./connect.sh $(COURSE) $(TERM))"
	rsync -rltvu \
		html/ \
		luthert@cs418.cs.illinois.edu:/var/www/html/website
	git push

html/%.html: md/%.md sskatex.js sidenotes.lua html5.template pikchr breadcrumber.py node_modules/katex/dist/katex.css
	mkdir -p $(@D)
	pandoc $< \
		-t html5 --columns 4095 \
		--html-q-tags \
		--metadata basedir=$(shell dirname $< | sed -e 's;[^/];;g' -e 's;/;../;g') \
		--css $(shell dirname $< | sed -e 's;[^/];;g' -e 's;/;../;g')katex.css \
		--css $(shell dirname $< | sed -e 's;[^/];;g' -e 's;/;../;g')layout.css \
		--css $(shell dirname $< | sed -e 's;[^/];;g' -e 's;/;../;g')sidenotes.css \
		--template=html5.template \
		--syntax-definition=abnf.xml \
		--standalone --section-divs \
		--number-sections \
		--table-of-contents --toc-depth=2 \
		--strip-comments \
		--filter ./sskatex.js \
		--lua-filter=sidenotes.lua \
		--lua-filter=pikchr.lua \
		--lua-filter=licenses.lua \
		$(shell grep -q '^date: ' $< || echo --metadata date="$(shell date -Idate --date="$(shell stat -c'%y' $<)")") \
		--metadata datetime="$(shell date -Iseconds --date="$(shell stat -c'%y' $<)")" \
		$(shell grep -q '^author:' $< || echo "--metadata author='Luther Tychonievich'") \
		-o $@
	python3 breadcrumber.py "$@"
	sed -i -e 's;<table style="[^"]*">;<table>;g' $@

html:
	rsync -avu \
	  node_modules/katex/dist/fonts \
		node_modules/katex/dist/katex.css \
		support/ \
		html/

md/text/index.md: $(TEXT_SRC) text-index.sh
	bash text-index.sh

pikchr: pikchr.c
	clang -Os -DPIKCHR_SHELL -lm pikchr.c -o pikchr

pikchr.c:
	curl 'https://pikchr.org/home/raw?name=pikchr.c&ci=tip' -o pikchr.c
	sed -i -e "s/\" style='font-size:initial;'\"//g" pikchr.c




