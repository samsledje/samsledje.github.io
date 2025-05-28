.PHONY: help
.DEFAULT_GOAL := help

.PHONY: all
all: clean cv latexclean build ## Clean, generate the CV, clean the latex build files, build the site

.PHONY: clean 
clean: latexclean ## Clean the site
	rm -rf _site

.PHONY: cv
cv: ## Generate the CV in PDF format
	python scripts/build_latex_source.py
	xelatex -output-directory=latex latex/main.tex -
	xelatex -output-directory=latex latex/main.tex -
	cp latex/main.pdf assets/files/Sledzieski_Samuel_CV.pdf

.PHONY: latexclean
latexclean: ## Clean the latex build files
	rm -rf latex/*.aux latex/*.log latex/*.out

.PHONY: build
build: ## Build the site
	bundle exec jekyll build

.PHONY: serve
serve: ## Serve the site locally
	bundle exec jekyll serve -l -H localhost

.PHONY: help
help: ## Show this help message
	@echo 'Usage:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
