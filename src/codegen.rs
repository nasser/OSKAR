use crate::ast as osk;
use python_parser::ast as py;
use python_parser::visitors::printer::format_module;

fn _box<T>(t: T) -> Box<T> {
    Box::new(t)
}

fn assign(lhs: py::Expression, rhs: py::Expression) -> py::Statement {
    py::Statement::Assignment(vec![lhs], vec![vec![rhs]])
}

fn assign_multiple(lhs: Vec<py::Expression>, rhs: py::Expression) -> py::Statement {
    py::Statement::Assignment(lhs, vec![vec![rhs]])
}

fn py_return(e: py::Expression) -> py::Statement {
    py::Statement::Return(vec![e])
}

fn name(s: &str) -> py::Expression {
    py::Expression::Name(s.to_string())
}

static mut _IDENTIFIER_ID: u32 = 0;

fn fresh_name(s: &str) -> py::Expression {
    unsafe {
        _IDENTIFIER_ID += 1;
        name(&format!("{}_{}", s, _IDENTIFIER_ID))
    }
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

fn keyword(k: String, v: py::Expression) -> py::Argument {
    py::Argument::Keyword(k, v)
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
fn bop_eq(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::Eq, _box(lhs), _box(rhs))
}

fn bop_and(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::And, _box(lhs), _box(rhs))
}

fn uop_not(e: py::Expression) -> py::Expression {
    py::Expression::Uop(py::Uop::Not, _box(e))
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

fn codegen_film(film: &osk::Film) -> py::Statement {
    statement(fcall_positional(
        name("osk_film"),
        vec![name(&film.picture.identifier), film.frames.clone().unwrap()],
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
    i: usize,
    scope: (py::Expression, py::Expression, py::Expression),
) -> py::Statement {
    let (parent_material_name, parent_visible_name, parent_xform_name) = scope;
    let material_name = fresh_name("material");
    let visible_name = fresh_name("visible");
    let xform_name = fresh_name("xform");
    let context_name = fresh_name("context");
    let xform_set = &xform_sets[xform_sets.len() - 1 - i];
    let num_pics_value = xform_set.num_pics.value.as_ref().unwrap();
    let mut loop_body = vec![
        // pct = nth / num_pics
        assign(
            name(&xform_set.num_pics.pct_identifier),
            py::Expression::Bop(
                py::Bop::Div,
                _box(name(&xform_set.num_pics.nth_identifier)),
                _box(num_pics_value.clone()),
            ),
        ),
    ];
    if let Some(Ok(statements)) = &xform_set.statements {
        loop_body.append(&mut statements.clone());
    }

    loop_body.push(assign(material_name.clone(), parent_material_name.clone()));
    loop_body.push(assign(visible_name.clone(), parent_visible_name.clone()));

    let mut translates = vec![];
    let mut rotates = vec![];
    let mut scales = vec![];
    for transform in &xform_set.transforms {
        match transform {
            osk::Transform::Scale((x, y, z)) => {
                let scale_name = fresh_name("scale");
                loop_body.push(assign(
                    scale_name.clone(),
                    tuple_literal(vec![
                        x.clone().unwrap(),
                        y.clone().unwrap(),
                        z.clone().unwrap(),
                    ]),
                ));
                loop_body.push(assign(
                    visible_name.clone(),
                    bop_and(
                        visible_name.clone(),
                        uop_not(fcall_positional(
                            name("osk_razor_thin"),
                            vec![scale_name.clone()],
                        )),
                    ),
                ));
                scales.push(scale_name)
            }
            osk::Transform::Translate((x, y, z)) => translates.push(tuple_literal(vec![
                x.clone().unwrap(),
                y.clone().unwrap(),
                z.clone().unwrap(),
            ])),
            osk::Transform::Rotate((x, y, z)) => rotates.push(tuple_literal(vec![
                x.clone().unwrap(),
                y.clone().unwrap(),
                z.clone().unwrap(),
            ])),
            osk::Transform::Color((h, s, v)) => loop_body.push(assign(
                material_name.clone(),
                tuple_literal(vec![
                    h.clone().unwrap(),
                    s.clone().unwrap(),
                    v.clone().unwrap(),
                ]),
            )),
        }
    }

    loop_body.push(assign(
        xform_name.clone(),
        fcall_positional(
            attribute(parent_xform_name.clone(), "add_child"),
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
            i + 1,
            (material_name, visible_name, xform_name),
        ))
    } else {
        let mut basis_args = vec![positional(name("t")), positional(context_name.clone())];
        for p in &picture.basis.parameters {
            match p {
                osk::Parameter::Simple(v) => basis_args.push(positional(v.clone().unwrap())),
                osk::Parameter::KeyValue(k, v) => {
                    basis_args.push(keyword(k.clone(), v.clone().unwrap()))
                }
            }
        }

        loop_body.push(assign(
            context_name.clone(),
            tuple_literal(vec![material_name.clone(), visible_name.clone()]),
        ));

        loop_body.push(statement(fcall_positional(
            attribute(xform_name, "add_child"),
            vec![fcall(name(&picture.basis.identifier), basis_args)],
        )));
    }

    for_loop(
        name(&xform_set.num_pics.nth_identifier),
        fcall_positional(
            name("range"),
            vec![xform_set.num_pics.value.clone().unwrap()],
        ),
        loop_body,
    )
}

fn codegen_standard_picture(picture: &osk::Picture) -> py::Statement {
    let material_name = fresh_name("material");
    let visible_name = fresh_name("visible");
    let root_name = fresh_name("root");

    let mut body = vec![
        assign(name("t"), name("pt")),
        assign_multiple(
            vec![material_name.clone(), visible_name.clone()],
            name("_context"),
        ),
    ];

    body.push(assign(
        root_name.clone(),
        fcall_positional(name("Transform"), vec![string(&picture.identifier)]),
    ));

    let body_specific = match picture.operations {
        osk::Operations::TransformSet(ref xforms) => codegen_standard_picture_transforms(
            &picture,
            xforms,
            0,
            (material_name, visible_name, root_name.clone()),
        ),
        osk::Operations::Csg(_) => todo!(),
    };

    body.push(body_specific);

    body.push(py::Statement::Return(vec![root_name]));

    let mut parameters = vec!["pt".to_owned(), "_context".to_owned()];
    for p in &picture.parameters {
        parameters.push(p.clone());
    }

    funcdef_statement(funcdef(&picture.identifier, parameters, body))
}

fn codegen_picture_list(picture_list: &osk::PictureList) -> Vec<py::Statement> {
    let children: Vec<py::Expression> = picture_list
        .invokes
        .iter()
        .map(|i| {
            let mut user_args: Vec<py::Argument> = i
                .parameters
                .iter()
                .map(|p| match p {
                    osk::Parameter::Simple(v) => positional(v.clone().unwrap()),
                    osk::Parameter::KeyValue(k, v) => keyword(k.clone(), v.clone().unwrap()),
                })
                .collect();
            let mut args = vec![positional(name("pt")), positional(name("_context"))];
            args.append(&mut user_args);
            fcall(name(&i.identifier), args)
        })
        .collect();

    let mut none_body = vec![assign(
        name("_root"),
        fcall_positional(name("Transform"), vec![string(&picture_list.identifier)]),
    )];
    none_body.append(
        &mut children
            .iter()
            .map(|child| {
                statement(fcall_positional(
                    attribute(name("_root"), "add_child"),
                    vec![child.clone()],
                ))
            })
            .collect(),
    );
    none_body.push(py_return(name("_root")));

    let mut branches = vec![(bop_is(name("i"), py::Expression::None), none_body)];
    let mut i = 0;
    for child in children {
        branches.push((
            bop_eq(name("i"), py::Expression::Int(i)),
            vec![py_return(child)],
        ));
        i = i + 1;
    }

    let body = vec![if_then(branches, None)];

    vec![funcdef_statement(funcdef_defaults(
        &picture_list.identifier,
        vec!["pt".to_owned(), "_context".to_owned(), "i".to_owned()],
        vec![None, None, Some(py::Expression::None)],
        body,
    ))]
}

pub fn codegen_toplevel(tl: &osk::TopLevel) -> Vec<py::Statement> {
    match tl {
        osk::TopLevel::Film(f) => vec![codegen_film(f)],
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Function(p)) => {
            vec![codegen_standard_picture(p)]
        }
        osk::TopLevel::Definition(osk::Definition::Selection(p)) => codegen_picture_list(p),
        osk::TopLevel::PythonCodeBlock(b) => b.lines.clone().unwrap(),
        osk::TopLevel::Skip => vec![],
    }
}

pub fn preamble() -> &'static str {
    include_str!("preamble.py")
}

pub fn to_python_source(tl: &osk::TopLevel) -> String {
    let stmts = codegen_toplevel(tl);
    format_module(&stmts)
}

pub fn print_python_ast(code: &str) {
    let ast = python_parser::file_input(python_parser::make_strspan(code))
        .unwrap()
        .1;
    println!("{:#?}", ast)
}
