use pest::iterators::*;
use pest::*;
use python_parser::ast as py;

use crate::parser::Rule;

type ParseError = pest::error::Error<()>;

type PythonExpression = py::Expression;
type PythonStatements = Vec<py::Statement>;

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
    Selection(PictureList),
}

#[derive(Debug)]
pub struct PictureList {
    pub identifier: String,
    pub invokes: Vec<Invoke>,
}

#[derive(Debug)]
pub struct Picture {
    pub identifier: String,
    pub parameters: Vec<String>,
    pub basis: Invoke,
    pub operations: Operations,
}

#[derive(Debug)]
pub enum Operations {
    TransformSet(Vec<TransformSet>),
    Csg(Vec<Csg>),
}

#[derive(Debug)]
pub enum Csg {
    Union(Invoke),
    Difference(Invoke),
    Intersection(Invoke),
    Concatenation(Invoke),
}

#[derive(Debug)]
pub struct TransformSet {
    pub num_pics: NumPics,
    pub statements: Option<PythonStatements>,
    pub transforms: Vec<Transform>,
    // pub iteration: bool,
}

#[derive(Debug)]
pub struct NumPics {
    pub value: PythonExpression,
    pub nth_identifier: String,
    pub pct_identifier: String,
}

type PythonExpressionTriple = (PythonExpression, PythonExpression, PythonExpression);

#[derive(Debug)]
pub enum Transform {
    Scale(PythonExpressionTriple),
    Translate(PythonExpressionTriple),
    Rotate(PythonExpressionTriple),
    Color(PythonExpressionTriple),
}

#[derive(Debug)]
pub struct Film {
    pub picture: Invoke,
    pub frames: PythonExpression,
}

#[derive(Debug, Clone)]
pub struct Invoke {
    pub identifier: String,
    pub parameters: Vec<Parameter>,
}

#[derive(Debug, Clone)]
pub enum Parameter {
    Simple(PythonExpression),
    KeyValue(String, PythonExpression),
}

#[derive(Debug)]
pub struct PythonCodeBlock {
    pub lines: PythonStatements,
}

fn error_from_span(span: &Span, message: &str) -> ParseError {
    pest::error::Error::new_from_span(
        pest::error::ErrorVariant::<()>::CustomError {
            message: message.to_owned(),
        },
        *span,
    )
}

fn fake_span(code: &str) -> Span {
    Span::new(code, 0, code.len()).unwrap()
}

pub fn to_python_statements(codes: &Vec<Span>) -> Result<PythonStatements, ParseError> {
    let mut statements = vec![];
    for code in codes {
        match python_parser::file_input(python_parser::make_strspan(code.as_str())) {
            Ok((_, ref mut s)) => statements.append(s),
            Err(_) => return Err(error_from_span(code, "python parse error")),
        }
    }
    Ok(statements)
}

pub fn to_python_expression(code: &Span) -> Result<PythonExpression, ParseError> {
    match to_python_statements(&vec![*code]) {
        Ok(s) if s.len() == 1 => match &s[0] {
            py::Statement::Assignment(lhs, _) if lhs.len() == 1 => Ok(lhs[0].clone()),
            _ => Err(error_from_span(
                code,
                "python expression parse error (expected py::Statement::Assignment)",
            )),
        },
        Ok(s) => Err(error_from_span(
            code,
            &format!("expected 1 expression, got {}", s.len()),
        )),
        Err(description) => Err(description),
    }
}

fn analyze_parameters(pairs: &mut Pairs<Rule>) -> Result<Vec<Parameter>, ParseError> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::parameters => {
            let param_pairs = pairs.next().unwrap().into_inner();
            let mut params = vec![];
            for p in param_pairs {
                match p.as_rule() {
                    Rule::expression => {
                        params.push(Parameter::Simple(to_python_expression(&p.as_span())?))
                    }
                    Rule::named_expression => {
                        let mut kv = p.into_inner();
                        params.push(Parameter::KeyValue(
                            kv.next().unwrap().as_str().to_string(),
                            to_python_expression(&kv.next().unwrap().as_span())?,
                        ));
                    }
                    _ => unreachable!(),
                }
            }
            Ok(params)
        }
        _ => Ok(vec![]),
    }
}

fn analyze_parameters_names(pairs: &mut Pairs<Rule>) -> Result<Vec<String>, ParseError> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::parameters => {
            let param_pairs = pairs.next().unwrap().into_inner();
            let mut params = vec![];
            for p in param_pairs {
                match p.as_rule() {
                    Rule::expression => params.push(p.as_str().to_owned()),
                    Rule::named_expression => {
                        return Err(error_from_span(
                            &p.as_span(),
                            "key-value pairs not supported here",
                        ))
                    }
                    _ => unreachable!(),
                }
            }
            Ok(params)
        }
        _ => Ok(vec![]),
    }
}

fn analyze_invoke(pairs: &mut Pairs<Rule>) -> Result<Invoke, ParseError> {
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(pairs)?;
    Ok(Invoke {
        identifier,
        parameters,
    })
}

fn analyze_film_parameters<'a>(pairs: &mut Pairs<'a, Rule>) -> Vec<(String, Span<'a>)> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::film_parameters => x
            .into_inner()
            .map(|p| {
                let mut inner = p.into_inner();
                (
                    inner.next().unwrap().as_str().trim().to_string(),
                    inner.next().unwrap().as_span(),
                )
            })
            .collect(),
        _ => vec![],
    }
}

fn analyze_film(pairs: &mut Pairs<Rule>) -> Result<Film, ParseError> {
    let film_identifier = pairs.next().unwrap();
    if film_identifier.as_str() != "Film" {
        return Err(error_from_span(
            &film_identifier.as_span(),
            "Film name must be exactly 'Film'",
        ));
    }
    let picture = analyze_invoke(&mut pairs.next().unwrap().into_inner())?;

    let mut frames = fake_span("250");
    for (name, value) in analyze_film_parameters(pairs) {
        match name.to_lowercase().as_str() {
            "frames" => frames = value,
            _ => {}
        }
    }

    Ok(Film {
        picture,
        frames: to_python_expression(&frames)?,
    })
}

fn analyze_python_code(pairs: &mut Pairs<Rule>) -> Result<PythonCodeBlock, ParseError> {
    let mut lines = vec![];
    for pair in pairs {
        lines.push(pair.as_span());
    }
    Ok(PythonCodeBlock {
        lines: to_python_statements(&lines)?,
    })
}

fn analyze_num_pics(pairs: &mut Pairs<Rule>) -> Result<NumPics, ParseError> {
    let p = pairs.next().unwrap();
    let value = to_python_expression(&p.as_span())?;
    let mut nth_identifier = "nth".to_string();
    let mut pct_identifier = "pct".to_string();
    match pairs.next() {
        Some(x) => match x.as_rule() {
            Rule::identifier => nth_identifier = x.as_str().to_string(),
            Rule::blank_argument => (),
            _ => unreachable!(),
        },
        _ => (),
    };
    match pairs.next() {
        Some(x) => match x.as_rule() {
            Rule::identifier => pct_identifier = x.as_str().to_string(),
            Rule::blank_argument => (),
            _ => unreachable!(),
        },
        _ => (),
    };

    Ok(NumPics {
        value,
        nth_identifier,
        pct_identifier,
    })
}

fn analyze_transform_argument(pair: Pair<Rule>) -> Option<Span> {
    match pair.as_rule() {
        Rule::blank_argument => None,
        Rule::expression => Some(pair.as_span()),
        _ => unreachable!(),
    }
}

fn analyze_transform_arguments<'a>(
    pairs: &mut Pairs<'a, Rule>,
) -> (Option<Span<'a>>, Option<Span<'a>>, Option<Span<'a>>) {
    let x = analyze_transform_argument(pairs.next().unwrap());
    let y = analyze_transform_argument(pairs.next().unwrap());
    let z = analyze_transform_argument(pairs.next().unwrap());
    (x, y, z)
}

fn default(v: Option<Span>, default: &str) -> Result<PythonExpression, ParseError> {
    let default_span = fake_span(default);
    to_python_expression(match v {
        None => &default_span,
        Some(ref vv) => vv,
    })
}

fn analyze_transforms(pairs: &mut Pairs<Rule>) -> Result<Vec<Transform>, ParseError> {
    let mut transforms: Vec<Transform> = vec![];
    for pair in pairs {
        let transform = match pair.as_rule() {
            Rule::translate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Translate((default(x, "0")?, default(y, "0")?, default(z, "0")?))
            }
            Rule::scale_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Scale((default(x, "1")?, default(y, "1")?, default(z, "1")?))
            }
            Rule::rotate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Rotate((default(x, "0")?, default(y, "0")?, default(z, "0")?))
            }
            Rule::color_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Color((default(x, "1")?, default(y, "1")?, default(z, "1")?))
            }
            _ => unreachable!(),
        };
        transforms.push(transform);
    }
    Ok(transforms)
}

fn analyze_transform_expression(
    pairs: &mut Pairs<Rule>,
) -> Result<Option<PythonStatements>, ParseError> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::expression_parens => {
            let code = pairs.next().unwrap().into_inner().next().unwrap().as_span();
            let statements = to_python_statements(&vec![code])?;
            Ok(Some(statements))
        }
        _ => Ok(None),
    }
}

fn analyze_transform_set(pairs: &mut Pairs<Rule>) -> Result<TransformSet, ParseError> {
    let num_pics = analyze_num_pics(&mut pairs.next().unwrap().into_inner())?;
    let statements = analyze_transform_expression(pairs)?;
    let transforms = analyze_transforms(pairs)?;

    Ok(TransformSet {
        num_pics,
        statements,
        transforms,
    })
}

fn analyze_transform_sets(pairs: &mut Pairs<Rule>) -> Result<Operations, ParseError> {
    let mut operations: Vec<TransformSet> = vec![];
    for pair in pairs {
        if pair.as_rule() != Rule::transform_set {
            return Err(error_from_span(
                &pair.as_span(),
                "Cannot mix transform sets and CSG operations",
            ));
        }
        let transform_set = analyze_transform_set(&mut pair.into_inner())?;
        operations.push(transform_set);
    }

    Ok(Operations::TransformSet(operations))
}

fn analyze_csg_operation(pairs: &mut Pairs<Rule>) -> Result<Csg, ParseError> {
    Ok(match pairs.next().unwrap().as_str() {
        "+" => Csg::Union(analyze_invoke(pairs)?),
        "-" => Csg::Difference(analyze_invoke(pairs)?),
        "n" => Csg::Intersection(analyze_invoke(pairs)?),
        "&" => Csg::Concatenation(analyze_invoke(pairs)?),
        x => unreachable!("unsupported csg operator {:?}", x),
    })
}

fn analyze_csg_operations(pairs: &mut Pairs<Rule>) -> Result<Operations, ParseError> {
    let mut operations: Vec<Csg> = vec![];

    for pair in pairs {
        if pair.as_rule() != Rule::csg_operation {
            return Err(error_from_span(
                &pair.as_span(),
                "Cannot mix transform sets and CSG operations",
            ));
        }

        let csg_operation = analyze_csg_operation(&mut pair.into_inner())?;
        operations.push(csg_operation);
    }

    Ok(Operations::Csg(operations))
}

fn analyze_operations(pairs: &mut Pairs<Rule>) -> Result<Operations, ParseError> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_set => analyze_transform_sets(pairs),
        Some(x) if x.as_rule() == Rule::csg_operation => analyze_csg_operations(pairs),
        _ => unreachable!(),
    }
}

fn analyze_picture(pairs: &mut Pairs<Rule>) -> Result<Picture, ParseError> {
    let mut pairs = pairs;
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters_names(&mut pairs)?;
    let basis = analyze_invoke(&mut pairs.next().unwrap().into_inner())?;
    let operations = analyze_operations(&mut pairs)?;

    Ok(Picture {
        identifier,
        parameters,
        basis,
        operations,
    })
}

fn analyze_picture_list(pairs: &mut Pairs<Rule>) -> Result<PictureList, ParseError> {
    let identifier = pairs.next().unwrap().as_str().to_string();

    let mut invokes: Vec<Invoke> = vec![];
    invokes.push(analyze_invoke(pairs)?);
    while pairs.peek().is_some() {
        invokes.push(analyze_invoke(pairs)?)
    }

    Ok(PictureList {
        identifier,
        invokes,
    })
}

fn analyze_definition(pairs: &mut Pairs<Rule>) -> Result<Definition, ParseError> {
    Ok(match pairs.peek().unwrap().as_rule() {
        Rule::standard_picture => {
            Definition::Standard(analyze_picture(&mut pairs.next().unwrap().into_inner())?)
        }
        Rule::picture_function => {
            Definition::Function(analyze_picture(&mut pairs.next().unwrap().into_inner())?)
        }
        Rule::picture_selection => Definition::Selection(analyze_picture_list(
            &mut pairs.next().unwrap().into_inner(),
        )?),
        _ => unreachable!(),
    })
}

pub fn analyze_top_level(pair: Pair<Rule>) -> Result<TopLevel, ParseError> {
    Ok(match pair.as_rule() {
        Rule::film => TopLevel::Film(analyze_film(&mut pair.into_inner())?),
        Rule::python_code => {
            TopLevel::PythonCodeBlock(analyze_python_code(&mut pair.into_inner())?)
        }
        Rule::picture_definition => {
            TopLevel::Definition(analyze_definition(&mut pair.into_inner())?)
        }
        Rule::EOI => TopLevel::Skip,
        _ => unreachable!(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parser::parse_source;
    use std::fs;

    fn test_analyzes(path: &str) {
        let source = fs::read_to_string(&path).expect("cannot read file");
        match parse_source(&source, &path) {
            Ok(pairs) => {
                for pair in pairs {
                    match analyze_top_level(pair) {
                        Err(_) => panic!(),
                        _ => {}
                    }
                }
            }
            Err(_) => panic!(),
        }
    }
    #[test]
    fn test_case_01() {
        test_analyzes("cases/test_case_01.osk");
    }
    #[test]
    fn test_case_02() {
        test_analyzes("cases/test_case_02.osk");
    }
    #[test]
    fn test_case_03() {
        test_analyzes("cases/test_case_03.osk");
    }
    #[test]
    fn test_case_04_1() {
        test_analyzes("cases/test_case_04.1.osk");
    }
    #[test]
    fn test_case_04_2() {
        test_analyzes("cases/test_case_04.2.osk");
    }
    #[test]
    fn test_case_04_3() {
        test_analyzes("cases/test_case_04.3.osk");
    }
    #[test]
    fn test_case_04_5() {
        test_analyzes("cases/test_case_04.5.osk");
    }
    #[test]
    fn test_case_04_6a() {
        test_analyzes("cases/test_case_04.6a.osk");
    }
    #[test]
    fn test_case_04a() {
        test_analyzes("cases/test_case_04a.osk");
    }
    #[test]
    fn test_case_07_5a() {
        test_analyzes("cases/test_case_07.5a.osk");
    }
    #[test]
    fn test_case_07_5b() {
        test_analyzes("cases/test_case_07.5b.osk");
    }
    #[test]
    fn test_case_07_5() {
        test_analyzes("cases/test_case_07.5.osk");
    }
    #[test]
    fn test_case_07_6() {
        test_analyzes("cases/test_case_07.6.osk");
    }
    #[test]
    fn test_case_07() {
        test_analyzes("cases/test_case_07.osk");
    }
    #[test]
    fn test_case_09() {
        test_analyzes("cases/test_case_09.osk");
    }
}
