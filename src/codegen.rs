use crate::ast as osk;
use python_parser::ast as py;
use python_parser::visitors::printer::format_module;

fn _box<T>(t:T) -> Box<T> {
    Box::new(t)
}

fn assign(lhs:py::Expression, rhs:py::Expression) -> py::Statement {
    py::Statement::Assignment(
        vec![lhs],
        vec![vec![rhs]]
    )
}

fn name(s:&str) -> py::Expression {
    py::Expression::Name(s.to_string())
}

fn string(s: &str) -> py::Expression {
    py::Expression::String(vec![py::PyString {
        prefix: "".to_string(),
        content: s.to_string(),
    }])
}

fn py_print(args: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        Box::new(name("print")),
        args.into_iter()
            .map(|a| py::Argument::Positional(a))
            .collect(),
    )
}

fn py_print_stmt(args: Vec<py::Expression>) -> py::Statement {
    py::Statement::Expressions(vec![py_print(args)])
}

fn method_call(target:py::Expression, name:&str, arguments:Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(py::Expression::Attribute(_box(target), name.to_string())),
        arguments.into_iter().map(|a| py::Argument::Positional(a)).collect()
    )
}

fn hou_make_visible(target:py::Expression) -> py::Expression {
    method_call( target, "setDisplayFlag", vec![py::Expression::Int(1)])
}

fn codegen_film(film: osk::Film) -> py::Statement {
    py::Statement::Expressions(
        vec![hou_make_visible(name(&film.picture.identifier))]
    )
}

fn basis(b:osk::Invoke) -> py::Expression {
    match b.identifier.as_str() {
        "Cube" => method_call(name("geo"), "createNode", vec![string("box")]),
        _ => panic!()
    }
}

fn codegen_standard_picture(picture: osk::Picture) -> py::Statement {
    let expression = basis(picture.basis);
    assign(name(&picture.identifier), expression)
}
 
pub fn codegen_toplevel(tl: osk::TopLevel) -> py::Statement {
    match tl {
        osk::TopLevel::Film(f) => codegen_film(f),
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => codegen_standard_picture(p),
        osk::TopLevel::Skip => unreachable!(),
        osk::TopLevel::PythonCodeBlock(_) => unreachable!(),
        _ => py_print_stmt(vec![string("?")]),
    }
}

fn import(m:&str) -> py::Statement {
    py::Statement::Import( py::Import::Import { names: vec![ (vec![m.to_string()], None) ] })
}

pub fn preamble() -> String {
    format_module(&vec![
        import("hou"),
        assign(name("geo"),
            method_call(
                method_call(name("hou"), "node", vec![string("/obj")]),
            "createNode", vec![string("geo")]))
    ])
}

pub fn to_python_source(tl: osk::TopLevel) -> String {
    let stmts = vec![codegen_toplevel(tl)];
    format_module(&stmts)
}

pub fn print_python_ast(code:&str) {
    let ast = python_parser::file_input(python_parser::make_strspan(code)).unwrap().1;
    println!("{:#?}", ast)
}