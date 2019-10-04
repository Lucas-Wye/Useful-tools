PAPER = papername
TEX = $(wildcard *.tex)
BIB = references.bib
FIGS = $(wildcard fig/*.pdf)
ALGOS = $(wildcard algo/*.tex)
OUT = out
PAPER_PDF = $(OUT)/$(PAPER).pdf
PAPER_XDV = $(OUT)/$(PAPER).xdv
PAPER_AUX = $(OUT)/$(PAPER).aux
PAPER_BCF = $(OUT)/$(PAPER).bcf

# flag
BUILD_FLGAS=-file-line-error -halt-on-error \
	-interaction=nonstopmode \
	--output-directory=$(OUT)
	# -synctex=1

# pdflatex
PDFLATEX_CMD=pdflatex $(BUILD_FLGAS) $(PAPER)

# xelatex
XELATEX_CMD=xelatex -no-pdf $(BUILD_FLGAS) $(PAPER)
XDV_CMD=xdvipdfmx -q -E -o $(PAPER_PDF) $(PAPER_XDV)
XDV_NO_COMPRESS_CMD=xdvipdfmx -z0 -q -E -o $(PAPER_PDF) $(PAPER_XDV)

# bibtex
BIBTEX_CMD=bibtex $(PAPER_AUX)
BIBER_CMD=biber $(PAPER_BCF)

.PHONY: all clean

all: $(PAPER_PDF)

$(PAPER_PDF): $(TEX) $(BIB) $(FIGS) $(ALGOS)
	mkdir -p $(OUT)
	# xelatex
	# $(XELATEX_CMD)
	# $(BIBER_CMD)
	# $(XELATEX_CMD)
	# $(XELATEX_CMD)
	# $(XDV_CMD)
	# pdflatex
	$(PDFLATEX_CMD)
	$(BIBTEX_CMD)
	$(PDFLATEX_CMD)
	$(PDFLATEX_CMD)

view: $(PAPER_PDF)
	zathura $(PAPER_PDF) &

format:
	latexindent -w $(TEX)

clean:
	rm -rf $(OUT) *.bak0 *.log

