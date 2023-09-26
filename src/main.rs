#[macro_use]
extern crate pest_derive;

mod parser;
use parser::parse_source;

mod ast;
use ast::analyze_top_level;

mod codegen;

use std::fs;

use clap::Clap;

use std::process;

#[derive(Clap)]
#[clap(version = "1.0", author = "Ramsey Nasser <ram@nas.sr>")]
struct Opts {
    #[clap(subcommand)]
    subcommand: SubCommand,
}

#[derive(Clap)]
enum SubCommand {
    /// Compile an OSKAR file
    Compile(CompileOpts),
    /// Print the AST of a Python file (for debugging)
    Reverse(ReverseOpts),
}

#[derive(Clap)]
struct CompileOpts {
    /// The file to compile
    file: String,
}

#[derive(Clap)]
struct ReverseOpts {
    /// The file to reverse compile
    file: String,
}

// maybe move to codegen
fn comment_string(s: &str) -> String {
    let mut ret = "# ".to_string();
    ret.push_str(&s.replace("\n", "\n# "));
    ret
}

fn compile(path: String) {
    let source = fs::read_to_string(&path).expect("cannot read file");
    let mut output = String::new();
    match parse_source(&source, &path) {
        Err(e) => {
            println!("{}", e.with_path(&path));
            process::exit(1);
        }
        Ok(pairs) => {
            output.push_str(&format!(
                "### generated by the OSKAR compiler {} ({}/{}, {})",
                env!("GIT_TAG"),
                env!("GIT_BRANCH"),
                env!("GIT_HASH"),
                env!("BUILD_DATE")
            ));
            output.push_str(&format!("### from {}\n", path));

            output.push_str(&format!("{}", codegen::preamble()));

            for pair in pairs {
                let source = pair.as_str().trim_end();
                match analyze_top_level(pair) {
                    Ok(ast) => {
                        let python = codegen::to_python_source(&ast);
                        match ast {
                            ast::TopLevel::PythonCodeBlock(_) => {
                                output.push_str(&format!("{}", python))
                            }
                            ast::TopLevel::Skip => {}
                            _ => {
                                output.push_str(&format!("{}\n{}", comment_string(source), python))
                            }
                        }
                    }
                    Err(error) => {
                        println!("{}", error.with_path(&path));
                        process::exit(1);
                    }
                }
            }

            print!("{}", output);
        }
    }
}

fn reverse(path: String) {
    let source = fs::read_to_string(&path).expect("cannot read file");
    codegen::print_python_ast(&source)
}

fn main() {
    let opts = Opts::parse();
    match opts.subcommand {
        SubCommand::Compile(c) => compile(c.file),
        SubCommand::Reverse(c) => reverse(c.file),
    }
}
