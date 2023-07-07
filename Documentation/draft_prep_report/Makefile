PAPERNAME=report
BIBNAME=literature

all: $(PAPERNAME).pdf

$(PAPERNAME).pdf: $(wildcard *.tex) $(PAPERNAME).bbl
	pdflatex -halt-on-error $(PAPERNAME).tex </dev/null
	bibtex $(PAPERNAME)
	pdflatex -halt-on-error $(PAPERNAME).tex </dev/null
	pdflatex -halt-on-error $(PAPERNAME).tex </dev/null

$(PAPERNAME).bbl: $(PAPERNAME).tex $(BIBNAME).bib $(PAPERNAME).aux

$(PAPERNAME).aux: $(PAPERNAME).tex
	pdflatex $(PAPERNAME).tex </dev/null

clean:
	rm *.log *.aux *.bbl *.blg
