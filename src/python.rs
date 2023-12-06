use pyo3::prelude::*;

lazy_static! {
    pub static ref AST_MODULE: Py<PyModule> =
        Python::with_gil(|py| { py.import("ast").unwrap().into() });
    pub static ref SYS_MODULE: Py<PyModule> =
        Python::with_gil(|py| { py.import("sys").unwrap().into() });
}

pub type AST = Py<PyAny>;

#[derive(Debug)]
pub struct Error {
    pub message: String,
    pub line: usize,
    pub offset: usize,
}

impl Error {
    fn from_py_err(e: PyErr) -> Self {
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

pub fn parse_exec(code: &str) -> Result<Py<PyAny>, Error> {
    Python::with_gil(|py| {
        let parse = AST_MODULE.getattr(py, "parse").unwrap();
        match parse.call1(py, (code,)) {
            Ok(result) => Ok(result),
            Err(e) => Err(Error::from_py_err(e)),
        }
    })
}

pub fn parse_eval(code: &str) -> Result<Py<PyAny>, Error> {
    Python::with_gil(|py| {
        let parse = AST_MODULE.getattr(py, "parse").unwrap();
        match parse.call1(py, (code, "<expr>", "eval")) {
            Ok(result) => {
                let body = result
                    .getattr(py, "body")
                    .expect("parsed value does not have body");
                Ok(body)
            }
            Err(e) => Err(Error::from_py_err(e)),
        }
    })
}

pub fn unparse(ast: &Py<PyAny>) -> String {
    Python::with_gil(|py| {
        let unparse = AST_MODULE.getattr(py, "unparse").unwrap();
        let fix_missing_locations = AST_MODULE.getattr(py, "fix_missing_locations").unwrap();
        let result = unparse
            .call1(py, (fix_missing_locations.call1(py, (ast,)).unwrap(),))
            .unwrap()
            .to_string();
        result
    })
}

pub fn version() -> String {
    Python::with_gil(|py| {
        SYS_MODULE.getattr(py, "version").unwrap().to_string()
    })
}
