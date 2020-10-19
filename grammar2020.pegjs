start                   = _ top_level*
top_level               = python_code / picture_definition

python_code             = "***"  code:python_code_line+  "***" _
python_code_line        = !"***" content:[^\r\n]* _newline

picture_definition      = standard_picture / picture_function / picture_selection / picture_combination
standard_picture        = identifier _empty_arguments "<<" _ basis_picture transform_set*
basis_picture           = identifier _empty_arguments
transform_set           = "[" _ num_pics transform* "]" _
num_pics                = "{" _ (literal / identifier)  "}" _
transform               = scale_transform / translate_transform / rotate_transform
scale_transform         = "*" _ transform_arguments
translate_transform     = "+" _ transform_arguments
rotate_transform        = "@" _ transform_arguments

transform_arguments     = "(" _ x:expression? "," _ y:expression? "," _ z:expression? ")" _
_empty_arguments        = "(" _  ")" _

expression              = (simple:[^,()]+ / parenthetical:("(" _ expression ")"))+

picture_function        = todo
picture_selection       = todo
picture_combination     = todo

literal                 = number _ 
identifier              = symbol _ 
number                  = digits _ 
symbol                  = [^ (),#=\*\+\-\[\]{}]+
digits                  = "-"? [0-9\.]+
_semicolon               = (";" _)?
_comma                   = ("," _)?

_                       = whitespace comment*  
_newline                = [\r\n]
whitespace              = [\r\n\t ]*
comment                 = single_line_comment / multi_line_comment
single_line_comment     = "#" [^\r\n]* whitespace
multi_line_comment      = "///" (!"\\\\\\\\\\\\" .)* "\\\\\\\\\\\\" whitespace
todo                    = "TODO"