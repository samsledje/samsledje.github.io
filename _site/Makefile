.PHONY: all
all: clean pdf latexclean build

.PHONY: clean
clean: latexclean
	rm -rf _site

.PHONY: pdf
pdf:
	xelatex -output-directory=latex latex/main.tex -
	xelatex -output-directory=latex latex/main.tex -
	cp latex/main.pdf assets/files/latex_autoCV.pdf

.PHONY: latexclean
latexclean:
	rm -rf latex/*.aux latex/*.log latex/*.out

.PHONY: build
build:
	bundle exec jekyll build

.PHONY: serve
serve:
	bundle exec jekyll serve -l -H localhost
