start                   = _ top_level*
top_level               = python_code / picture_definition _

python_code             = "***"  code:python_code_line+  "***" _
python_code_line        = !"***" content:[^\r\n]* _newline

picture_definition      = standard_picture / picture_function / picture_selection / picture_combination
standard_picture        = todo
picture_function        = todo
picture_selection       = todo
picture_combination     = todo

literal                 = number _ 
identifier              = symbol _ 
number                  = digits _ 
symbol                  = [^ (),#=\*\+\-\[\]]+
digits                  = "-"? [0-9\.]+
_semicolon               = (";" _)?
_comma                   = ("," _)?

_                       = whitespace? comment*  
_newline                = [\r\n]
whitespace              = [\r\n\t ]*
comment                 = single_line_comment / multi_line_comment
single_line_comment     = "#" [^\r\n]* whitespace
multi_line_comment      = "///" (!"\\\\\\\\\\\\" .)* "\\\\\\\\\\\\" whitespace
todo                    = "##TODO##"