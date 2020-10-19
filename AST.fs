module AST

type Identifier = string

type OpaqueExpression = string

type NumPics = 
    | Value of int
    | Identifier of Identifier

type TransformOperation =
    | Scale
    | Translate
    | Rotate

type Transform = 
    { Operation : TransformOperation
      X: OpaqueExpression
      Y: OpaqueExpression
      Z: OpaqueExpression }

type TransformSet = 
    { NumPics : NumPics
      Transforms : Transform list }

type StandardPicture =
    { Name : Identifier
      Basis : Identifier
      TransformSets : TransformSet list }

type AST =
    | PythonBlock of string
    | StandardPicture of StandardPicture