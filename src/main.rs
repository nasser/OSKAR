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

fn analyze_invoke(pairs:&mut Pairs<Rule>) -> ast::Invoke {
    let mut inner = pairs.next().unwrap().into_inner();
    let identifier = inner.next().unwrap().as_str().to_string();
    let parameters = match inner.peek() {
        Some(x) if x.as_rule() == Rule::parameters 
            => x.into_inner().map(|p| p.as_str().to_string()).collect(),
        _ => vec![]
    };

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

fn analyze_picture(pairs:&mut Pairs<Rule>) -> ast::Picture {
    panic!("TODO")
}

fn analyze_definition(pairs:&mut Pairs<Rule>) -> ast::Definition {
    match pairs.peek().unwrap().as_rule() {
        Rule::standard_picture => ast::Definition::Standard(analyze_picture(&mut pairs.next().unwrap().into_inner())),
        Rule::picture_function => ast::Definition::Function,
        Rule::picture_selection => ast::Definition::Selection,
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
        println!("[toplevel] {:?}", x);
    }
}

fn main() {
    let opts = Opts::parse();
    match opts.subcommand {
        SubCommand::Compile(c) => compile(c.file)
    }
}
