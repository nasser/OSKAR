#[macro_use]
extern crate pest_derive;

mod parser;
use parser::parse_source;

mod ast;
use ast::analyze_top_level;

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
