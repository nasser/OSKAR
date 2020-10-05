start                   = top_level*
top_level               = python_code / picture_definition
python_code             = _python_code_delimeter  code:python_code_line+  _python_code_delimeter 
_python_code_delimeter   = "***" _newline?
python_code_line        = !_python_code_delimeter content:[^\r\n]* _newline
picture_definition      = todo

literal                 = number _ 
identifier              = symbol _ 
number                  = digits _ 
symbol                  = [^ (),#=\*\+\-\[\]]+
digits                  = "-"? [0-9\.]+
_semicolon               = (";" _)?
_comma                   = ("," _)?

_                       = whitespace? comment* 
_newline                 = [\r\n]
whitespace              = [\r\n ]*
comment                 = "#" [^\r\n]* whitespace
todo                    = "##TODO##"