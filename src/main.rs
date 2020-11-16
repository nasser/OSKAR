extern crate pest;
#[macro_use]
extern crate pest_derive;
use pest::Parser;
use pest::error::*;

mod parser;

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

fn print_error(e:Error<Rule>, path:&str) {
    match e.line_col {
        LineColLocation::Pos((l, c)) => println!("{} ({}:{}:{})", e, path, l, c),
        LineColLocation::Span((sl,sc), _) => println!("{} ({}:{}:{})", e, path, sl, sc)
    }
}

fn print_parse_tree(tree:pest::iterators::Pair<Rule>, indent:usize) {
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

fn compile(path:String) {
    let source = fs::read_to_string(&path).expect("cannot read file");
    let sp = OskarParser::parse(Rule::start, &source);
    match sp {
        // Ok(res) => println!("ok {:#?}", res),
        Ok(res) => for r in res { print_parse_tree(r, 0) }
        Err(e) => print_error(e, &path)
    }
    // for record in sp.into_inner() {
    //     match record.as_rule() {
    //         Rule::record => {
    //             println!("record {:?}", record.as_str());
    //             for field in record.into_inner() {
    //                 println!("field {:?}", field.as_str())
    //             }
    //         }
    //         Rule::EOI => println!("eoi"),
    //         _ => unreachable!()
    //     }
    // }
}

fn main() {
    let opts = Opts::parse();
    match opts.subcommand {
        SubCommand::Compile(c) => compile(c.file)
    }
}
