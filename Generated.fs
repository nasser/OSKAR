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


type Start = TopLevel list
and TopLevel = TopLevel of expr:TopLevelExpr
and TopLevelExpr = 
| FunctionDefinition of FunctionDefinition
| VariableDefinition of VariableDefinition
| PictureListDefinition of PictureListDefinition
| PictureDefinition of PictureDefinition
and FunctionDefinition = FunctionDefinition of Identifier * Parameters * Expression
and Parameters = Parameters of ParametersElement3
and ParametersElement3 = Parameter list
and Parameter = Parameter of Identifier * default_value:ParameterDefaultValue
and ParameterDefaultValue = ParameterDefaultValue of ParameterDefaultValueExpression option
and ParameterDefaultValueExpression = ParameterDefaultValueExpression of Literal
and VariableDefinition = VariableDefinition of Identifier * Expression
and PictureDefinition = PictureDefinition of Identifier * parameters:PictureDefinitionParameters * body:PictureComponent * Csg
and PictureDefinitionParameters = PictureDefinitionParameters of Parameters option
and Csg = Csg of terms:CsgTerms
and CsgTerms = CsgTerm list
and CsgTerm = CsgTerm of operator:CsgOperator * term:CsgFactor
and CsgFactor = 
| CsgFactorCase1 of CsgFactorCase1
| CsgFactorCase7 of CsgFactorCase7
and CsgFactorCase1 = CsgFactorCase1 of lhs:PictureComponent * term:CsgTerm
and CsgFactorCase7 = CsgFactorCase7 of PictureComponent
and CsgOperator = CsgOperator of CsgOperatorElement1
and CsgOperatorElement1 = 
| Plusplus of ArzLiteral
| Minusminus of ArzLiteral
| Andand of ArzLiteral
and PictureComponent = PictureComponent of Basis * PictureComponentElement2
and PictureComponentElement2 = PictureComponentElement2 of PictureSetRhs option
and PictureSetRhs = PictureSetRhs of PictureSet * transform_set:PictureSetRhsTransformSet
and PictureSetRhsTransformSet = TransformSet list
and PictureSet = PictureSet of NumPics * transformations:PictureSetTransformations
and PictureSetTransformations = Transformation list
and TransformSet = TransformSet of NumPics * transformations:TransformSetTransformations
and TransformSetTransformations = Transformation list
and Basis = 
| Invocation of Invocation
| Identifier of Identifier
and NumPics = NumPics of value:NumPicsValue
and NumPicsValue = 
| Literal of Literal
| Identifier of Identifier
and Transformation = Transformation of Operator * Arguments
and PictureListDefinition = PictureListDefinition of Identifier * parameters:PictureListDefinitionParameters * PictureList
and PictureListDefinitionParameters = PictureListDefinitionParameters of Parameters option
and PictureList = PictureList of PictureListElement3
and PictureListElement3 = PictureListElement3Expression list
and PictureListElement3Expression = PictureListElement3Expression of Identifier
and Expression = Expression of expression:ExpressionExpression
and ExpressionExpression = 
| Infix of Infix
| Invocation of Invocation
| Literal of Literal
| Identifier of Identifier
and Infix = Infix of lhs:Term * op:Operator * rhs:Expression
and Term = 
| Expression of TermExpression
| Invocation of Invocation
| Literal of Literal
| Identifier of Identifier
and TermExpression = TermExpression of Expression
and Operator = Operator of char
and Invocation = Invocation of Identifier * Arguments
and Arguments = Arguments of ArgumentsElement3
and ArgumentsElement3 = Argument list
and Argument = Argument of ArgumentElement1
and ArgumentElement1 = 
| NamedArgument of NamedArgument
| PositionalArgument of PositionalArgument
and NamedArgument = NamedArgument of Identifier * Expression
and PositionalArgument = PositionalArgument of Expression
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
and Whitespace = string
and Comment = Comment of CommentElement2 * Whitespace
and CommentElement2 = string
let rec start (sr:SourceReader) : Start option =
  let p = position sr
  let rec readList list =
    match top_level sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 1 -> Some list
  | _ ->
  reset sr p
  None
and top_level (sr:SourceReader) : TopLevel option =
  let p = position sr
  let var0 = underscore sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = top_level_expr sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (TopLevel.TopLevel (Option.get var1))
and top_level_expr (sr:SourceReader) : TopLevelExpr option =
  let p = position sr
  match function_definition sr with
  | Some x -> Some (TopLevelExpr.FunctionDefinition x)
  | _ ->
  reset sr p
  match variable_definition sr with
  | Some x -> Some (TopLevelExpr.VariableDefinition x)
  | _ ->
  reset sr p
  match picture_list_definition sr with
  | Some x -> Some (TopLevelExpr.PictureListDefinition x)
  | _ ->
  reset sr p
  match picture_definition sr with
  | Some x -> Some (TopLevelExpr.PictureDefinition x)
  | _ ->
  reset sr p
  None
and function_definition (sr:SourceReader) : FunctionDefinition option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = parameters sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "::"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = underscore sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = expression sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (FunctionDefinition.FunctionDefinition (Option.get var0,Option.get var1,Option.get var4))
and parameters (sr:SourceReader) : Parameters option =
  let p = position sr
  let var0 = expectLiteral sr "("
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = parameters_element3 sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expectLiteral sr ")"
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = underscore sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (Parameters.Parameters (Option.get var2))
and parameters_element3 (sr:SourceReader) : ParametersElement3 option =
  let p = position sr
  let rec readList list =
    match parameter sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and parameter (sr:SourceReader) : Parameter option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = parameter_default_value sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = underscore_comma sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (Parameter.Parameter (Option.get var0,Option.get var1))
and parameter_default_value (sr:SourceReader) : ParameterDefaultValue option =
  let p = position sr
  match parameter_default_value_expression sr with
  | Some v -> Some (ParameterDefaultValue (Some v))
  | None -> Some (ParameterDefaultValue None)
and parameter_default_value_expression (sr:SourceReader) : ParameterDefaultValueExpression option =
  let p = position sr
  let var0 = expectLiteral sr "="
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = literal sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (ParameterDefaultValueExpression.ParameterDefaultValueExpression (Option.get var2))
and variable_definition (sr:SourceReader) : VariableDefinition option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = expectLiteral sr "="
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = underscore sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expression sr
  if Option.isNone var3 then
    reset sr p; None
  else
    Some (VariableDefinition.VariableDefinition (Option.get var0,Option.get var3))
and picture_definition (sr:SourceReader) : PictureDefinition option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = picture_definition_parameters sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "<<"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = underscore sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = picture_component sr
  if Option.isNone var4 then
    reset sr p; None
  else
  let var5 = csg sr
  if Option.isNone var5 then
    reset sr p; None
  else
    Some (PictureDefinition.PictureDefinition (Option.get var0,Option.get var1,Option.get var4,Option.get var5))
and picture_definition_parameters (sr:SourceReader) : PictureDefinitionParameters option =
  let p = position sr
  match parameters sr with
  | Some v -> Some (PictureDefinitionParameters (Some v))
  | None -> Some (PictureDefinitionParameters None)
and csg (sr:SourceReader) : Csg option =
  let p = position sr
  let var0 = csg_terms sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Csg.Csg (Option.get var0))
and csg_terms (sr:SourceReader) : CsgTerms option =
  let p = position sr
  let rec readList list =
    match csg_term sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and csg_term (sr:SourceReader) : CsgTerm option =
  let p = position sr
  let var0 = csg_operator sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = csg_factor sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (CsgTerm.CsgTerm (Option.get var0,Option.get var1))
and csg_factor (sr:SourceReader) : CsgFactor option =
  let p = position sr
  match csg_factor_case1 sr with
  | Some x -> Some (CsgFactor.CsgFactorCase1 x)
  | _ ->
  reset sr p
  match csg_factor_case7 sr with
  | Some x -> Some (CsgFactor.CsgFactorCase7 x)
  | _ ->
  reset sr p
  None
and csg_factor_case1 (sr:SourceReader) : CsgFactorCase1 option =
  let p = position sr
  let var0 = expectLiteral sr "("
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = picture_component sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = csg_term sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = expectLiteral sr ")"
  if Option.isNone var4 then
    reset sr p; None
  else
  let var5 = underscore sr
  if Option.isNone var5 then
    reset sr p; None
  else
    Some (CsgFactorCase1.CsgFactorCase1 (Option.get var2,Option.get var3))
and csg_factor_case7 (sr:SourceReader) : CsgFactorCase7 option =
  let p = position sr
  let var0 = picture_component sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (CsgFactorCase7.CsgFactorCase7 (Option.get var0))
and csg_operator (sr:SourceReader) : CsgOperator option =
  let p = position sr
  let var0 = csg_operator_element1 sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (CsgOperator.CsgOperator (Option.get var0))
and csg_operator_element1 (sr:SourceReader) : CsgOperatorElement1 option =
  let p = position sr
  match expectLiteral sr "++" with
  | Some x -> Some (CsgOperatorElement1.Plusplus x)
  | _ ->
  reset sr p
  match expectLiteral sr "--" with
  | Some x -> Some (CsgOperatorElement1.Minusminus x)
  | _ ->
  reset sr p
  match expectLiteral sr "&&" with
  | Some x -> Some (CsgOperatorElement1.Andand x)
  | _ ->
  reset sr p
  None
and picture_component (sr:SourceReader) : PictureComponent option =
  let p = position sr
  let var0 = basis sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = picture_component_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = underscore sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (PictureComponent.PictureComponent (Option.get var0,Option.get var1))
and picture_component_element2 (sr:SourceReader) : PictureComponentElement2 option =
  let p = position sr
  match picture_set_rhs sr with
  | Some v -> Some (PictureComponentElement2 (Some v))
  | None -> Some (PictureComponentElement2 None)
and picture_set_rhs (sr:SourceReader) : PictureSetRhs option =
  let p = position sr
  let var0 = picture_set sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = picture_set_rhs_transform_set sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (PictureSetRhs.PictureSetRhs (Option.get var0,Option.get var1))
and picture_set_rhs_transform_set (sr:SourceReader) : PictureSetRhsTransformSet option =
  let p = position sr
  let rec readList list =
    match transform_set sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and picture_set (sr:SourceReader) : PictureSet option =
  let p = position sr
  let var0 = expectLiteral sr "["
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = num_pics sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = picture_set_transformations sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = expectLiteral sr "]"
  if Option.isNone var4 then
    reset sr p; None
  else
  let var5 = underscore sr
  if Option.isNone var5 then
    reset sr p; None
  else
    Some (PictureSet.PictureSet (Option.get var2,Option.get var3))
and picture_set_transformations (sr:SourceReader) : PictureSetTransformations option =
  let p = position sr
  let rec readList list =
    match transformation sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and transform_set (sr:SourceReader) : TransformSet option =
  let p = position sr
  let var0 = expectLiteral sr "["
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = num_pics sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = transform_set_transformations sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = expectLiteral sr "]"
  if Option.isNone var4 then
    reset sr p; None
  else
  let var5 = underscore sr
  if Option.isNone var5 then
    reset sr p; None
  else
    Some (TransformSet.TransformSet (Option.get var2,Option.get var3))
and transform_set_transformations (sr:SourceReader) : TransformSetTransformations option =
  let p = position sr
  let rec readList list =
    match transformation sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and basis (sr:SourceReader) : Basis option =
  let p = position sr
  match invocation sr with
  | Some x -> Some (Basis.Invocation x)
  | _ ->
  reset sr p
  match identifier sr with
  | Some x -> Some (Basis.Identifier x)
  | _ ->
  reset sr p
  None
and num_pics (sr:SourceReader) : NumPics option =
  let p = position sr
  let var0 = expectLiteral sr "{"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = num_pics_value sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "}"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = underscore sr
  if Option.isNone var3 then
    reset sr p; None
  else
    Some (NumPics.NumPics (Option.get var1))
and num_pics_value (sr:SourceReader) : NumPicsValue option =
  let p = position sr
  match literal sr with
  | Some x -> Some (NumPicsValue.Literal x)
  | _ ->
  reset sr p
  match identifier sr with
  | Some x -> Some (NumPicsValue.Identifier x)
  | _ ->
  reset sr p
  None
and transformation (sr:SourceReader) : Transformation option =
  let p = position sr
  let var0 = operator sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = arguments sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Transformation.Transformation (Option.get var0,Option.get var1))
and picture_list_definition (sr:SourceReader) : PictureListDefinition option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = picture_list_definition_parameters sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expectLiteral sr "<<<"
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = underscore sr
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = picture_list sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (PictureListDefinition.PictureListDefinition (Option.get var0,Option.get var1,Option.get var4))
and picture_list_definition_parameters (sr:SourceReader) : PictureListDefinitionParameters option =
  let p = position sr
  match parameters sr with
  | Some v -> Some (PictureListDefinitionParameters (Some v))
  | None -> Some (PictureListDefinitionParameters None)
and picture_list (sr:SourceReader) : PictureList option =
  let p = position sr
  let var0 = expectLiteral sr "["
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = picture_list_element3 sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expectLiteral sr "]"
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = underscore sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (PictureList.PictureList (Option.get var2))
and picture_list_element3 (sr:SourceReader) : PictureListElement3 option =
  let p = position sr
  let rec readList list =
    match picture_list_element3_expression sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and picture_list_element3_expression (sr:SourceReader) : PictureListElement3Expression option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore_comma sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (PictureListElement3Expression.PictureListElement3Expression (Option.get var0))
and expression (sr:SourceReader) : Expression option =
  let p = position sr
  let var0 = expression_expression sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore_semicolon sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Expression.Expression (Option.get var0))
and expression_expression (sr:SourceReader) : ExpressionExpression option =
  let p = position sr
  match infix sr with
  | Some x -> Some (ExpressionExpression.Infix x)
  | _ ->
  reset sr p
  match invocation sr with
  | Some x -> Some (ExpressionExpression.Invocation x)
  | _ ->
  reset sr p
  match literal sr with
  | Some x -> Some (ExpressionExpression.Literal x)
  | _ ->
  reset sr p
  match identifier sr with
  | Some x -> Some (ExpressionExpression.Identifier x)
  | _ ->
  reset sr p
  None
and infix (sr:SourceReader) : Infix option =
  let p = position sr
  let var0 = term sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = operator sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expression sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (Infix.Infix (Option.get var0,Option.get var1,Option.get var2))
and term (sr:SourceReader) : Term option =
  let p = position sr
  match term_expression sr with
  | Some x -> Some (Term.Expression x)
  | _ ->
  reset sr p
  match invocation sr with
  | Some x -> Some (Term.Invocation x)
  | _ ->
  reset sr p
  match literal sr with
  | Some x -> Some (Term.Literal x)
  | _ ->
  reset sr p
  match identifier sr with
  | Some x -> Some (Term.Identifier x)
  | _ ->
  reset sr p
  None
and term_expression (sr:SourceReader) : TermExpression option =
  let p = position sr
  let var0 = expectLiteral sr "("
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = expression sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expectLiteral sr ")"
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = underscore sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (TermExpression.TermExpression (Option.get var2))
and operator (sr:SourceReader) : Operator option =
  let p = position sr
  let var0 = expectMatch (Regex "[\+\*\/\-@]") sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Operator.Operator (Option.get var0))
and invocation (sr:SourceReader) : Invocation option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = arguments sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Invocation.Invocation (Option.get var0,Option.get var1))
and arguments (sr:SourceReader) : Arguments option =
  let p = position sr
  let var0 = expectLiteral sr "("
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = arguments_element3 sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expectLiteral sr ")"
  if Option.isNone var3 then
    reset sr p; None
  else
  let var4 = underscore sr
  if Option.isNone var4 then
    reset sr p; None
  else
    Some (Arguments.Arguments (Option.get var2))
and arguments_element3 (sr:SourceReader) : ArgumentsElement3 option =
  let p = position sr
  let rec readList list =
    match argument sr with
    | Some next -> readList (List.append list [next])
    | None -> list
  match readList [] with
  | list when List.length list >= 0 -> Some list
  | _ ->
  reset sr p
  None
and argument (sr:SourceReader) : Argument option =
  let p = position sr
  let var0 = argument_element1 sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = underscore_comma sr
  if Option.isNone var1 then
    reset sr p; None
  else
    Some (Argument.Argument (Option.get var0))
and argument_element1 (sr:SourceReader) : ArgumentElement1 option =
  let p = position sr
  match named_argument sr with
  | Some x -> Some (ArgumentElement1.NamedArgument x)
  | _ ->
  reset sr p
  match positional_argument sr with
  | Some x -> Some (ArgumentElement1.PositionalArgument x)
  | _ ->
  reset sr p
  None
and named_argument (sr:SourceReader) : NamedArgument option =
  let p = position sr
  let var0 = identifier sr
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = expectLiteral sr "="
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = underscore sr
  if Option.isNone var2 then
    reset sr p; None
  else
  let var3 = expression sr
  if Option.isNone var3 then
    reset sr p; None
  else
    Some (NamedArgument.NamedArgument (Option.get var0,Option.get var3))
and positional_argument (sr:SourceReader) : PositionalArgument option =
  let p = position sr
  match expression sr with
  | Some v -> Some (PositionalArgument v)
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
and whitespace (sr:SourceReader) : Whitespace option =
  let p = position sr
  let pattern = Regex "[
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
  let var0 = expectLiteral sr "#"
  if Option.isNone var0 then
    reset sr p; None
  else
  let var1 = comment_element2 sr
  if Option.isNone var1 then
    reset sr p; None
  else
  let var2 = whitespace sr
  if Option.isNone var2 then
    reset sr p; None
  else
    Some (Comment.Comment (Option.get var1,Option.get var2))
and comment_element2 (sr:SourceReader) : CommentElement2 option =
  let p = position sr
  let pattern = Regex "[^
  let rec readString s =
    match expectMatch pattern sr with
    | Some c -> readString (s + (string c))
    | None -> s
  match readString "" with
  | s when s.Length >= 0 -> Some s
  | _ ->
  reset sr p
  None


/// END GENERATED GRAMMAR ///

let parse s =
    let sr = SourceReader s
    start sr
