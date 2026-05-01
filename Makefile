TEX      = pdflatex -interaction=nonstopmode
OUTDIR   = build
MAIN     = main.tex
PDF      = $(OUTDIR)/main.pdf

TEX_FILES = $(shell find . -name "*.tex" -not -path "./$(OUTDIR)/*")

.PHONY: all clean

all: $(PDF)

$(OUTDIR):
	@mkdir -p $(OUTDIR)

$(PDF): $(TEX_FILES) | $(OUTDIR)
	$(TEX) -output-directory=$(OUTDIR) $(MAIN)
	$(TEX) -output-directory=$(OUTDIR) $(MAIN)
	cp $(OUTDIR)/main.pdf ./main.pdf

clean:
	rm -rf $(OUTDIR)