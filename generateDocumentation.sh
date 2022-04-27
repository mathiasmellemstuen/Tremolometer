#Script for generating documentation PDF
doxygen -u TremoloConf
doxygen Tremoloconf
cd doc/latex
pdflatex refman.tex
open refman.pdf
cd ../../
