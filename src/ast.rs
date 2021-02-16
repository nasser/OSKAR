use pest::*;
use pest::iterators::*;

use crate::parser::Rule;

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
    Function(Picture),
    Selection(PictureList)
}

#[derive(Debug)]
pub struct PictureList {
    pub identifier: String,
    pub invokes: Vec<Invoke>
}

#[derive(Debug)]
pub struct Picture {
    pub identifier: String,
    pub parameters: Vec<String>,
    pub basis: Invoke,
    pub operations: Operations
}

#[derive(Debug)]
pub enum Operations {
    TransformSet(Vec<TransformSet>),
    Csg(Vec<Csg>)   
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
    pub top_level_expression: Option<Vec<String>>,
    pub transforms: Vec<Transform>,
    pub iteration: bool
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

fn panic_span(span:Span, message:&str) {
    let (l, c) = span.start_pos().line_col();
    let line = span.start_pos().line_of();
    println!("  | \n{} | {}\n  | {}^---\n  = {} (#file#:{}:{})", l, line, " ".repeat(c-1), message, l, c);
    panic!("analysis error")
}

fn analyze_parameters(pairs:&mut Pairs<Rule>) -> Vec<String> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::parameters 
            => pairs.next().unwrap().into_inner().map(|p| p.as_str().to_string()).collect(),
        _ => vec![]
    }
}

fn analyze_invoke(pairs:&mut Pairs<Rule>) -> Invoke {
    // let mut inner = pairs.next().unwrap().into_inner();
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(pairs);
    Invoke { identifier, parameters }
}

fn analyze_film_parameters(pairs:&mut Pairs<Rule>) -> Vec<(String, String)> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::film_parameters => {
            x.into_inner().map(|p| {
                let mut inner = p.into_inner();
                (inner.next().unwrap().as_str().trim().to_string(),
                 inner.next().unwrap().as_str().trim().to_string())
            }).collect()
        }
        _ => vec![]
    }
}

fn analyze_film(pairs:&mut Pairs<Rule>) -> Film {
    let film_identifier = pairs.next().unwrap();
    if film_identifier.as_str() != "Film" {
        panic_span(film_identifier.as_span(), "Film name must be exactly 'Film'");
    }
    let picture = analyze_invoke(&mut pairs.next().unwrap().into_inner());
    let film_parameters = analyze_film_parameters(pairs);

    Film { picture, film_parameters }
}

fn analyze_python_code(pairs:&mut Pairs<Rule>) -> PythonCodeBlock {
    let mut lines = "".to_owned();
    for pair in pairs {
        lines.push_str(pair.as_str());
    }
    PythonCodeBlock { lines }
}

fn analyze_num_pics(pairs:&mut Pairs<Rule>) -> NumPics {
    let number = pairs.next().unwrap().as_str().to_string();
    let identifier = match pairs.peek() {
        Some(x) => Some(x.as_str().to_string()),
        None => None
    };

    NumPics { number, identifier }
}

fn analyze_transform_argument(pair:Pair<Rule>) -> Option<String> {
    match pair.as_rule() {
        Rule::blank_argument => None,
        Rule::expression => Some(pair.as_str().to_string()),
        _ => unreachable!()
    }
}

fn analyze_transform_arguments(pairs:&mut Pairs<Rule>) -> (Option<String>, Option<String>, Option<String>) {
    let x = analyze_transform_argument(pairs.next().unwrap());
    let y = analyze_transform_argument(pairs.next().unwrap());
    let z = analyze_transform_argument(pairs.next().unwrap());
    (x, y, z)
}

fn analyze_transforms(pairs:&mut Pairs<Rule>) -> Vec<Transform> {
    let mut transforms : Vec<Transform> = vec![];
    for pair in pairs {
        let transform = match pair.as_rule() {
            Rule::translate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Translate(x, y, z)
            },
            Rule::scale_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Scale(x, y, z)
            },
            Rule::rotate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Rotate(x, y, z)
            },
            _ => unreachable!()
        };
        transforms.push(transform);
    }
    transforms
}

fn analyze_transform_expression(pairs:&mut Pairs<Rule>) -> Option<Vec<String>> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::expression_parens => {
            let mut code = pairs.next().unwrap().as_str().to_string();
            code.pop();
            Some(code[1..]
                .split("\n")
                .map(|l| l.trim().to_string())
                .collect(),
        )},
        _ => None,
    }
}

fn analyze_transform_set(pairs:&mut Pairs<Rule>) -> TransformSet {
    let num_pics = analyze_num_pics(&mut pairs.next().unwrap().into_inner());
    let top_level_expression = analyze_transform_expression(pairs);
    let transforms = analyze_transforms(pairs);
    let iteration = match num_pics.number.parse::<i32>() {
        Ok(n) => n > 1,
        _ => true
    };
    
    TransformSet { num_pics, top_level_expression, transforms, iteration }
}

fn analyze_transform_sets(pairs:&mut Pairs<Rule>) -> Operations {
    let mut operations:Vec<TransformSet> = vec![];
    
    for pair in pairs {
        if pair.as_rule() != Rule::transform_set {
            panic_span(pair.as_span(), "Cannot mix transform sets and CSG operations");
        }
        let transform_set = analyze_transform_set(&mut pair.into_inner());
        operations.push(transform_set);
    }

    Operations::TransformSet(operations)
}

fn analyze_csg_operation(pairs:&mut Pairs<Rule>) -> Csg {
    match pairs.next().unwrap().as_str() {
        "+" => Csg::Union(analyze_invoke(pairs)),
        "-" => Csg::Difference(analyze_invoke(pairs)),
        "n" => Csg::Intersection(analyze_invoke(pairs)),
        x => unreachable!("unsupported csg operator {:?}", x)
    }
}

fn analyze_csg_operations(pairs:&mut Pairs<Rule>) -> Operations {
    let mut operations:Vec<Csg> = vec![];

    for pair in pairs {
        if pair.as_rule() != Rule::csg_operation {
            panic_span(pair.as_span(), "Cannot mix transform sets and CSG operations");
        }

        let csg_operation = analyze_csg_operation(&mut pair.into_inner());
        operations.push(csg_operation);
    }

    Operations::Csg(operations)
}

fn analyze_operations(pairs:&mut Pairs<Rule>) -> Operations {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_set =>
            analyze_transform_sets(pairs),
        Some(x) if x.as_rule() == Rule::csg_operation =>
            analyze_csg_operations(pairs),
        _ => unreachable!()
    }
}

fn analyze_picture(pairs:&mut Pairs<Rule>) -> Picture {
    let mut pairs = pairs;
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(&mut pairs);
    let basis = analyze_invoke(&mut pairs.next().unwrap().into_inner());
    let operations = analyze_operations(&mut pairs);

    Picture { identifier, parameters, basis, operations }
}

fn analyze_picture_list(pairs:&mut Pairs<Rule>) -> PictureList {
    let identifier = pairs.next().unwrap().as_str().to_string();

    let mut invokes:Vec<Invoke> = vec![];
    invokes.push(analyze_invoke(pairs));
    while pairs.peek().is_some() {
        invokes.push(analyze_invoke(pairs))
    }

    PictureList { identifier, invokes }
}

fn analyze_definition(pairs:&mut Pairs<Rule>) -> Definition {
    match pairs.peek().unwrap().as_rule() {
        Rule::standard_picture => Definition::Standard(analyze_picture(&mut pairs.next().unwrap().into_inner())),
        Rule::picture_function => Definition::Function(analyze_picture(&mut pairs.next().unwrap().into_inner())),
        Rule::picture_selection => Definition::Selection(analyze_picture_list(&mut pairs.next().unwrap().into_inner())),
        _ => unreachable!()
    }
}

pub fn analyze_top_level(pair:Pair<Rule>) -> TopLevel {
    match pair.as_rule() {
        Rule::film =>
            TopLevel::Film(analyze_film(&mut pair.into_inner())),
        Rule::python_code =>
            TopLevel::PythonCodeBlock(analyze_python_code(&mut pair.into_inner())),
        Rule::picture_definition =>
            TopLevel::Definition(analyze_definition(&mut pair.into_inner())),
        Rule::EOI => TopLevel::Skip,
        _ => unreachable!()
    }
}

#[cfg(test)]
mod tests {
    use std::fs;
    use super::*;
    use crate::parser::parse_source;

    fn test_analyzes(path: &str) {
        let source = fs::read_to_string(&path).expect("cannot read file");
        let pairs = parse_source(&source, &path);
        for pair in pairs {
            analyze_top_level(pair);
        }
    }
    
    #[test]
    fn test_case_01() { test_analyzes("cases/test_case_01.osk"); }
    #[test]
    fn test_case_02() { test_analyzes("cases/test_case_02.osk"); }
    #[test]
    fn test_case_03() { test_analyzes("cases/test_case_03.osk"); }
    #[test]
    fn test_case_04_1() { test_analyzes("cases/test_case_04.1.osk"); }
    #[test]
    fn test_case_04_2() { test_analyzes("cases/test_case_04.2.osk"); }
    #[test]
    fn test_case_04_3() { test_analyzes("cases/test_case_04.3.osk"); }
    #[test]
    fn test_case_04_5() { test_analyzes("cases/test_case_04.5.osk"); }
    #[test]
    fn test_case_04_6a() { test_analyzes("cases/test_case_04.6a.osk"); }
    #[test]
    fn test_case_04a() { test_analyzes("cases/test_case_04a.osk"); }
    #[test]
    fn test_case_07_5a() { test_analyzes("cases/test_case_07.5a.osk"); }
    #[test]
    fn test_case_07_5b() { test_analyzes("cases/test_case_07.5b.osk"); }
    #[test]
    fn test_case_07_5() { test_analyzes("cases/test_case_07.5.osk"); }
    #[test]
    fn test_case_07_6() { test_analyzes("cases/test_case_07.6.osk"); }
    #[test]
    fn test_case_07() { test_analyzes("cases/test_case_07.osk"); }
    #[test]
    fn test_case_09() { test_analyzes("cases/test_case_09.osk"); }
}