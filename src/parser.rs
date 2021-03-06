use pest::error::*;
use pest::iterators::*;
use pest::Parser;
use std::process;

#[derive(Parser, Debug)]
#[grammar = "grammar.pest"]
pub struct OskarParser;

fn print_error(e: Error<Rule>, path: &str) {
    eprintln!("ERROR in OSKAR syntax in file '{}'", path);
    match e.line_col {
        LineColLocation::Pos((l, c)) => eprintln!("{} ({}:{}:{})", e, path, l, c),
        LineColLocation::Span((sl, sc), _) => eprintln!("{} ({}:{}:{})", e, path, sl, sc),
    }
    process::exit(1)
}

pub fn parse_source<'a>(source: &'a str, path: &str) -> Pairs<'a, Rule> {
    let sp = OskarParser::parse(Rule::start, source);
    match sp {
        Ok(res) => res,
        Err(e) => {
            print_error(e, &path);
            panic!("could not parse")
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pest::error::*;
    use pest::Parser;
    use std::fs;

    fn print_error(e: Error<Rule>, path: &str) {
        match e.line_col {
            LineColLocation::Pos((l, c)) => println!("{} ({}:{}:{})", e, path, l, c),
            LineColLocation::Span((sl, sc), _) => println!("{} ({}:{}:{})", e, path, sl, sc),
        }
    }

    fn test_parses(path: &str) {
        let source = fs::read_to_string(path).expect("cannot read file");
        match OskarParser::parse(Rule::start, &source) {
            Err(e) => {
                print_error(e, path);
                panic!("parse failed");
            }
            _ => (),
        }
    }
    #[test]
    fn test_case_01() {
        test_parses("cases/test_case_01.osk");
    }
    #[test]
    fn test_case_02() {
        test_parses("cases/test_case_02.osk");
    }
    #[test]
    fn test_case_03() {
        test_parses("cases/test_case_03.osk");
    }
    #[test]
    fn test_case_04_1() {
        test_parses("cases/test_case_04.1.osk");
    }
    #[test]
    fn test_case_04_2() {
        test_parses("cases/test_case_04.2.osk");
    }
    #[test]
    fn test_case_04_3() {
        test_parses("cases/test_case_04.3.osk");
    }
    #[test]
    fn test_case_04_5() {
        test_parses("cases/test_case_04.5.osk");
    }
    #[test]
    fn test_case_04_6a() {
        test_parses("cases/test_case_04.6a.osk");
    }
    #[test]
    fn test_case_04a() {
        test_parses("cases/test_case_04a.osk");
    }
    #[test]
    fn test_case_07_5a() {
        test_parses("cases/test_case_07.5a.osk");
    }
    #[test]
    fn test_case_07_5b() {
        test_parses("cases/test_case_07.5b.osk");
    }
    #[test]
    fn test_case_07_5() {
        test_parses("cases/test_case_07.5.osk");
    }
    #[test]
    fn test_case_07_6() {
        test_parses("cases/test_case_07.6.osk");
    }
    #[test]
    fn test_case_07() {
        test_parses("cases/test_case_07.osk");
    }
    #[test]
    fn test_case_09() {
        test_parses("cases/test_case_09.osk");
    }
}
