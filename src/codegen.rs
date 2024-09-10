use crate::ast as osk;
use crate::python as py;
use pyo3::prelude::*;

// https://docs.python.org/3/library/ast.html
#[macro_export]
macro_rules! ast {
    ($name:ident) => {
        Python::with_gil(|py| $crate::python::AST_MODULE.getattr(py, stringify!($name)).unwrap().call0(py)).unwrap()
    };
    ($name:ident, $ex:expr) => {
        Python::with_gil(|py| $crate::python::AST_MODULE.getattr(py, stringify!($name)).unwrap().call1(py, ($ex,))).unwrap()
    };
    ($name:ident, $($ex:expr),+) => {
        Python::with_gil(|py| $crate::python::AST_MODULE.getattr(py, stringify!($name)).unwrap().call1(py, ($($ex),+))).unwrap()
    };
}

macro_rules! empty_list {
    () => {
        Vec::<i32>::new()
    };
}

macro_rules! module {
    ($body:expr) => {
        ast!(Module, $body, empty_list!())
    };
}

macro_rules! constant {
    ($v:expr) => {
        ast!(Constant, $v)
    };
    ($v:literal) => {
        ast!(Constant, $v)
    };
}

macro_rules! ret {
    ($v:expr) => {
        ast!(Return, $v)
    };
}

macro_rules! raise {
    ($e:expr) => {
        ast!(Raise, $e)
    };
}

macro_rules! name {
    ($v:expr) => {
        ast!(Name, $v)
    };
}

macro_rules! compare {
    ($op:ident, $lhs:expr, $rhs:expr) => {
        ast!(Compare, $lhs, [ast!($op)], [$rhs])
    };
}

macro_rules! if_stmt {
    ($test:expr, $body:expr, $or_else:expr) => {
        ast!(If, $test, $body, $or_else)
    };
}

macro_rules! with_stmt {
    ($items:expr, $body:expr) => {
        ast!(With, $items, $body)
    };
}

macro_rules! call {
    ($target:expr) => {
        ast!(Call, $target, empty_list!(), empty_list!())
    };
    ($target:expr, $positional:expr) => {
        ast!(Call, $target, $positional, empty_list!())
    };
}

macro_rules! call_kw {
    ($target:expr, $positional:expr, $kw:expr) => {
        ast!(Call, $target, $positional, $kw)
    };
}

macro_rules! unary_op {
    ($op:ident, $target:expr) => {
        ast!(UnaryOp, ast!($op), $target)
    };
}

macro_rules! bool_op {
    ($op:ident, $left:expr, $right:expr) => {
        ast!(BoolOp, ast!($op), [$left, $right])
    };
}

macro_rules! bin_op {
    ($op:ident, $left:expr, $right:expr) => {
        ast!(BinOp, $left, ast!($op), $right)
    };
}

macro_rules! keyword {
    ($arg:expr, $value:expr) => {
        ast!(keyword, $arg, $value)
    };
}

macro_rules! arg {
    ($name:expr) => {
        ast!(arg, $name)
    };
}

macro_rules! args {
    ($args:expr) => {
        ast!(
            arguments,
            empty_list!(), // posonlyargs
            $args,         // args
            empty_list!(), // vararg
            empty_list!(), // kwonlyargs
            empty_list!(), // kw_defaults
            empty_list!(), // kwarg
            empty_list!()  // defaults
        )
    };
}

macro_rules! args_defaults {
    ($args:expr, $defaults:expr) => {
        ast!(
            arguments,
            empty_list!(), // posonlyargs
            $args,         // args
            empty_list!(), // vararg
            empty_list!(), // kwonlyargs
            empty_list!(), // kw_defaults
            empty_list!(), // kwarg
            $defaults      // defaults
        )
    };
}

macro_rules! funcdef {
    ($name:expr, $args:expr, $body:expr) => {
        ast!(FunctionDef, $name, $args, $body, empty_list!())
    };
}

macro_rules! assign {
    ($target:expr, $value:expr) => {
        $crate::ast!(Assign, $target, $value)
    };
}

macro_rules! list {
    ($elts:expr) => {
        $crate::ast!(List, $elts)
    };
}

macro_rules! tuple {
    ($elts:expr) => {
        $crate::ast!(Tuple, $elts)
    };
}

macro_rules! attribute {
    ($value:expr, $attr:literal) => {
        ast!(Attribute, $value, $attr)
    };
}

macro_rules! for_loop {
    ($target:expr, $iter:expr, $body:expr) => {
        ast!(For, $target, $iter, $body, empty_list!())
    };
}

macro_rules! expr {
    ($e:expr) => {
        ast!(Expr, $e)
    };
}

static mut _IDENTIFIER_ID: u32 = 0;

fn fresh_name(s: &str) -> py::AST {
    unsafe {
        _IDENTIFIER_ID += 1;
        name!(format!("{}_{}", s, _IDENTIFIER_ID))
    }
}

fn codegen_film(film: &osk::Film) -> py::AST {
    call!(
        name!("osk_film"),
        [name!(&film.picture.identifier), film.frames.clone()]
    )
}

fn codegen_standard_picture_transforms(
    picture: &osk::Picture,
    xform_sets: &Vec<osk::TransformSet>,
    i: usize,
    parent_xform_name: py::AST,
) -> Vec<py::AST> {
    let xform_name = fresh_name("_xform");
    let basis_name = name!(picture.basis.identifier.clone());
    let num_pics_name = fresh_name("_num_pics");
    let xform_set = &xform_sets[xform_sets.len() - 1 - i];
    let mut loop_body = vec![
        // pct = nth / num_pics
        assign!(
            [name!(&xform_set.num_pics.pct_identifier)],
            bin_op!(
                Div,
                name!(&xform_set.num_pics.nth_identifier),
                // num_pics_value.clone()
                num_pics_name.clone()
            )
        ),
    ];
    if let Some(statement) = &xform_set.statement {
        loop_body.push(statement.clone());
    }

    let mut translates = vec![];
    let mut rotates = vec![];
    let mut scales = vec![];
    let mut dynamic_bindings = vec![call!(name!("__time__"), [name!("t")])];
    for transform in &xform_set.transforms {
        match transform {
            osk::Transform::Scale((x, y, z)) => {
                let scale_name = fresh_name("_scale");
                loop_body.push(assign!(
                    [scale_name.clone()],
                    tuple!(vec![x.clone(), y.clone(), z.clone()])
                ));
                dynamic_bindings.push(call!(
                    name!("__visible__"),
                    [bool_op!(
                        And,
                        attribute!(name!("__visible__"), "value"),
                        unary_op!(
                            Not,
                            call!(name!("osk_razor_thin"), vec![scale_name.clone()])
                        )
                    )]
                ));
                scales.push(scale_name)
            }
            osk::Transform::Translate((x, y, z)) => {
                translates.push(tuple!(vec![x.clone(), y.clone(), z.clone()]))
            }
            osk::Transform::Rotate((x, y, z)) => {
                rotates.push(tuple!(vec![x.clone(), y.clone(), z.clone()]))
            }
            osk::Transform::Color((h, s, v)) => dynamic_bindings.push(call!(
                name!("__material__"),
                [tuple!(vec![h.clone(), s.clone(), v.clone()])]
            )),
        }
    }

    loop_body.push(assign!(
        [xform_name.clone()],
        call!(
            attribute!(parent_xform_name.clone(), "add_child"),
            vec![call!(
                name!("Transform"),
                vec![
                    constant!(&picture.identifier),
                    list!(translates),
                    list!(rotates),
                    list!(scales),
                ]
            )]
        )
    ));

    if i < xform_sets.len() - 1 {
        loop_body.append(&mut codegen_standard_picture_transforms(
            picture,
            xform_sets,
            i + 1,
            xform_name,
        ))
    } else {
        let mut basis_args = vec![];
        let mut basis_kw_args = vec![];
        for p in &picture.basis.parameters {
            match p {
                osk::Parameter::Simple(v) => basis_args.push(v.clone()),
                osk::Parameter::KeyValue(k, v) => {
                    basis_kw_args.push(keyword!(k.clone(), v.clone()))
                }
            }
        }

        let mut basis_args_custom_primitive = vec![basis_name.clone()];
        basis_args_custom_primitive.append(&mut basis_args.clone());

        loop_body.push(with_stmt!(
            dynamic_bindings,
            [if_stmt!(
                call!(name!("osk_is_primitive"), [basis_name.clone()]),
                [expr!(call!(
                    attribute!(xform_name.clone(), "add_child"),
                    vec![call_kw!(
                        name!("Primitive"),
                        basis_args_custom_primitive,
                        basis_kw_args.clone()
                    )]
                ))],
                [expr!(call!(
                    attribute!(xform_name, "add_child"),
                    vec![call_kw!(basis_name, basis_args, basis_kw_args)]
                ))]
            )]
        ));
    }

    vec![
        assign!([num_pics_name.clone()], xform_set.num_pics.value.clone()),
        for_loop!(
            name!(&xform_set.num_pics.nth_identifier),
            call!(name!("range"), vec![num_pics_name.clone()]),
            loop_body
        ),
    ]
}

fn codegen_standard_picture(picture: &osk::Picture) -> py::AST {
    let root_name = fresh_name("_root");

    let mut body = vec![
        assign!([name!("pt")], attribute!(name!("__time__"), "value")),
        assign!([name!("t")], name!("pt")),
    ];

    body.push(assign!(
        [root_name.clone()],
        call!(name!("Transform"), [constant!(&picture.identifier)])
    ));

    let mut body_specific = match picture.operations {
        osk::Operations::TransformSet(ref xforms) => {
            codegen_standard_picture_transforms(&picture, xforms, 0, root_name.clone())
        }
        osk::Operations::Csg(_) => todo!(),
    };

    body.append(&mut body_specific);

    body.push(ret!(root_name));

    let mut parameters = vec![];
    for p in &picture.parameters {
        parameters.push(arg!(p.clone()));
    }

    funcdef!(&picture.identifier, args!(parameters), body)
}

fn codegen_picture_list(picture_list: &osk::PictureList) -> py::AST {
    let children: Vec<py::AST> = picture_list
        .invokes
        .iter()
        .map(|i| {
            let mut user_args: Vec<py::AST> = i
                .parameters
                .iter()
                .map(|p| match p {
                    osk::Parameter::Simple(v) => v.clone(),
                    osk::Parameter::KeyValue(k, v) => keyword!(k.clone(), v.clone()),
                })
                .collect();
            let mut args = vec![];
            args.append(&mut user_args);
            call!(name!(&i.identifier), args)
        })
        .collect();

    let mut none_body = vec![assign!(
        [name!("_root")],
        call!(
            name!("Transform"),
            vec![constant!(&picture_list.identifier)]
        )
    )];
    none_body.append(
        &mut children
            .iter()
            .map(|child| {
                expr!(call!(
                    attribute!(name!("_root"), "add_child"),
                    [child.clone()]
                ))
            })
            .collect(),
    );
    none_body.push(ret!(name!("_root")));

    let mut body = vec![];
    let mut i = children.len();
    for child in children.iter().rev() {
        body = vec![if_stmt!(
            compare!(Eq, name!("i"), constant!(i - 1)),
            vec![ret!(child)],
            body
        )];
        i = i - 1;
    }

    body = vec![
        if_stmt!(compare!(Is, name!("i"), name!("None")), none_body, body),
        raise!(call!(name!("IndexError"))),
    ];

    funcdef!(
        &picture_list.identifier,
        args_defaults!([arg!("i")], [name!("None")]),
        body
    )
}

pub fn codegen_toplevel(tl: &osk::TopLevel) -> py::AST {
    let module_body = match tl {
        osk::TopLevel::Film(f) => vec![codegen_film(f)],
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Function(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Selection(p)) => vec![codegen_picture_list(p)],
        osk::TopLevel::PythonCodeBlock(b) => vec![b.lines.clone()],
        osk::TopLevel::Skip => vec![],
    };
    module!(module_body)
}

pub fn preamble() -> &'static str {
    include_str!("preamble.py")
}

pub fn to_python_source(tl: &osk::TopLevel) -> String {
    py::unparse(&codegen_toplevel(tl))
}
