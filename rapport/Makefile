# Indicate what compiler we use
PDFLATEX	?= pdflatex
PDFTK		?= pdftk

TEXFILE 	= rapport_iutbm.tex

# Compilation and linking
pdf:
	$(PDFLATEX) $(TEXFILE)
	$(PDFLATEX) $(TEXFILE)
clean:
	rm -f *.aux *.lof *.log *.lot *.out *.toc
clean-all:
	rm -f *.aux *.lof *.log *.lot *.out *.toc *.pdf
