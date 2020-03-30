start                   = top_level+
top_level               = _ expr:(function_definition / variable_definition / picture_list_definition / picture_definition) 

function_definition     = identifier parameters "::" _ expression 
parameters              = "(" _ parameter* ")" _ 
parameter               = identifier default_value:("=" _ literal)? _comma

variable_definition     = identifier "=" _ expression 
picture_definition      = identifier parameters:parameters? "<<" _ body:picture_component csg 
csg                     = terms:csg_term* _ 
csg_term                = operator:csg_operator term:csg_factor 
csg_factor              = "(" _ lhs:picture_component term:csg_term ")" _  / picture_component _ 
csg_operator            = (plusplus:"++" / minusminus:"--" / andand:"&&") _ 
picture_component       = basis picture_set_rhs? _
picture_set_rhs         = picture_set transform_set:transform_set*
picture_set             = "[" _ num_pics transformations:transformation* "]" _ 
transform_set           = "[" _ num_pics transformations:transformation* "]" _ 
basis                   = invocation / identifier
num_pics                = "{" value:(literal / identifier) "}" _ 
transformation          = operator arguments 

picture_list_definition = identifier parameters:parameters? "<<<" _ picture_list 
picture_list            = "[" _ (identifier _comma)* "]" _ 

expression              = expression:(infix / invocation / literal / identifier) _semicolon
infix                   = lhs:term op:operator rhs:expression 
term                    = expression:("(" _ expression ")" _) / invocation / literal / identifier
operator                = [\+\*\/\-\@] _ 
invocation              = identifier arguments 
arguments               = "(" _ argument* ")" _ 
argument                = (named_argument / positional_argument) _comma
named_argument          = identifier "=" _ expression 
positional_argument     = expression

literal                 = number _ 
identifier              = symbol _ 
number                  = digits _ 
symbol                  = [^ (),#=\*\+\-\[\]]+
digits                  = "-"? [0-9\.]+
_semicolon               = (";" _)?
_comma                   = ("," _)?

_                       = whitespace? comment* 
whitespace              = [\r\n ]*
comment                 = "#" [^\r\n]* whitespace