use pest::iterators::*;
use pest::*;

use crate::parser::Rule;

use crate::python as py;

#[derive(Debug)]
/// OSKAR Analyzer Error
///
/// Captures the minimal amount of information required to report an error in
/// the analysis phase. Certain things like line number and file name are not
/// accessible to us here and can only be derived at the top level of the
/// compiler. The data in this struct is incomplete and exists solely to help
/// the top level report the error correctly.
pub struct Error {
    /// the span that generated the error, offsets into original source
    pub span: (usize, usize),
    /// the offset in lines into the span to focus the error on
    pub line_offset: usize,
    /// the offset in columns into the span to focus the error on
    pub column_offset: usize,
    /// a description of the error
    pub message: String,
}

fn get_line_col(source: &str, offset: usize) -> Option<(usize, usize)> {
    let mut line_number = 1;
    let mut current_offset = 0;

    for line in source.lines() {
        let line_length = line.len() + 1;
        if current_offset + line_length > offset {
            return Some((line_number, offset - current_offset));
        }
        line_number += 1;
        current_offset += line_length;
    }

    None
}

/// Format an analysis error
///
/// File and source are not known to us in this module and must be passed in
/// from the top level of the compiler
pub fn format_error(error: &Error, file: &str, source: &str) -> String {
    eprintln!("{:?}", error);
    let (start_line, start_col) =
        get_line_col(&source, error.span.0).expect("error span out of bounds of source");
    let line = error.line_offset + start_line - 1;
    let column = error.column_offset + start_col;
    let line_content = source
        .lines()
        .nth(line - 1)
        .expect("error line out of bounds of source");
    let spacing = String::from_utf8(vec![b' '; line.to_string().len()]).unwrap();
    let mut carat = String::from_utf8(vec![b' '; column - 1]).unwrap();
    carat.push('^');
    format!(
        "{s    }--> {p}:{ls}:{c}\n\
            {s    } |\n\
            {ls:w$} | {line}\n\
            {s    } | {carat}\n\
            {s    } |\n\
            {s    } = {message}",
        s = spacing,
        w = spacing.len(),
        p = file,
        ls = line,
        c = column,
        line = line_content,
        message = error.message
    )
}

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
    pub elements: Vec<String>,
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
    pub statement: Option<py::AST>,
    pub transforms: Vec<Transform>,
    // pub iteration: bool,
}

#[derive(Debug)]
pub struct NumPics {
    pub value: py::AST,
    pub nth_identifier: String,
    pub pct_identifier: String,
}

type PythonExpressionTriple = (py::AST, py::AST, py::AST);

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
    pub frames: py::AST,
}

#[derive(Debug, Clone)]
pub struct Invoke {
    pub identifier: String,
    pub parameters: Vec<Parameter>,
}

#[derive(Debug, Clone)]
pub enum Parameter {
    Simple(py::AST),
    KeyValue(String, py::AST),
}

#[derive(Debug)]
pub struct PythonCodeBlock {
    pub lines: py::AST,
}

fn error_from_span(span: &Span, message: &str) -> Error {
    let (line_number, column_number) = span.start_pos().line_col();
    Error {
        line_offset: line_number,
        column_offset: column_number,
        message: message.to_owned(),
        span: (span.start(), span.end()),
    }
}

fn error_from_python(span: &Span, error: &py::Error) -> Error {
    println!("error_from_python {}", error.offset);
    Error {
        line_offset: error.line,
        column_offset: error.offset,
        message: format!("python error: {}", error.message),
        span: (span.start(), span.end()),
    }
}

fn error_from_python_trimmed(code: &str, trimmed: &str, error: &py::Error) -> Error {
    let line_original = code.lines().collect::<Vec<&str>>()[error.line - 1];
    let line_trimmed = trimmed.lines().collect::<Vec<&str>>()[error.line - 1];
    let indent = line_original.len() - line_trimmed.len();
    Error {
        line_offset: error.line,
        column_offset: error.offset + indent,
        message: format!("python error: {}", error.message),
        span: (0, 0),
    }
}

fn fake_span(code: &str) -> Span {
    Span::new(code, 0, code.len()).unwrap()
}

fn trim_lines(s: &str) -> String {
    s.lines()
        .map(|l| l.trim_start())
        .collect::<Vec<&str>>()
        .join("\n")
}

pub fn to_python_statement_trimmed(code: &str) -> Result<py::AST, Error> {
    let trimmed = trim_lines(code);
    match py::parse_exec(&trimmed) {
        Ok(v) => Ok(v),
        Err(e) => Err(error_from_python_trimmed(code, &trimmed, &e)),
    }
}

pub fn to_python_statement(code: &str, span: &Span) -> Result<py::AST, Error> {
    match py::parse_exec(code) {
        Ok(v) => Ok(v),
        Err(e) => Err(error_from_python(span, &e)),
    }
}

pub fn to_python_expression(code: &Span) -> Result<py::AST, Error> {
    match py::parse_eval(code.as_str()) {
        Ok(v) => Ok(v),
        Err(e) => return Err(error_from_python(code, &e)),
    }
}

fn analyze_parameters(pairs: &mut Pairs<Rule>) -> Result<Option<Vec<Parameter>>, Error> {
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
            Ok(Some(params))
        }
        _ => Ok(Some(vec![])),
    }
}

fn analyze_parameters_names(pairs: &mut Pairs<Rule>) -> Result<Vec<String>, Error> {
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

fn analyze_invoke(pairs: &mut Pairs<Rule>) -> Result<Invoke, Error> {
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(pairs)?.unwrap_or(vec![]);
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

fn analyze_film(pairs: &mut Pairs<Rule>) -> Result<Film, Error> {
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

fn analyze_python_code(pairs: &mut Pairs<Rule>) -> Result<PythonCodeBlock, Error> {
    let pair = pairs.next().unwrap();
    Ok(PythonCodeBlock {
        lines: to_python_statement(&pair.clone().as_str(), &pair.as_span())?,
    })
}

fn analyze_num_pics(pairs: &mut Pairs<Rule>) -> Result<NumPics, Error> {
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

fn default(v: Option<Span>, default: &str) -> Result<py::AST, Error> {
    let default_span = fake_span(default);
    to_python_expression(match v {
        None => &default_span,
        Some(ref vv) => vv,
    })
}

fn analyze_transforms(pairs: &mut Pairs<Rule>) -> Result<Vec<Transform>, Error> {
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

fn analyze_transform_expression(pairs: &mut Pairs<Rule>) -> Result<Option<py::AST>, Error> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_expressions => {
            // we parse it with the surrounding parens because that makes the
            // grammar a lot simpler. we strip them off here.
            let pair = pairs.next().unwrap();
            let mut chars = pair.clone().as_str().chars();
            chars.next();
            chars.next_back();
            let code = chars.as_str();
            let statement = to_python_statement_trimmed(&code)?;
            Ok(Some(statement))
        }
        _ => Ok(None),
    }
}

fn analyze_transform_set(pairs: &mut Pairs<Rule>) -> Result<TransformSet, Error> {
    let num_pics = analyze_num_pics(&mut pairs.next().unwrap().into_inner())?;
    let statement = analyze_transform_expression(pairs)?;
    let transforms = analyze_transforms(pairs)?;

    Ok(TransformSet {
        num_pics,
        statement,
        transforms,
    })
}

fn analyze_transform_sets(pairs: &mut Pairs<Rule>) -> Result<Operations, Error> {
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

fn analyze_csg_operation(pairs: &mut Pairs<Rule>) -> Result<Csg, Error> {
    Ok(match pairs.next().unwrap().as_str() {
        "+" => Csg::Union(analyze_invoke(pairs)?),
        "-" => Csg::Difference(analyze_invoke(pairs)?),
        "n" => Csg::Intersection(analyze_invoke(pairs)?),
        "&" => Csg::Concatenation(analyze_invoke(pairs)?),
        x => unreachable!("unsupported csg operator {:?}", x),
    })
}

fn analyze_csg_operations(pairs: &mut Pairs<Rule>) -> Result<Operations, Error> {
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

fn analyze_operations(pairs: &mut Pairs<Rule>) -> Result<Operations, Error> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_set => analyze_transform_sets(pairs),
        Some(x) if x.as_rule() == Rule::csg_operation => analyze_csg_operations(pairs),
        _ => unreachable!(),
    }
}

fn analyze_picture(pairs: &mut Pairs<Rule>) -> Result<Picture, Error> {
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

fn analyze_picture_list(pairs: &mut Pairs<Rule>) -> Result<PictureList, Error> {
    let identifier = pairs.next().unwrap().as_str().to_string();
    let mut elements: Vec<String> = vec![];
    while pairs.peek().is_some() {
        elements.push(pairs.next().unwrap().as_str().to_owned())
    }

    Ok(PictureList {
        identifier,
        elements,
    })
}

fn analyze_definition(pairs: &mut Pairs<Rule>) -> Result<Definition, Error> {
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

pub fn analyze_top_level(pair: Pair<Rule>) -> Result<TopLevel, Error> {
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
    use normalize_line_endings::normalized;
    use std::fs;
    use std::iter::FromIterator;
    use test_case::test_case;

    #[test_case("cases/test_case_01.osk"; "case 01")]
    #[test_case("cases/test_case_02.osk"; "case 02")]
    #[test_case("cases/test_case_03.osk"; "case 03")]
    #[test_case("cases/test_case_04.1.osk"; "case 04.1")]
    #[test_case("cases/test_case_04.2.osk"; "case 04.2")]
    #[test_case("cases/test_case_04.3.osk"; "case 04.3")]
    #[test_case("cases/test_case_04.5.osk"; "case 04.5")]
    #[test_case("cases/test_case_04.6a.osk"; "case 04.6a")]
    #[test_case("cases/test_case_04a.osk"; "case 04a")]
    #[test_case("cases/test_case_07.5a.osk"; "case 07.5a")]
    #[test_case("cases/test_case_07.5b.osk"; "case 07.5b")]
    #[test_case("cases/test_case_07.5.osk"; "case 07.5")]
    #[test_case("cases/test_case_07.6.osk"; "case 07.6")]
    #[test_case("cases/test_case_07.osk"; "case 07")]
    #[test_case("cases/test_case_09.osk"; "case 09")]
    fn analysis(path: &str) {
        let source = fs::read_to_string(&path).expect("cannot read file");
        let source_normalized = String::from_iter(normalized(source.chars()));
        match parse_source(&source_normalized) {
            Ok(pairs) => {
                for pair in pairs {
                    match analyze_top_level(pair) {
                        Err(e) => panic!("!!! {:?}", e),
                        _ => {}
                    }
                }
            }
            Err(_) => panic!(),
        }
    }
}
