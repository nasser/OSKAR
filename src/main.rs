extern crate pest;
#[macro_use]
extern crate pest_derive;
use pest::*;
use pest::error::*;
use pest::Parser;
use pest::iterators::*;

mod parser;
mod ast;

use std::fs;

use clap::Clap;

#[derive(Clap)]
#[clap(version = "1.0", author = "Ramsey Nasser <ram@nas.sr>")]
struct Opts {
    #[clap(subcommand)]
    subcommand: SubCommand,
}

#[derive(Clap)]
enum SubCommand {
    Compile(CompileOpts)
}

#[derive(Clap)]
struct CompileOpts {
    /// The file to compile
    file: String
}

#[derive(Parser, Debug)]
#[grammar = "grammar.pest"]
struct OskarParser;

fn print_error(e: Error<Rule>, path: &str) {
    match e.line_col {
        LineColLocation::Pos((l, c)) => println!("{} ({}:{}:{})", e, path, l, c),
        LineColLocation::Span((sl, sc), _) => println!("{} ({}:{}:{})", e, path, sl, sc),
    }
    panic!("could not parse")
}

fn print_parse_tree(tree: Pair<Rule>, indent: usize) {
    print!("\n{}{:?}", " ".repeat(indent), tree.as_rule());
    let mut child_count = 0;
    let span = tree.as_str();
    for t in tree.into_inner() {
        print_parse_tree(t, indent + 2);
        child_count += 1;
    }

    if child_count == 0 {
        print!(": {:?}", span);
    }
}

fn parse_source<'a>(source: &'a str, path: &str) -> Pairs<'a, Rule> {
    let sp = OskarParser::parse(Rule::start, source);
    match sp {
        Ok(res) => res,
        Err(e) => {
            print_error(e, &path);
            panic!("could not parse")
        },
    }
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

fn analyze_invoke(pairs:&mut Pairs<Rule>) -> ast::Invoke {
    let mut inner = pairs.next().unwrap().into_inner();
    let identifier = inner.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(&mut inner);
    ast::Invoke { identifier, parameters }
}

fn analyze_film_parameters(pairs:&mut Pairs<Rule>) -> Vec<(String, String)> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::film_parameters => {
            x.into_inner().map(|p| {
                let mut inner = p.into_inner();
                (inner.next().unwrap().as_str().to_string(),
                 inner.next().unwrap().as_str().to_string())
            }).collect()
        }
        _ => vec![]
    }
}

fn analyze_film(pairs:&mut Pairs<Rule>) -> ast::Film {
    let film_identifier = pairs.next().unwrap();
    if film_identifier.as_str() != "Film" {
        panic_span(film_identifier.as_span(), "Film name must be exactly 'Film'");
    }
    let picture = analyze_invoke(pairs);
    let film_parameters = analyze_film_parameters(pairs);

    ast::Film { picture, film_parameters }
}

fn analyze_python_code(pairs:&mut Pairs<Rule>) -> ast::PythonCodeBlock {
    let mut lines = "".to_owned();
    for pair in pairs {
        lines.push_str(pair.as_str());
    }
    ast::PythonCodeBlock { lines }
}

fn analyze_num_pics(pairs:&mut Pairs<Rule>) -> ast::NumPics {
    let number = pairs.next().unwrap().as_str().to_string();
    let identifier = match pairs.peek() {
        Some(x) => Some(x.as_str().to_string()),
        None => None
    };

    ast::NumPics { number, identifier }
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

fn analyze_transforms(pairs:&mut Pairs<Rule>) -> Vec<ast::Transform> {
    let mut transforms : Vec<ast::Transform> = vec![];
    for pair in pairs {
        let transform = match pair.as_rule() {
            Rule::translate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                ast::Transform::Translate(x, y, z)
            },
            Rule::scale_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                ast::Transform::Scale(x, y, z)
            },
            Rule::rotate_transform => {
                let (x, y, z) = analyze_transform_arguments(&mut pair.into_inner());
                ast::Transform::Rotate(x, y, z)
            },
            _ => unreachable!()
        };
        transforms.push(transform);
    }
    transforms
}

fn analyze_transform_expression(pairs:&mut Pairs<Rule>) -> Option<String> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::expression_parens =>
            Some(pairs.next().unwrap().as_str().to_string()),
        _ => None
    }
}

fn analyze_transform_set(pairs:&mut Pairs<Rule>) -> ast::TransformSet {
    let num_pics = analyze_num_pics(&mut pairs.next().unwrap().into_inner());
    let top_level_expression = analyze_transform_expression(pairs);
    let transforms = analyze_transforms(pairs);
    
    ast::TransformSet { num_pics, top_level_expression, transforms }
}

fn analyze_transform_sets(pairs:&mut Pairs<Rule>) -> Vec<ast::Operation> {
    let mut operations:Vec<ast::Operation> = vec![];
    
    for pair in pairs {
        if pair.as_rule() != Rule::transform_set {
            panic_span(pair.as_span(), "Cannot mix transform sets and CSG operations");
        }
        let transform_set = ast::Operation::TransformSet(analyze_transform_set(&mut pair.into_inner()));
        operations.push(transform_set);
    }

    operations
}

fn analyze_csg_operations(pairs:&mut Pairs<Rule>) -> Vec<ast::Operation> {
    for pair in pairs {
        if pair.as_rule() != Rule::csg_operation {
            panic_span(pair.as_span(), "Cannot mix transform sets and CSG operations");
        }
    }
    panic!("CSG Operations")
}

fn analyze_operations(pairs:&mut Pairs<Rule>) -> Vec<ast::Operation> {
    match pairs.peek() {
        Some(x) if x.as_rule() == Rule::transform_set =>
            analyze_transform_sets(pairs),
        Some(x) if x.as_rule() == Rule::csg_operation =>
            analyze_csg_operations(pairs),
        _ => unreachable!()
    }
}

fn analyze_picture(pairs:&mut Pairs<Rule>) -> ast::Picture {
    let mut pairs = pairs;
    let identifier = pairs.next().unwrap().as_str().to_string();
    let parameters = analyze_parameters(&mut pairs);
    let basis = analyze_invoke(&mut pairs);
    let operations = analyze_operations(&mut pairs);

    ast::Picture { identifier, parameters, basis, operations }
}

fn analyze_definition(pairs:&mut Pairs<Rule>) -> ast::Definition {
    match pairs.peek().unwrap().as_rule() {
        Rule::standard_picture => ast::Definition::Standard(analyze_picture(&mut pairs.next().unwrap().into_inner())),
        Rule::picture_function => ast::Definition::Function(analyze_picture(&mut pairs.next().unwrap().into_inner())),
        Rule::picture_selection => panic!("Picture Lists"),
        _ => unreachable!()
    }
}

fn analyze_top_level(pair:Pair<Rule>) -> ast::TopLevel {
    match pair.as_rule() {
        Rule::film =>
            ast::TopLevel::Film(analyze_film(&mut pair.into_inner())),
        Rule::python_code =>
            ast::TopLevel::PythonCodeBlock(analyze_python_code(&mut pair.into_inner())),
        Rule::picture_definition =>
            ast::TopLevel::Definition(analyze_definition(&mut pair.into_inner())),
        Rule::EOI => ast::TopLevel::Skip,
        _ => unreachable!()
    }
}

fn compile(path: String) {
    let source = fs::read_to_string(&path).expect("cannot read file");
    let pairs = parse_source(&source, &path);
    for pair in pairs {
        let x = analyze_top_level(pair);
        println!("[toplevel] {:#?}", x);
    }
}

fn main() {
    let opts = Opts::parse();
    match opts.subcommand {
        SubCommand::Compile(c) => compile(c.file)
    }
}
