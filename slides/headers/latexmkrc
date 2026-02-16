$out_dir = "build";
$lualatex = "lualatex --shell-escape -interaction=\${INTERACTION:-nonstopmode} -halt-on-error %O %S";

# ignore lualatex font cache, which leads to latexmk thinking it needs
# to rerun document indefinitely
$hash_calc_ignore_pattern{'luc'}='^';

# use lualatex
$pdf_mode = 4;

