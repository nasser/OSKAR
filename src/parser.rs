use pest::error::*;
use pest::Parser;
use std::fs;

#[derive(Parser, Debug)]
#[grammar = "grammar.pest"]
struct OskarParser;

fn print_error(e: Error<Rule>, path: &str) {
    match e.line_col {
        LineColLocation::Pos((l, c)) => println!("{} ({}:{}:{})", e, path, l, c),
        LineColLocation::Span((sl, sc), _) => println!("{} ({}:{}:{})", e, path, sl, sc),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_compiles(path: &str) {
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
    fn test_case_01() { test_compiles("cases/test_case_01.osk"); }
    #[test]
    fn test_case_02() { test_compiles("cases/test_case_02.osk"); }
    #[test]
    fn test_case_03() { test_compiles("cases/test_case_03.osk"); }
    #[test]
    fn test_case_04() { test_compiles("cases/test_case_04.osk"); }
    #[test]
    fn test_case_04_1() { test_compiles("cases/test_case_04.1.osk"); }
    #[test]
    fn test_case_04_2() { test_compiles("cases/test_case_04.2.osk"); }
    #[test]
    fn test_case_04_3() { test_compiles("cases/test_case_04.3.osk"); }
    #[test]
    fn test_case_04_5() { test_compiles("cases/test_case_04.5.osk"); }
    #[test]
    fn test_case_04_6a() { test_compiles("cases/test_case_04.6a.osk"); }
    #[test]
    fn test_case_04_6() { test_compiles("cases/test_case_04.6.osk"); }
    #[test]
    fn test_case_04a() { test_compiles("cases/test_case_04a.osk"); }
    #[test]
    fn test_case_04b() { test_compiles("cases/test_case_04b.osk"); }
    #[test]
    fn test_case_06_a() { test_compiles("cases/test_case_06.a.osk"); }
    #[test]
    fn test_case_06() { test_compiles("cases/test_case_06.osk"); }
    #[test]
    fn test_case_07_5a() { test_compiles("cases/test_case_07.5a.osk"); }
    #[test]
    fn test_case_07_5b() { test_compiles("cases/test_case_07.5b.osk"); }
    #[test]
    fn test_case_07_5_for_pix() { test_compiles("cases/test_case_07.5 for pix.osk"); }
    #[test]
    fn test_case_07_5() { test_compiles("cases/test_case_07.5.osk"); }
    #[test]
    fn test_case_07() { test_compiles("cases/test_case_07.osk"); }
    #[test]
    fn test_case_08() { test_compiles("cases/test_case_08.osk"); }
    #[test]
    fn test_case_09() { test_compiles("cases/test_case_09.osk"); }
    #[test]
    fn test_case_10() { test_compiles("cases/test_case_10.osk"); }
}
