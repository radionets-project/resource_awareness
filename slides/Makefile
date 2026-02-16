TeXInputs = TEXINPUTS=$(PWD):$(PWD)/headers/:


all: build/presentation.pdf

build/presentation.pdf: FORCE | build
	$(TeXInputs) latexmk -r headers/latexmkrc presentation.tex

preview: FORCE | build
	$(TeXInputs) latexmk -r headers/latexmkrc -pvc presentation.tex

FORCE:

build:
	mkdir -p build

clean:
	rm -r build
