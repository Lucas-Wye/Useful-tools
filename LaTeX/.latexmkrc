$out_dir="texout";

$preview_mode=1;
$pdf_previewer="$HOME\\AppData\\Local\\SumatraPDF\\SumatraPDF.exe";
$bibtex_use=1.5;# 自动检测根据条件清理 bbl 文件
$clean_ext='thm bbl hd loe synctex.gz xdv run.xml';
$makeindex='makeindex -s gind.ist %O -o %D %S';

# -------------------------------------------------- pdflatex
$pdf_mode=1;
$pdflatex="pdflatex -file-line-error -halt-on-error -interaction=nonstopmode -synctex=1 %O %S";
# -file-line-error 报错输出文件和行号
# -halt-on-error -interaction=nonstopmode 编译遇到错误时立即停止
# -synctex=1 开启 synctex

# -------------------------------------------------- xelatex
# $pdf_mode=5;
# $xelatex="xelatex -file-line-error -halt-on-error -interaction=nonstopmode -no-pdf -synctex=1 %O %S";
# $xdvipdfmx="xdvipdfmx -q -E -o %D %O %S";
# $xdvipdfmx="xdvipdfmx -q -z0 -E -o %D %O %S";

# -------------------------------------------------- lualatex
# lualatex
# $pdf_mode=4;
# $lualatex="lualatex";
