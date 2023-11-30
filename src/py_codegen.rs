use lazy_static::lazy_static;
use pyo3::prelude::*;

lazy_static! {
    static ref AST_MODULE: Py<PyModule> =
        Python::with_gil(|py| { py.import("ast").unwrap().into() });
}

// https://docs.python.org/3/library/ast.html
macro_rules! ast {
    ($name:ident) => {
        Python::with_gil(|py| AST_MODULE.getattr(py, stringify!($name)).unwrap().call0(py)).unwrap()
    };
    ($name:ident, $ex:expr) => {
        Python::with_gil(|py| AST_MODULE.getattr(py, stringify!($name)).unwrap().call1(py, ($ex,))).unwrap()
    };
    ($name:ident, $($ex:expr),+) => {
        Python::with_gil(|py| AST_MODULE.getattr(py, stringify!($name)).unwrap().call1(py, ($($ex),+))).unwrap()
    };
}

macro_rules! py_const {
    ($v:literal) => {
        ast!(Constant, $v)
    };
}

macro_rules! py_ret {
    ($v:expr) => {
        ast!(Return, $v)
    };
}

macro_rules! py_name {
    ($v:expr) => {
        ast!(Name, $v)
    };
}

macro_rules! py_cmp {
    ($op:ident, $lhs:expr, $rhs:expr) => {
        ast!(Compare, $lhs, [ast!($op)], [$rhs])
    };
}

macro_rules! py_if {
    ($test:expr, $body:expr, $or_else:expr) => {
        ast!(If, $test, $body, $or_else)
    };
}

macro_rules! py_call {
    ($target:expr) => {
        ast!(Call, $target, Vec::<i32>::new(), Vec::<i32>::new())
    };
    ($target:expr, $positional:expr) => {
        ast!(Call, $target, $positional, Vec::<i32>::new())
    };
}

macro_rules! py_unary {
    ($op:ident, $target:expr) => {
        ast!(UnaryOp, ast!($op), $target)
    };
}

pub fn test_macros() {
    let test_call = py_call!(
        py_name!("if_you_can_see_this"),
        [py_const!(44), py_const!(true)]
    );
    let ast = py_if!(
        py_cmp!(NotEq, test_call, py_const!(97)),
        [py_ret!(py_const!("we are good"))],
        [py_ret!(py_unary!(Not, py_name!("good")))]
    );
    let code = unparse(&ast);
    println!("{}", code);
}

#[derive(Debug)]
pub struct ParseError {
    message: String,
    line: usize,
    offset: usize,
}

impl ParseError {
    fn from_err(e: PyErr) -> Self {
        Python::with_gil(|py| {
            let ex = e.value(py);
            let message = ex.getattr("msg").unwrap().extract().unwrap();
            let line = ex.getattr("lineno").unwrap().extract().unwrap();
            let offset = ex.getattr("offset").unwrap().extract().unwrap();
            Self {
                message,
                line,
                offset,
            }
        })
    }
}

pub fn parse(code: &str) -> Result<Py<PyAny>, ParseError> {
    Python::with_gil(|py| {
        let parse = AST_MODULE.getattr(py, "parse").unwrap();
        match parse.call1(py, (code,)) {
            Ok(result) => Ok(result),
            Err(e) => Err(ParseError::from_err(e)),
        }
    })
}

pub fn unparse(ast: &Py<PyAny>) -> String {
    Python::with_gil(|py| {
        let unparse = AST_MODULE.getattr(py, "unparse").unwrap();
        let result = unparse.call1(py, (ast,)).unwrap().to_string();
        result
    })
}
