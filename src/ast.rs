#[derive(Debug)]
pub enum TopLevel {
    Film(Film),
    PythonCodeBlock(PythonCodeBlock),
    Definition(Definition),
    Skip, // for EOL etc
}

#[derive(Debug)]
pub enum Definition {
    Standard(Picture),
    Function,
    Selection
}

#[derive(Debug)]
pub struct Picture {
    pub identifier: String,
    pub parameters: Vec<String>,
    pub basis: Invoke,
    pub operations: Vec<Operation>
}

#[derive(Debug)]
pub enum Operation {
    TransformSets(TransformSet),
    Csg(Csg)
}

#[derive(Debug)]
pub enum Csg {
    Union(Invoke),
    Difference(Invoke),
    Intersection(Invoke)
}

#[derive(Debug)]
pub struct TransformSet {
    pub num_pics: NumPics,
    pub top_level_expression: String,
    pub transforms: Vec<Transform>
}

#[derive(Debug)]
pub struct NumPics {
    pub number: String,
    pub identifier: Option<String>
}

#[derive(Debug)]
pub enum Transform {
    Scale(Option<String>, Option<String>, Option<String>),
    Translate(Option<String>, Option<String>, Option<String>),
    Rotate(Option<String>, Option<String>, Option<String>),
}

#[derive(Debug)]
pub struct Film {
    pub picture: Invoke,
    pub film_parameters : Vec<(String, String)>
}

#[derive(Debug)]
pub struct Invoke {
    pub identifier : String,
    pub parameters : Vec<String>
}

#[derive(Debug)]
pub struct PythonCodeBlock {
    pub lines : String
}
