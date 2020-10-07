/// this file was generated by the arz parser generator
/// probably don't edit it by hand
/// take care of each other

module Generated

open System.Text.RegularExpressions

type SourceReader (source:string) =
    member val position = 0 with get, set
    member val source = source

type ArzLiteral = ArzLiteral of string
let peek (sr:SourceReader) =
    if sr.position < sr.source.Length
    then sr.source.[sr.position]
    else (char -1)

let position (sr:SourceReader) =
    sr.position

let reset (sr:SourceReader) position' =
    sr.position <- position'

let advance (sr:SourceReader) =
    reset sr (sr.position+1)

let read sr =
    let c = peek sr
    advance sr
    c

let readString sr length =
    let mutable s = ""
    for _ in 0..length do
        s <- s + (string (read sr))
    s    

let expect sr c =
    let p = position sr
    if read sr = c
    then Some c
    else reset sr p; None

let expectMatch (pattern:Regex) sr =
    let p = position sr
    let c = read sr
    if c <> '\uffff' && pattern.IsMatch (string c)
    then Some c
    else reset sr p; None

let expectMatchString sr (pattern:Regex) minimum =
    let p = position sr
    let rec readString s =
        match expectMatch pattern sr with
        | Some c -> readString (s + (string c))
        | None -> s
    match readString "" with
    | s when s.Length > minimum -> Some s
    | _ -> reset sr p; None

let expectAny sr (s:string) =
    let p = position sr
    let cs = Set.ofArray (s.ToCharArray())
    let c = read sr
    if Set.contains c cs
    then Some (string c)
    else reset sr p; None

let expectString sr (s:string) =
    let p = position sr
    let s' = readString sr (s.Length-1)
    if s' = s
    then Some s'
    else reset sr p; None

let expectLiteral sr (s:string) =
    match expectString sr s with
    | Some s' -> Some (ArzLiteral s')
    | _ -> None

let parseList sr minimum parsef =
    let p = position sr
    let rec readList list =
        match parsef sr with
        | Some x -> readList (List.append list [x])
        | None -> list
    match readList [] with
    | list when List.length list >= minimum -> Some list
    | _ -> reset sr p; None

/// START GENERATED GRAMMAR ///


type Start = Start of StartElement2
and StartElement2 = TopLevel list
and TopLevel = 
| PythonCode of PythonCode
| TopLevelCase2 of TopLevelCase2
and TopLevelCase2 = TopLevelCase2 of PictureDefinition
and PythonCode = PythonCode of code:PythonCodeCode
and PythonCodeCode = PythonCodeLine list
and PythonCodeLine = PythonCodeLine of content:PythonCodeLineContent
and PythonCodeLineContent = string
and PictureDefinition = 
| StandardPicture of StandardPicture
| PictureFunction of PictureFunction
| PictureSelection of PictureSelection
| PictureCombination of PictureCombination
and StandardPicture = StandardPicture of Todo
and PictureFunction = PictureFunction of Todo
and PictureSelection = PictureSelection of Todo
and PictureCombination = PictureCombination of Todo
and Literal = Literal of Number
and Identifier = Identifier of Symbol
and Number = Number of Digits
and Symbol = string
and Digits = Digits of DigitsElement2
and DigitsElement1 = DigitsElement1 of ArzLiteral option
and DigitsElement2 = string
and UnderscoreSemicolon = UnderscoreSemicolon of UnderscoreSemicolonExpression option
and UnderscoreSemicolonExpression = UnderscoreSemicolonExpression
and UnderscoreComma = UnderscoreComma of UnderscoreCommaExpression option
and UnderscoreCommaExpression = UnderscoreCommaExpression
and Underscore = Underscore of UnderscoreElement1 * UnderscoreElement2
and UnderscoreElement1 = UnderscoreElement1 of Whitespace option
and UnderscoreElement2 = Comment list
and UnderscoreNewline = UnderscoreNewline of char
and Whitespace = string
and Comment = 
| SingleLineComment of SingleLineComment
| MultiLineComment of MultiLineComment
and SingleLineComment = SingleLineComment of SingleLineCommentElement2 * Whitespace
and SingleLineCommentElement2 = string
and MultiLineComment = MultiLineComment of MultiLineCommentElement2 * Whitespace
and MultiLineCommentElement2 = MultiLineCommentElement2Expression list
and MultiLineCommentElement2Expression = MultiLineCommentElement2Expression of char
and Todo = ArzLiteral
let rec start (sr:SourceReader) : Start option =
  let p = position sr
  let var0 = underscore sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = start_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Start.Start (Option.get var1))
and start_element2 (sr:SourceReader) : StartElement2 option =
  let p = position sr
  let rec readList list =
    match top_level sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and top_level (sr:SourceReader) : TopLevel option =
  let p = position sr
  match python_code sr with
  | Some x -> Some (TopLevel.PythonCode x)
  | _ ->
  reset sr p
  match top_level_case2 sr with
  | Some x -> Some (TopLevel.TopLevelCase2 x)
  | _ ->
  reset sr p
  None
and top_level_case2 (sr:SourceReader) : TopLevelCase2 option =
  let p = position sr
  let var0 = picture_definition sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (TopLevelCase2.TopLevelCase2 (Option.get var0))
and python_code (sr:SourceReader) : PythonCode option =
  let p = position sr
  let var0 = expectLiteral sr "***"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = python_code_code sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "***"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = underscore sr
  if Option.isNone var3 then
    reset sr p; None
  else
    Some (PythonCode.PythonCode (Option.get var1))
and python_code_code (sr:SourceReader) : PythonCodeCode option =
  let p = position sr
  let rec readList list =
    match python_code_line sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 1 -> Some list
  | _ ->
  reset sr p
  None
and python_code_line (sr:SourceReader) : PythonCodeLine option =
  let p = position sr
  let p0 = position sr
  let var0 = expectLiteral sr "***"
  if Option.isSome var0 then
    reset sr p; None
  else
  reset sr p0
  let var1 = python_code_line_content sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = underscore_newline sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (PythonCodeLine.PythonCodeLine (Option.get var1))
and python_code_line_content (sr:SourceReader) : PythonCodeLineContent option =
  let p = position sr
  let pattern = Regex "[^\n]"
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 0 -> Some s
  | _ ->
  reset sr p
  None
and picture_definition (sr:SourceReader) : PictureDefinition option =
  let p = position sr
  match standard_picture sr with
  | Some x -> Some (PictureDefinition.StandardPicture x)
  | _ ->
  reset sr p
  match picture_function sr with
  | Some x -> Some (PictureDefinition.PictureFunction x)
  | _ ->
  reset sr p
  match picture_selection sr with
  | Some x -> Some (PictureDefinition.PictureSelection x)
  | _ ->
  reset sr p
  match picture_combination sr with
  | Some x -> Some (PictureDefinition.PictureCombination x)
  | _ ->
  reset sr p
  None
and standard_picture (sr:SourceReader) : StandardPicture option =
  let p = position sr
  match todo sr with
  | Some v -> Some (StandardPicture v)
  | None ->
  reset sr p
  None
and picture_function (sr:SourceReader) : PictureFunction option =
  let p = position sr
  match todo sr with
  | Some v -> Some (PictureFunction v)
  | None ->
  reset sr p
  None
and picture_selection (sr:SourceReader) : PictureSelection option =
  let p = position sr
  match todo sr with
  | Some v -> Some (PictureSelection v)
  | None ->
  reset sr p
  None
and picture_combination (sr:SourceReader) : PictureCombination option =
  let p = position sr
  match todo sr with
  | Some v -> Some (PictureCombination v)
  | None ->
  reset sr p
  None
and literal (sr:SourceReader) : Literal option =
  let p = position sr
  let var0 = number sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Literal.Literal (Option.get var0))
and identifier (sr:SourceReader) : Identifier option =
  let p = position sr
  let var0 = symbol sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Identifier.Identifier (Option.get var0))
and number (sr:SourceReader) : Number option =
  let p = position sr
  let var0 = digits sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Number.Number (Option.get var0))
and symbol (sr:SourceReader) : Symbol option =
  let p = position sr
  let pattern = Regex "[^ \(\),#=\*\+\-\[\]]"
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 1 -> Some s
  | _ ->
  reset sr p
  None
and digits (sr:SourceReader) : Digits option =
  let p = position sr
  let var0 = digits_element1 sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = digits_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Digits.Digits (Option.get var1))
and digits_element1 (sr:SourceReader) : DigitsElement1 option =
  let p = position sr
  match expectLiteral sr "-" with
  | Some v -> Some (DigitsElement1 (Some v))
  | None -> Some (DigitsElement1 None)
and digits_element2 (sr:SourceReader) : DigitsElement2 option =
  let p = position sr
  let pattern = Regex "[0-9\.]"
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 1 -> Some s
  | _ ->
  reset sr p
  None
and underscore_semicolon (sr:SourceReader) : UnderscoreSemicolon option =
  let p = position sr
  match underscore_semicolon_expression sr with
  | Some v -> Some (UnderscoreSemicolon (Some v))
  | None -> Some (UnderscoreSemicolon None)
and underscore_semicolon_expression (sr:SourceReader) : UnderscoreSemicolonExpression option =
  let p = position sr
  let var0 = expectLiteral sr ";"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (UnderscoreSemicolonExpression.UnderscoreSemicolonExpression)
and underscore_comma (sr:SourceReader) : UnderscoreComma option =
  let p = position sr
  match underscore_comma_expression sr with
  | Some v -> Some (UnderscoreComma (Some v))
  | None -> Some (UnderscoreComma None)
and underscore_comma_expression (sr:SourceReader) : UnderscoreCommaExpression option =
  let p = position sr
  let var0 = expectLiteral sr ","
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (UnderscoreCommaExpression.UnderscoreCommaExpression)
and underscore (sr:SourceReader) : Underscore option =
  let p = position sr
  let var0 = underscore__element1 sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore__element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Underscore.Underscore (Option.get var0,Option.get var1))
and underscore__element1 (sr:SourceReader) : UnderscoreElement1 option =
  let p = position sr
  match whitespace sr with
  | Some v -> Some (UnderscoreElement1 (Some v))
  | None -> Some (UnderscoreElement1 None)
and underscore__element2 (sr:SourceReader) : UnderscoreElement2 option =
  let p = position sr
  let rec readList list =
    match comment sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and underscore_newline (sr:SourceReader) : UnderscoreNewline option =
  let p = position sr
  match expectMatch (Regex "[\n]") sr with
  | Some s -> Some (UnderscoreNewline s)
  | None ->
  reset sr p
  None
and whitespace (sr:SourceReader) : Whitespace option =
  let p = position sr
  let pattern = Regex "[\n\t ]"
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 0 -> Some s
  | _ ->
  reset sr p
  None
and comment (sr:SourceReader) : Comment option =
  let p = position sr
  match single_line_comment sr with
  | Some x -> Some (Comment.SingleLineComment x)
  | _ ->
  reset sr p
  match multi_line_comment sr with
  | Some x -> Some (Comment.MultiLineComment x)
  | _ ->
  reset sr p
  None
and single_line_comment (sr:SourceReader) : SingleLineComment option =
  let p = position sr
  let var0 = expectLiteral sr "#"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = single_line_comment_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = whitespace sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (SingleLineComment.SingleLineComment (Option.get var1,Option.get var2))
and single_line_comment_element2 (sr:SourceReader) : SingleLineCommentElement2 option =
  let p = position sr
  let pattern = Regex "[^\n]"
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 0 -> Some s
  | _ ->
  reset sr p
  None
and multi_line_comment (sr:SourceReader) : MultiLineComment option =
  let p = position sr
  let var0 = expectLiteral sr "///"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = multi_line_comment_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "\\\\\\"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = whitespace sr
  if Option.isNone var3 then
    reset sr p; None
  else
    Some (MultiLineComment.MultiLineComment (Option.get var1,Option.get var3))
and multi_line_comment_element2 (sr:SourceReader) : MultiLineCommentElement2 option =
  let p = position sr
  let rec readList list =
    match multi_line_comment_element2_expression sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and multi_line_comment_element2_expression (sr:SourceReader) : MultiLineCommentElement2Expression option =
  let p = position sr
  let p0 = position sr
  let var0 = expectLiteral sr "\\\\\\"
  if Option.isSome var0 then
    reset sr p; None
  else
  reset sr p0
  let var1 = expectMatch (Regex ".|\\n") sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (MultiLineCommentElement2Expression.MultiLineCommentElement2Expression (Option.get var1))
and todo (sr:SourceReader) : Todo option =
  let p = position sr
  match expectString sr "##TODO##" with
  | Some v -> Some (ArzLiteral v)
  | None ->
  reset sr p
  None


/// END GENERATED GRAMMAR ///

let parse s =
    let sr = SourceReader s
    start sr

