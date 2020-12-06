use crate::ast as osk;
use python_parser::ast as py;
use python_parser::visitors::printer::format_module;

fn py_string(s: &str) -> py::Expression {
    py::Expression::String(vec![py::PyString {
        prefix: "".to_string(),
        content: s.to_string(),
    }])
}

fn py_print(args: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        Box::new(py::Expression::Name("print".to_string())),
        args.into_iter()
            .map(|a| py::Argument::Positional(a))
            .collect(),
    )
}

pub fn to_python_ast(tl: osk::TopLevel) -> py::Statement {
    let e = match tl {
        osk::TopLevel::Film(f) => {
            py_print(vec![py_string("[film]"), py_string(&f.picture.identifier)])
        }
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => py_print(vec![
            py_string("[standard picture]"),
            py_string(&p.identifier),
            py_string(&p.basis.identifier)
        ]),
        _ => py_print(vec![py_string("?")]),
    };

    py::Statement::Expressions(vec![e])
}

pub fn to_python_source(tl: osk::TopLevel) -> String {
    let stmts = vec![to_python_ast(tl)];
    format_module(&stmts)
}
