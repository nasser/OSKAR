use pest::error::*;
use pest::iterators::*;
use pest::Parser;

#[derive(Parser, Debug)]
#[grammar = "grammar.pest"]
pub struct OskarParser;

pub fn parse_source<'a>(source: &'a str) -> Result<Pairs<'a, Rule>, Error<Rule>> {
    OskarParser::parse(Rule::start, source)
}

#[cfg(test)]
mod tests {
    use super::*;
    use pest::Parser;
    use std::fs;
    use test_case::test_case;

    fn print_error(e: Error<Rule>, path: &str) {
        match e.line_col {
            LineColLocation::Pos((l, c)) => println!("{} ({}:{}:{})", e, path, l, c),
            LineColLocation::Span((sl, sc), _) => println!("{} ({}:{}:{})", e, path, sl, sc),
        }
    }

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
    fn parses(path: &str) {
        let source = fs::read_to_string(path).expect("cannot read file");
        match OskarParser::parse(Rule::start, &source) {
            Err(e) => {
                print_error(e, path);
                panic!("parse failed");
            }
            _ => (),
        }
    }
}
