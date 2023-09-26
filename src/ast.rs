use pest::iterators::*;
use pest::*;
use python_parser::ast as py;

use crate::parser::Rule;

type PythonParseError = pest::error::Error<()>;

type PythonExpression = Result<py::Expression, PythonParseError>;
type PythonStatements = Result<Vec<py::Statement>, PythonParseError>;

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

fn panic_span(span: Span, message: &str) {
    let (l, c) = span.start_pos().line_col();
    let line = span.start_pos().line_of();
    println!(
        "  | \n{} | {}\n  | {}^---\n  = {} (#file#:{}:{})",
        l,
        line,
        " ".repeat(c - 1),
        message,
        l,
        c
    );
    panic!("analysis error")
}

fn new_error(span: &Span, message: &str) -> PythonParseError {
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

pub fn to_python_statements(codes: &Vec<Span>) -> PythonStatements {
    let mut statements = vec![];
    for code in codes {
        match python_parser::file_input(python_parser::make_strspan(code.as_str())) {
            Ok((_, ref mut s)) => statements.append(s),
            Err(_) => return Err(new_error(code, "python parse error")),
        }
    }
    Ok(statements)
}

pub fn to_python_expression(code: &Span) -> PythonExpression {
    match to_python_statements(&vec![*code]) {
        Ok(s) if s.len() == 1 => match &s[0] {
            py::Statement::Assignment(lhs, _) if lhs.len() == 1 => Ok(lhs[0].clone()),
            _ => Err(new_error(
                code,
                "python expression parse error (expected py::Statement::Assignment)",
            )),
        },
        Ok(s) => Err(new_error(
            code,
            &format!("expected 1 expression, got {}", s.len()),
        )),
        Err(description) => Err(description),
    }
}

fn analyze_parameters(pairs: &mut Pairs<Rule>) -> Vec<Parameter> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::parameters => pairs
            .next()
            .unwrap()
            .into_inner()
            .map(|p| match p.as_rule() {
                Rule::expression => Parameter::Simple(to_python_expression(&p.as_span())),
                Rule::named_expression => {
                    let mut kv = p.into_inner();
                    Parameter::KeyValue(
                        kv.next().unwrap().as_str().to_string(),
                        to_python_expression(&kv.next().unwrap().as_span()),
                    )
                }
                _ => unreachable!(),
            })
            .collect(),
        _ => vec![],
    }
}

fn analyze_parameters_names(pairs: &mut Pairs<Rule>) -> Vec<String> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::parameters => pairs
            .next()
            .unwrap()
            .into_inner()
            .map(|p| match p.as_rule() {
                Rule::expression => p.as_str().to_owned(),
                Rule::named_expression => panic!(),
                _ => unreachable!(),
            })
            .collect(),
        _ => vec![],
    }
}

fn analyze_invoke(pairs: &mut Pairs<Rule>) -> Invoke {
    // let mut inner = pairs.next().unwrap().into_inner();
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(pairs);
    Invoke {
        identifier,
        parameters,
    }
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

fn analyze_film(pairs: &mut Pairs<Rule>) -> Film {
    let film_identifier = pairs.next().unwrap();
    if film_identifier.as_str() != "Film" {
        panic_span(
            film_identifier.as_span(),
            "Film name must be exactly 'Film'",
        );
    }
    let picture = analyze_invoke(&mut pairs.next().unwrap().into_inner());

    let mut frames = fake_span("250");
    for (name, value) in analyze_film_parameters(pairs) {
        match name.to_lowercase().as_str() {
            "frames" => frames = value,
            _ => {}
        }
    }

    Film {
        picture,
        frames: to_python_expression(&frames),
    }
}

fn analyze_python_code(pairs: &mut Pairs<Rule>) -> PythonCodeBlock {
    let mut lines = vec![];
    for pair in pairs {
        lines.push(pair.as_span());
    }
    PythonCodeBlock {
        lines: to_python_statements(&lines),
    }
}

fn analyze_num_pics(pairs: &mut Pairs<Rule>) -> NumPics {
    let p = pairs.next().unwrap();
    let value = to_python_expression(&p.as_span());
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

    NumPics {
        value,
        nth_identifier,
        pct_identifier,
    }
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

fn default(v: Option<Span>, default: &str) -> PythonExpression {
    let default_span = fake_span(default);
    to_python_expression(match v {
        None => &default_span,
        Some(ref vv) => vv,
    })
}

fn analyze_transforms(pairs: &mut Pairs<Rule>) -> Vec<Transform> {
    let mut transforms: Vec<Transform> = vec![];
    for pair in pairs {
        let transform = match pair.as_rule() {
            Rule::translate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Translate((default(x, "0"), default(y, "0"), default(z, "0")))
            }
            Rule::scale_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Scale((default(x, "1"), default(y, "1"), default(z, "1")))
            }
            Rule::rotate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Rotate((default(x, "0"), default(y, "0"), default(z, "0")))
            }
            Rule::color_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                Transform::Color((default(x, "1"), default(y, "1"), default(z, "1")))
            }
            _ => unreachable!(),
        };
        transforms.push(transform);
    }
    transforms
}

fn analyze_transform_expression(pairs: &mut Pairs<Rule>) -> Option<PythonStatements> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::expression_parens => {
            let code = pairs.next().unwrap().into_inner().next().unwrap().as_span();
            let statements = to_python_statements(&vec![code]);
            Some(statements)
        }
        _ => None,
    }
}

fn analyze_transform_set(pairs: &mut Pairs<Rule>) -> TransformSet {
    let num_pics = analyze_num_pics(&mut pairs.next().unwrap().into_inner());
    let top_level_expression = analyze_transform_expression(pairs);
    let transforms = analyze_transforms(pairs);
    // let iteration = match num_pics.value.parse::<i32>() {
    //     Ok(n) => n > 1,
    //     _ => true,
    // };

    TransformSet {
        num_pics,
        statements: top_level_expression,
        transforms,
        // iteration,
    }
}

fn analyze_transform_sets(pairs: &mut Pairs<Rule>) -> Operations {
    let mut operations: Vec<TransformSet> = vec![];
    for pair in pairs {
        if pair.as_rule() != Rule::transform_set {
            panic_span(
                pair.as_span(),
                "Cannot mix transform sets and CSG operations",
            );
        }
        let transform_set = analyze_transform_set(&mut pair.into_inner());
        operations.push(transform_set);
    }

    Operations::TransformSet(operations)
}

fn analyze_csg_operation(pairs: &mut Pairs<Rule>) -> Csg {
    match pairs.next().unwrap().as_str() {
        "+" => Csg::Union(analyze_invoke(pairs)),
        "-" => Csg::Difference(analyze_invoke(pairs)),
        "n" => Csg::Intersection(analyze_invoke(pairs)),
        "&" => Csg::Concatenation(analyze_invoke(pairs)),
        x => unreachable!("unsupported csg operator {:?}", x),
    }
}

fn analyze_csg_operations(pairs: &mut Pairs<Rule>) -> Operations {
    let mut operations: Vec<Csg> = vec![];

    for pair in pairs {
        if pair.as_rule() != Rule::csg_operation {
            panic_span(
                pair.as_span(),
                "Cannot mix transform sets and CSG operations",
            );
        }

        let csg_operation = analyze_csg_operation(&mut pair.into_inner());
        operations.push(csg_operation);
    }

    Operations::Csg(operations)
}

fn analyze_operations(pairs: &mut Pairs<Rule>) -> Operations {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_set => analyze_transform_sets(pairs),
        Some(x) if x.as_rule() == Rule::csg_operation => analyze_csg_operations(pairs),
        _ => unreachable!(),
    }
}

fn analyze_picture(pairs: &mut Pairs<Rule>) -> Picture {
    let mut pairs = pairs;
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters_names(&mut pairs);
    let basis = analyze_invoke(&mut pairs.next().unwrap().into_inner());
    let operations = analyze_operations(&mut pairs);

    Picture {
        identifier,
        parameters,
        basis,
        operations,
    }
}

fn analyze_picture_list(pairs: &mut Pairs<Rule>) -> PictureList {
    let identifier = pairs.next().unwrap().as_str().to_string();

    let mut invokes: Vec<Invoke> = vec![];
    invokes.push(analyze_invoke(pairs));
    while pairs.peek().is_some() {
        invokes.push(analyze_invoke(pairs))
    }

    PictureList {
        identifier,
        invokes,
    }
}

fn analyze_definition(pairs: &mut Pairs<Rule>) -> Definition {
    match pairs.peek().unwrap().as_rule() {
        Rule::standard_picture => {
            Definition::Standard(analyze_picture(&mut pairs.next().unwrap().into_inner()))
        }
        Rule::picture_function => {
            Definition::Function(analyze_picture(&mut pairs.next().unwrap().into_inner()))
        }
        Rule::picture_selection => Definition::Selection(analyze_picture_list(
            &mut pairs.next().unwrap().into_inner(),
        )),
        _ => unreachable!(),
    }
}

pub fn analyze_top_level(pair: Pair<Rule>) -> TopLevel {
    match pair.as_rule() {
        Rule::film => TopLevel::Film(analyze_film(&mut pair.into_inner())),
        Rule::python_code => TopLevel::PythonCodeBlock(analyze_python_code(&mut pair.into_inner())),
        Rule::picture_definition => {
            TopLevel::Definition(analyze_definition(&mut pair.into_inner()))
        }
        Rule::EOI => TopLevel::Skip,
        _ => unreachable!(),
    }
}

fn validate_invoke(invoke: &Invoke, python_errors: &mut Vec<PythonParseError>) {
    for p in &invoke.parameters {
        match p {
            Parameter::Simple(Err(e)) => python_errors.push(e.clone()),
            Parameter::KeyValue(_, Err(e)) => python_errors.push(e.clone()),
            _ => {}
        }
    }
}

fn validate_python_code_block(block: &PythonCodeBlock, python_errors: &mut Vec<PythonParseError>) {
    if let Err(e) = &block.lines {
        python_errors.push(e.clone());
    }
}

fn validate_film(film: &Film, python_errors: &mut Vec<PythonParseError>) {
    validate_invoke(&film.picture, python_errors);
    if let Err(e) = &film.frames {
        python_errors.push(e.clone());
    }
}

fn validate_triple(exs: &PythonExpressionTriple, python_errors: &mut Vec<PythonParseError>) {
    let (x, y, z) = exs;
    if let Err(e) = x {
        python_errors.push(e.clone());
    }
    if let Err(e) = y {
        python_errors.push(e.clone());
    }
    if let Err(e) = z {
        python_errors.push(e.clone());
    }
}

fn validate_picture(picture: &Picture, python_errors: &mut Vec<PythonParseError>) {
    validate_invoke(&picture.basis, python_errors);
    match &picture.operations {
        Operations::TransformSet(xform_sets) => {
            for x in xform_sets {
                if let Err(e) = &x.num_pics.value {
                    python_errors.push(e.clone());
                }
                if let Some(Err(e)) = &x.statements {
                    python_errors.push(e.clone());
                }
                for t in &x.transforms {
                    match t {
                        Transform::Scale(xyz) => validate_triple(xyz, python_errors),
                        Transform::Translate(xyz) => validate_triple(xyz, python_errors),
                        Transform::Rotate(xyz) => validate_triple(xyz, python_errors),
                        Transform::Color(hsl) => validate_triple(hsl, python_errors),
                    }
                }
            }
        }
        Operations::Csg(csgs) => {
            for csg in csgs {
                match csg {
                    Csg::Union(invoke) => validate_invoke(invoke, python_errors),
                    Csg::Difference(invoke) => validate_invoke(invoke, python_errors),
                    Csg::Intersection(invoke) => validate_invoke(invoke, python_errors),
                    Csg::Concatenation(invoke) => validate_invoke(invoke, python_errors),
                }
            }
        }
    }
}

fn validate_picture_list(picture_list: &PictureList, python_errors: &mut Vec<PythonParseError>) {
    for invoke in &picture_list.invokes {
        validate_invoke(invoke, python_errors);
    }
}

pub fn validate(ast: TopLevel) -> Result<TopLevel, Vec<PythonParseError>> {
    let mut python_errors = vec![];
    match &ast {
        TopLevel::Film(film) => validate_film(film, &mut python_errors),
        TopLevel::PythonCodeBlock(block) => validate_python_code_block(block, &mut python_errors),
        TopLevel::Definition(definition) => match definition {
            Definition::Standard(picture) => validate_picture(picture, &mut python_errors),
            Definition::Function(picture) => validate_picture(picture, &mut python_errors),
            Definition::Selection(picture_list) => {
                validate_picture_list(picture_list, &mut python_errors)
            }
        },
        TopLevel::Skip => {}
    }

    if python_errors.len() == 0 {
        Ok(ast)
    } else {
        Err(python_errors)
    }
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
                    analyze_top_level(pair);
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
