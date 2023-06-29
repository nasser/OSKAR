use crate::ast as osk;
use python_parser::ast as py;
use python_parser::visitors::printer::format_module;

fn to_python_expression(code: &str) -> py::Expression {
    match osk::to_python_statements(code) {
        stmnts if stmnts.len() == 1 => match &stmnts[0] {
            py::Statement::Assignment(lhs, _) if lhs.len() == 1 => lhs[0].clone(),
            _ => panic!("unexpected python AST in {}", code),
        },
        _ => panic!("unexpected python AST in {}", code),
    }
}

fn _box<T>(t: T) -> Box<T> {
    Box::new(t)
}

fn assign(lhs: py::Expression, rhs: py::Expression) -> py::Statement {
    py::Statement::Assignment(vec![lhs], vec![vec![rhs]])
}

fn py_return(e: py::Expression) -> py::Statement {
    py::Statement::Return(vec![e])
}

fn name(s: &str) -> py::Expression {
    py::Expression::Name(s.to_string())
}

fn string(s: &str) -> py::Expression {
    py::Expression::String(vec![py::PyString {
        prefix: "".to_string(),
        content: s.to_string(),
    }])
}

fn if_then(
    branches: Vec<(py::Expression, Vec<py::Statement>)>,
    else_branch: Option<Vec<py::Statement>>,
) -> py::Statement {
    py::Statement::Compound(_box(py::CompoundStatement::If(branches, else_branch)))
}

fn fcall_positional(target: py::Expression, arguments: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(target),
        arguments
            .into_iter()
            .map(py::Argument::Positional)
            .collect(),
    )
}

fn fcall(target: py::Expression, arguments: Vec<py::Argument>) -> py::Expression {
    py::Expression::Call(_box(target), arguments)
}

fn positional(arg: py::Expression) -> py::Argument {
    py::Argument::Positional(arg)
}

fn starargs(arg: py::Expression) -> py::Argument {
    py::Argument::Starargs(arg)
}

fn attribute(x: py::Expression, name: &str) -> py::Expression {
    py::Expression::Attribute(_box(x), name.to_string())
}

fn bop_is(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::Is, _box(lhs), _box(rhs))
}

fn statement(ex: py::Expression) -> py::Statement {
    py::Statement::Expressions(vec![ex])
}

fn typed_args_list(names: Vec<String>) -> py::TypedArgsList {
    let args = names.iter().map(|n| (n.to_string(), None, None)).collect();
    py::TypedArgsList {
        args,
        posonly_args: vec![],
        star_args: py::StarParams::No,
        keyword_args: vec![],
        star_kwargs: None,
    }
}

fn typed_args_list_defaults(
    names: Vec<String>,
    defaults: Vec<Option<py::Expression>>,
) -> py::TypedArgsList {
    let args = names
        .iter()
        .enumerate()
        .map(|(i, n)| (n.to_string(), None, defaults[i].clone()))
        .collect();
    py::TypedArgsList {
        args,
        posonly_args: vec![],
        star_args: py::StarParams::No,
        keyword_args: vec![],
        star_kwargs: None,
    }
}

fn funcdef(name: &str, params: Vec<String>, code: Vec<py::Statement>) -> py::Funcdef {
    let name = name.to_string();
    let r#async = false;
    let decorators = vec![];
    let parameters = typed_args_list(params);
    let return_type = None;

    py::Funcdef {
        r#async,
        decorators,
        name,
        return_type,
        code,
        parameters,
    }
}

fn funcdef_defaults(
    name: &str,
    params: Vec<String>,
    defaults: Vec<Option<py::Expression>>,
    code: Vec<py::Statement>,
) -> py::Funcdef {
    let name = name.to_string();
    let r#async = false;
    let decorators = vec![];
    let parameters = typed_args_list_defaults(params, defaults);
    let return_type = None;

    py::Funcdef {
        r#async,
        decorators,
        name,
        return_type,
        code,
        parameters,
    }
}

fn funcdef_statement(f: py::Funcdef) -> py::Statement {
    py::Statement::Compound(_box(py::CompoundStatement::Funcdef(f)))
}

fn list_literal(exprs: Vec<py::Expression>) -> py::Expression {
    py::Expression::ListLiteral(
        exprs
            .iter()
            .map(|e| py::SetItem::Unique(e.clone()))
            .collect(),
    )
}

fn tuple_literal(exprs: Vec<py::Expression>) -> py::Expression {
    py::Expression::TupleLiteral(
        exprs
            .iter()
            .map(|e| py::SetItem::Unique(e.clone()))
            .collect(),
    )
}

fn subscript(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Subscript(_box(lhs), vec![py::Subscript::Simple(rhs)])
}

fn codegen_film(film: osk::Film) -> py::Statement {
    statement(fcall_positional(
        name("osk_film"),
        vec![
            name(&film.picture.identifier),
            to_python_expression(film.frames.as_str()),
        ],
    ))
}

fn for_loop(
    item: py::Expression,
    iterator: py::Expression,
    for_block: Vec<py::Statement>,
) -> py::Statement {
    py::Statement::Compound(_box(py::CompoundStatement::For {
        r#async: false,
        item: vec![item],
        iterator: vec![iterator],
        for_block,
        else_block: None,
    }))
}

fn codegen_standard_picture_transforms(
    picture: &osk::Picture,
    xform_sets: &Vec<osk::TransformSet>,
    root: String,
    i: usize,
) -> py::Statement {
    let xform_set = &xform_sets[xform_sets.len() - 1 - i];
    let xform_name = format!("_xform_{}", i);
    let mut loop_body = vec![
        // pct = nth / num_pics
        assign(
            name(&xform_set.num_pics.pct_identifier),
            py::Expression::Bop(
                py::Bop::Div,
                _box(name(&xform_set.num_pics.nth_identifier)),
                _box(to_python_expression(&xform_set.num_pics.value)),
            ),
        ),
    ];
    // a = b # (user code)
    if let Some(ref e) = xform_set.top_level_expression {
        loop_body.append(&mut e.statements.clone())
    }
    let mut translates = vec![];
    let mut rotates = vec![];
    let mut scales = vec![];
    for transform in &xform_set.transforms {
        match transform {
            osk::Transform::Scale(x, y, z) => scales.push(tuple_literal(vec![
                to_python_expression(x),
                to_python_expression(y),
                to_python_expression(z),
            ])),
            osk::Transform::Translate(x, y, z) => translates.push(tuple_literal(vec![
                to_python_expression(x),
                to_python_expression(y),
                to_python_expression(z),
            ])),
            osk::Transform::Rotate(x, y, z) => rotates.push(tuple_literal(vec![
                to_python_expression(x),
                to_python_expression(y),
                to_python_expression(z),
            ])),
            osk::Transform::Color(r, g, b) => todo!(),
        }
    }

    loop_body.push(assign(
        name(&xform_name),
        fcall_positional(
            attribute(name(&root), "add_child"),
            vec![fcall_positional(
                name("Transform"),
                vec![
                    string(&picture.identifier),
                    list_literal(translates),
                    list_literal(rotates),
                    list_literal(scales),
                ],
            )],
        ),
    ));

    if i < xform_sets.len() - 1 {
        loop_body.push(codegen_standard_picture_transforms(
            picture,
            xform_sets,
            xform_name,
            i + 1,
        ))
    } else {
        let mut basis_args = vec![name("t")];
        for p in &picture.basis.parameters {
            basis_args.push(to_python_expression(p))
        }

        loop_body.push(statement(fcall_positional(
            attribute(name(&xform_name), "add_child"),
            vec![fcall_positional(
                name(&picture.basis.identifier),
                basis_args,
            )],
        )));
    }

    for_loop(
        name(&xform_set.num_pics.nth_identifier),
        fcall_positional(
            name("range"),
            vec![to_python_expression(&xform_set.num_pics.value)],
        ),
        loop_body,
    )
}

fn codegen_standard_picture(picture: osk::Picture) -> py::Statement {
    let mut body = vec![assign(name("t"), name("pt"))];

    body.push(assign(name("_root"), fcall_positional(name("Transform"), vec![string(&picture.identifier)])));

    let body_specific = match picture.operations {
        osk::Operations::TransformSet(ref xforms) => {
            codegen_standard_picture_transforms(&picture, xforms, "_root".to_owned(), 0)
        }
        osk::Operations::Csg(_) => todo!(),
    };

    body.push(body_specific);

    body.push(py::Statement::Return(vec![name("_root")]));

    let mut funcdef_parameters = vec!["pt".to_owned()];
    for p in picture.parameters {
        funcdef_parameters.push(p)
    }

    funcdef_statement(funcdef(&picture.identifier, funcdef_parameters, body))
}

fn codegen_picture_list(picture_list: osk::PictureList) -> Vec<py::Statement> {
    let mut then_body = vec![assign(name("_root"), fcall_positional(name("Transform"), vec![string(&picture_list.identifier)]))];
    then_body.append(
        &mut picture_list
            .invokes
            .iter()
            .map(|i| {
                let mut user_args: Vec<py::Expression> =
                    i.parameters.iter().map(|p| name(&p)).collect();
                let mut args = vec![name("pt")];
                args.append(&mut user_args);
                statement(fcall_positional(
                    attribute(name("_root"), "add_child"),
                    vec![fcall_positional(name(&i.identifier), args)],
                ))
            })
            .collect(),
    );
    then_body.push(py_return(name("_root")));

    let body = vec![if_then(
        vec![(bop_is(name("i"), py::Expression::None), then_body)],
        Some(vec![
            assign(
                name("user_args"),
                list_literal(
                    picture_list
                        .invokes
                        .iter()
                        .map(|i| list_literal(i.parameters.iter().map(|p| name(&p)).collect()))
                        .collect(),
                ),
            ),
            py_return(fcall(
                subscript(
                    list_literal(
                        picture_list
                            .invokes
                            .iter()
                            .map(|i| name(&i.identifier))
                            .collect(),
                    ),
                    name("i"),
                ),
                vec![
                    positional(name("pt")),
                    starargs(subscript(name("user_args"), name("i"))),
                ],
            )),
        ]),
    )];
    vec![funcdef_statement(funcdef_defaults(
        &picture_list.identifier,
        vec!["pt".to_owned(), "i".to_owned()],
        vec![None, Some(py::Expression::None)],
        body,
    ))]
}

pub fn codegen_toplevel(tl: osk::TopLevel) -> Vec<py::Statement> {
    match tl {
        osk::TopLevel::Film(f) => vec![codegen_film(f)],
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Function(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Selection(p)) => codegen_picture_list(p),
        osk::TopLevel::Skip => unreachable!(),
        osk::TopLevel::PythonCodeBlock(_) => unreachable!(),
    }
}

pub fn preamble() -> &'static str {
    include_str!("preamble.py")
}

pub fn to_python_source(tl: osk::TopLevel) -> String {
    let stmts = codegen_toplevel(tl);
    format_module(&stmts)
}

pub fn print_python_ast(code: &str) {
    let ast = python_parser::file_input(python_parser::make_strspan(code))
        .unwrap()
        .1;
    println!("{:#?}", ast)
}
