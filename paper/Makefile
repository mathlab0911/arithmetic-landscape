# Build the paper.  Requires a TeX distribution (latexmk + pdflatex).
#   make        -> paper.pdf
#   make clean  -> remove build artefacts (keeps paper.pdf)
#   make figs   -> regenerate the figures from the experimental data

paper.pdf: paper.tex fig_flatness.pdf fig_convergence.pdf
	latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex

.PHONY: figs clean distclean
figs:
	cd ../lean/pnp && python figures_r9.py
	cp ../lean/pnp/fig_flatness.pdf ../lean/pnp/fig_convergence.pdf .

clean:
	latexmk -c
	rm -f *.png

distclean: clean
	rm -f paper.pdf
