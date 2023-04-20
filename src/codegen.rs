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

fn tuple(exprs: Vec<py::Expression>) -> py::Expression {
    py::Expression::TupleLiteral(
        exprs
            .iter()
            .map(|e| py::SetItem::Unique(e.clone()))
            .collect(),
    )
}

fn name(s: &str) -> py::Expression {
    py::Expression::Name(s.to_string())
}

fn integer(i: u64) -> py::Expression {
    py::Expression::Int(i)
}

fn string(s: &str) -> py::Expression {
    py::Expression::String(vec![py::PyString {
        prefix: "".to_string(),
        content: s.to_string(),
    }])
}

fn py_return(expression: py::Expression) -> py::Statement {
    py::Statement::Return(vec![expression])
}

fn mcall(target: py::Expression, name: &str, arguments: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(py::Expression::Attribute(_box(target), name.to_string())),
        arguments
            .into_iter()
            .map(py::Argument::Positional)
            .collect(),
    )
}

fn fcall(target: py::Expression, arguments: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(target),
        arguments
            .into_iter()
            .map(py::Argument::Positional)
            .collect(),
    )
}

fn attribute(x: py::Expression, name: &str) -> py::Expression {
    py::Expression::Attribute(_box(x), name.to_string())
}

fn bop_or(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::Or, _box(lhs), _box(rhs))
}

fn bop_mod(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::Mod, _box(lhs), _box(rhs))
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

fn untyped_args_list(names: Vec<&str>) -> py::UntypedArgsList {
    let args = names.iter().map(|n| (n.to_string(), None)).collect();
    py::UntypedArgsList {
        args,
        posonly_args: vec![],
        star_args: py::StarParams::No,
        keyword_args: vec![],
        star_kwargs: None,
    }
}

fn lambda(params: Vec<&str>, body: py::Expression) -> py::Expression {
    py::Expression::Lambdef(untyped_args_list(params), _box(body))
}

fn ternary(
    then: py::Expression,
    condition: py::Expression,
    else_: py::Expression,
) -> py::Expression {
    py::Expression::Ternary(_box(then), _box(condition), _box(else_))
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

fn subscript(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Subscript(_box(lhs), vec![py::Subscript::Simple(rhs)])
}

fn hou_make_visible(target: py::Expression) -> py::Expression {
    mcall(target, "setDisplayFlag", vec![py::Expression::Int(1)])
}

fn codegen_film(film: osk::Film) -> py::Statement {
    statement(fcall(
        name("osk_film"),
        vec![
            name(&film.picture.identifier),
            to_python_expression(film.frames.as_str()),
        ],
    ))
}

fn iter_begin_name(picture_name: &str, i: usize) -> py::Expression {
    name(&format!("{}_{}_iter_begin", picture_name, i))
}

fn iter_end_name(picture_name: &str, i: usize) -> py::Expression {
    name(&format!("{}_{}_iter_end", picture_name, i))
}

fn iter_meta_name(picture_name: &str, i: usize) -> py::Expression {
    name(&format!("{}_{}_iter_meta_path", picture_name, i))
}

fn time_func_name_str(picture_name: &str, i: usize) -> String {
    format!("{}_{}_0_local_time", picture_name, i)
}

fn time_func_name(picture_name: &str, i: usize) -> py::Expression {
    name(&time_func_name_str(picture_name, i))
}

fn env_func_name_str(name: &str, i: usize, j: usize) -> String {
    format!("{}_{}_{}", name, i, j)
}

fn basis_name(picture_name: &str, i: usize) -> py::Expression {
    name(&format!("{}_{}_basis", picture_name, i))
}

fn out_name(picture_name: &str, i: usize) -> py::Expression {
    name(&format!("{}_{}_out", picture_name, i))
}

fn xform_set_node_name(picture_name: &str, xform_num: usize, node_num: usize) -> py::Expression {
    name(&format!("{}_{}_{}", picture_name, xform_num, node_num))
}

fn iteration_networks(
    picture: &osk::Picture,
    transforms: &[osk::TransformSet],
) -> Vec<py::Statement> {
    let mut ret = vec![];
    transforms.iter().enumerate().for_each(|(i, t)| {
        if t.iteration {
            let iter_name = format!("{}_{}_iteration", picture.identifier, i);
            let iter_value = to_python_expression(&t.num_pics.value);
            ret.push(assign(
                tuple(vec![
                    iter_begin_name(&picture.identifier, i),
                    iter_end_name(&picture.identifier, i),
                    iter_meta_name(&picture.identifier, i),
                ]),
                fcall(
                    name("iteration_network"),
                    vec![name("root"), string(&iter_name), iter_value],
                ),
            ))
        }
    });
    ret
}

fn iteration_thunks(picture: &osk::Picture, xforms: &[osk::TransformSet]) -> Vec<py::Statement> {
    let mut ret = vec![];
    // TODO this logic is duplicated in env_func
    xforms.iter().enumerate().rev().for_each(|(j, t)| {
        let nth_identifier = name(&t.num_pics.nth_identifier);
        let value = if t.iteration {
            fcall(
                name("Thunk"),
                vec![lambda(vec![], get_iteration_index(picture, j))],
            )
        } else {
            integer(0)
        };
        ret.push(assign(nth_identifier, value));
        let pct_identifier = name(&t.num_pics.pct_identifier);
        let value = if t.iteration {
            fcall(
                name("Thunk"),
                vec![lambda(vec![], get_iteration_value(picture, j))],
            )
        } else {
            integer(0)
        };
        ret.push(assign(pct_identifier.clone(), value));
        ret.push(assign(name("i"), pct_identifier));
    });
    ret
}

fn get_iteration_value(picture: &osk::Picture, i: usize) -> py::Expression {
    fcall(
        name("iteration_value"),
        vec![iter_meta_name(&picture.identifier, i)],
    )
}

fn get_iteration_index(picture: &osk::Picture, i: usize) -> py::Expression {
    fcall(
        name("iteration_index"),
        vec![iter_meta_name(&picture.identifier, i)],
    )
}

fn env_func(
    picture: &osk::Picture,
    xforms: &[osk::TransformSet],
    i: usize,
    j: usize,
) -> py::Funcdef {
    let pt = if i == xforms.len() - 1 {
        name("_pt")
    } else {
        time_func_name(&picture.identifier, i + 1)
    };
    let mut body = vec![
        // time variables
        assign(name("pt"), fcall(pt, vec![])),
        assign(name("t"), name("pt")),
    ];
    for parameter in &picture.parameters {
        // parameter variables
        let p = name(&parameter);
        let _p = name(&format!("_{}", parameter));
        body.push(assign(
            p,
            ternary(
                fcall(_p.clone(), vec![]),
                fcall(name("isinstance"), vec![_p.clone(), name("Thunk")]),
                _p,
            ),
        ))
    }
    xforms.iter().enumerate().rev().for_each(|(j, t)| {
        // TODO this logic is duplicated in iteration_thunks
        // iteration variables
        if j >= i {
            let nth_identifier = name(&t.num_pics.nth_identifier);
            let value = if t.iteration {
                get_iteration_index(picture, j)
            } else {
                integer(0)
            };
            body.push(assign(nth_identifier, value));
            let pct_identifier = name(&t.num_pics.pct_identifier);
            let value = if t.iteration {
                get_iteration_value(picture, j)
            } else {
                integer(0)
            };
            body.push(assign(pct_identifier.clone(), value));
            body.push(assign(name("i"), pct_identifier));
        }
    });

    if let Some(e) = &xforms[i].top_level_expression {
        body.append(&mut e.statements.to_owned());
    };
    funcdef(&env_func_name_str(&picture.identifier, i, j), vec![], body)
}

fn time_func_and_thunk(stub: &py::Funcdef) -> Vec<py::Statement> {
    let mut code = stub.code.clone();
    // TODO time function name is duplicated
    let func_name = format!("{}_local_time", stub.name);
    code.push(py_return(name("t")));
    let time_func = py::Funcdef {
        code,
        name: func_name.clone(),
        ..stub.clone()
    };

    vec![
        funcdef_statement(time_func),
        assign(name("t"), fcall(name("Thunk"), vec![name(&func_name)])),
    ]
}

fn xform_code_thunks(
    stub: &py::Funcdef,
    statements: &osk::TransformSetStatements,
) -> Vec<py::Statement> {
    statements
        .names
        .iter()
        .flat_map(|n| {
            let mut code = stub.code.clone();
            let func_name = format!("{}_parameter_{}", stub.name, n);
            code.push(py_return(name(n)));
            let time_func = py::Funcdef {
                code,
                name: func_name.to_owned(),
                ..stub.clone()
            };

            vec![
                funcdef_statement(time_func),
                assign(name(n), fcall(name("Thunk"), vec![name(&func_name)])),
            ]
        })
        .collect()
}

fn basis_value(picture: &osk::Picture, i: usize) -> py::Statement {
    // TODO time function name is duplicated
    let mut basis_invocation_parameters =
        vec![name("root"), time_func_name(&picture.identifier, i)];
    picture
        .basis
        .parameters
        .iter()
        .for_each(|p| basis_invocation_parameters.push(name(&p)));
    let basis_value = if i == 0 {
        fcall(name(&picture.basis.identifier), basis_invocation_parameters)
    } else {
        out_name(&picture.identifier, i - 1)
    };
    assign(basis_name(&picture.identifier, i), basis_value)
}

fn parm_set(node: &py::Expression, parm_name: &str, value: py::Expression) -> py::Statement {
    statement(mcall(
        mcall(node.clone(), "parm", vec![string(parm_name)]),
        "set",
        vec![value],
    ))
}

fn expression_function(
    parm_name: &str,
    expression: &str,
    stub: &py::Funcdef,
) -> (String, py::Statement) {
    let mut code = stub.code.clone();
    let func_name = format!("{}_parm_{}", stub.name, parm_name);
    code.push(py_return(to_python_expression(expression)));
    let parm_func = py::Funcdef {
        code,
        name: func_name.clone(),
        ..stub.clone()
    };
    (func_name, funcdef_statement(parm_func))
}

fn parm_set_expression(
    node: &py::Expression,
    parm_name: &str,
    expression: &str,
    stub: &py::Funcdef,
) -> Vec<py::Statement> {
    let (func_name, func_def) = expression_function(parm_name, expression, stub);
    let hou_expr_language_python = attribute(attribute(name("hou"), "exprLanguage"), "Python");
    let parm_expr_string = bop_mod(
        string("%s()"),
        fcall(name("export_function"), vec![name(&func_name)]),
    );
    vec![
        func_def,
        statement(mcall(
            mcall(node.clone(), "parm", vec![string(parm_name)]),
            "setExpression",
            vec![parm_expr_string, hou_expr_language_python],
        )),
    ]
}

fn get_number_literal(s: &str) -> Option<py::Expression> {
    let expr = to_python_expression(s);
    match to_python_expression(s) {
        py::Expression::Int(_) => Some(expr),
        py::Expression::Float(_) => Some(expr),
        py::Expression::Uop(py::Uop::Minus, boxed) => match *boxed {
            py::Expression::Int(_) => Some(expr),
            py::Expression::Float(_) => Some(expr),
            _ => None,
        },
        _ => None,
    }
}

fn set_xform_parm(
    var: &py::Expression,
    parm: &str,
    value: &String,
    stub: &py::Funcdef,
) -> Vec<py::Statement> {
    match get_number_literal(&value) {
        Some(expr) => vec![parm_set(var, parm, expr)],
        None => parm_set_expression(var, parm, &value, stub),
    }
}

fn set_name(target: py::Expression, name_argument: &str) -> py::Expression {
    mcall(
        target,
        "setName",
        vec![fcall(name("unique"), vec![string(name_argument)])],
    )
}

static COLOR_NODE_CODE : &str = "import colorsys
def color_attribute(geo):
    return geo.findPointAttrib(\"Cd\") or geo.addAttrib(hou.attribType.Point, \"Cd\", (0.0, 0.0, 0.0))
geo = hou.pwd().geometry()
attr = color_attribute(geo)
f = hou.expressionGlobals()['%s']
for point in geo.points():
    point.setAttribValue(attr, colorsys.hsv_to_rgb(*f()))";

fn make_transform_node(
    root: py::Expression,
    picture: &osk::Picture,
    xform: &osk::Transform,
    stub: &py::Funcdef,
    set_index: usize,
    xform_index: usize,
) -> Vec<py::Statement> {
    let mut ret = vec![];
    let var = name(&format!(
        "{}_{}_{}",
        picture.identifier, set_index, xform_index
    ));

    let node_type = match xform {
        osk::Transform::Color(_, _, _) => "python",
        _ => "xform",
    };
    ret.push(assign(
        var.clone(),
        mcall(root, "createNode", vec![string(node_type)]),
    ));

    match xform {
        osk::Transform::Translate(x, y, z) => {
            let name = &format!(
                "{}_{}_{}_translate",
                picture.identifier, set_index, xform_index
            );
            ret.append(&mut set_xform_parm(&var, "tx", x, &stub));
            ret.append(&mut set_xform_parm(&var, "ty", y, &stub));
            ret.append(&mut set_xform_parm(&var, "tz", z, &stub));
            ret.push(statement(set_name(var, name)));
        }
        osk::Transform::Rotate(x, y, z) => {
            let name = &format!(
                "{}_{}_{}_rotate",
                picture.identifier, set_index, xform_index
            );
            ret.append(&mut set_xform_parm(&var, "rx", x, &stub));
            ret.append(&mut set_xform_parm(&var, "ry", y, &stub));
            ret.append(&mut set_xform_parm(&var, "rz", z, &stub));
            ret.push(statement(set_name(var, name)));
        }
        osk::Transform::Scale(x, y, z) => {
            let name = &format!("{}_{}_{}_scale", picture.identifier, set_index, xform_index);
            ret.append(&mut set_xform_parm(&var, "sx", x, &stub));
            ret.append(&mut set_xform_parm(&var, "sy", y, &stub));
            ret.append(&mut set_xform_parm(&var, "sz", z, &stub));
            ret.push(statement(set_name(var, name)));
        }
        osk::Transform::Color(h, s, v) => {
            let node_name = &format!("{}_{}_{}_color", picture.identifier, set_index, xform_index);
            let code = COLOR_NODE_CODE;
            let (func_name, func_def) =
                expression_function("color", &format!("(({}),({}),({}))", h, s, v), &stub);
            ret.push(func_def);
            ret.push(parm_set(
                &var,
                "python",
                bop_mod(
                    string(&code),
                    fcall(name("export_function"), vec![name(&func_name)]),
                ),
            ));
            ret.push(statement(set_name(var, node_name)));
        }
    };
    ret
}

fn transform_set_nodes(
    picture: &osk::Picture,
    xform_sets: &[osk::TransformSet],
    xform_set: &osk::TransformSet,
    i: usize,
) -> Vec<py::Statement> {
    let mut ret = vec![];
    xform_set
        .transforms
        .iter()
        .enumerate()
        .for_each(|(j, xform)| {
            let stub = env_func(&picture, xform_sets, i, j);
            ret.append(&mut make_transform_node(
                name("root"),
                picture,
                xform,
                &stub,
                i,
                j,
            ));
            let in_node = if j == 0 {
                basis_name(&picture.identifier, i)
            } else {
                xform_set_node_name(&picture.identifier, i, j - 1)
            };
            ret.push(statement(fcall(
                name("connect"),
                vec![xform_set_node_name(&picture.identifier, i, j), in_node],
            )))
        });
    ret
}

fn establish_out(
    picture: &osk::Picture,
    xform: &osk::TransformSet,
    i: usize,
) -> Vec<py::Statement> {
    let out_node = if xform.transforms.is_empty() {
        basis_name(&picture.identifier, i)
    } else {
        xform_set_node_name(&picture.identifier, i, xform.transforms.len() - 1)
    };
    if xform.iteration {
        vec![
            statement(fcall(
                name("connect"),
                vec![iter_begin_name(&picture.identifier, i), out_node],
            )),
            assign(
                out_name(&picture.identifier, i),
                iter_end_name(&picture.identifier, i),
            ),
        ]
    } else {
        vec![assign(out_name(&picture.identifier, i), out_node)]
    }
}

fn assign_parameters_to_locals(picture: &osk::Picture) -> Vec<py::Statement> {
    picture
        .parameters
        .iter()
        .map(|p| assign(name(p), name(&format!("_{}", p))))
        .collect()
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
        assign(
            name(&xform_set.num_pics.pct_identifier),
            py::Expression::Bop(
                py::Bop::Div,
                _box(name(&xform_set.num_pics.nth_identifier)),
                _box(to_python_expression(&xform_set.num_pics.value)),
            ),
        ),
        assign(name(&xform_name), fcall(name("Empty"), vec![name(&root)])),
        assign(
            attribute(name(&xform_name), "name"),
            string(&picture.identifier),
        ),
    ];
    for transform in &xform_set.transforms {
        loop_body.push(statement(match transform {
            osk::Transform::Scale(x, y, z) => fcall(
                name("osk_scale"),
                vec![
                    name(&xform_name),
                    to_python_expression(x),
                    to_python_expression(y),
                    to_python_expression(z),
                ],
            ),
            osk::Transform::Translate(x, y, z) => fcall(
                name("osk_translate"),
                vec![
                    name(&xform_name),
                    to_python_expression(x),
                    to_python_expression(y),
                    to_python_expression(z),
                ],
            ),
            osk::Transform::Rotate(x, y, z) => fcall(
                name("osk_rotate"),
                vec![
                    name(&xform_name),
                    to_python_expression(x),
                    to_python_expression(y),
                    to_python_expression(z),
                ],
            ),
            osk::Transform::Color(_, _, _) => todo!(),
        }))
    }

    if i < xform_sets.len() - 1 {
        loop_body.push(codegen_standard_picture_transforms(
            picture,
            xform_sets,
            xform_name,
            i + 1,
        ))
    } else {
        let mut basis_args = vec![name(&xform_name), name("t")];
        for p in &picture.basis.parameters {
            basis_args.push(to_python_expression(p))
        }
        loop_body.push(statement(fcall(
            name(&picture.basis.identifier),
            basis_args,
        )));
    }

    for_loop(
        name(&xform_set.num_pics.nth_identifier),
        fcall(
            name("range"),
            vec![to_python_expression(&xform_set.num_pics.value)],
        ),
        loop_body,
    )
}

fn csg_invoke(invoke: &osk::Invoke, parameters: Vec<py::Expression>) -> py::Expression {
    parameters.clone().append(
        &mut invoke
            .parameters
            .iter()
            .map(|p| to_python_expression(p))
            .collect(),
    );
    fcall(name(&invoke.identifier), parameters)
}

fn codegen_standard_picture_csg(picture: &osk::Picture, csgs: &[osk::Csg]) -> Vec<py::Statement> {
    let mut ret = vec![];
    let var = name("node");
    ret.push(assign(
        var.clone(),
        csg_invoke(&picture.basis, vec![name("root"), name("_pt")]),
    ));
    csgs.iter().for_each(|csg| {
        let var = var.clone();
        let (rhs, operation) = match csg {
            osk::Csg::Union(invoke) => (
                csg_invoke(&invoke, vec![name("root"), name("_pt")]),
                string("union"),
            ),
            osk::Csg::Intersection(invoke) => (
                csg_invoke(&invoke, vec![name("root"), name("_pt")]),
                string("intersect"),
            ),
            osk::Csg::Difference(invoke) => (
                csg_invoke(&invoke, vec![name("root"), name("_pt")]),
                string("subtract"),
            ),
            osk::Csg::Concatenation(invoke) => (
                csg_invoke(&invoke, vec![name("root"), name("_pt")]),
                string("concatenate"),
            ),
        };
        ret.push(assign(
            var.clone(),
            fcall(name("create_csg"), vec![name("root"), var, rhs, operation]),
        ));
    });
    ret.push(statement(mcall(name("root"), "layoutChildren", vec![])));
    ret.push(py_return(var));
    ret
}

fn codegen_standard_picture(picture: osk::Picture) -> py::Statement {
    let mut body = vec![assign(name("t"), name("pt"))];

    let body_specific = match picture.operations {
        osk::Operations::TransformSet(ref xforms) => {
            codegen_standard_picture_transforms(&picture, xforms, "root".to_owned(), 0)
        }
        osk::Operations::Csg(_) => todo!(),
    };

    body.push(body_specific);

    let mut funcdef_parameters = vec!["root".to_owned(), "pt".to_owned()];
    for p in picture.parameters {
        funcdef_parameters.push(p)
    }

    funcdef_statement(funcdef(&picture.identifier, funcdef_parameters, body))
}

fn codegen_picture_selection(picture_list: osk::PictureList) -> Vec<py::Statement> {
    let body = vec![py_return(subscript(
        list_literal(
            picture_list
                .invokes
                .iter()
                .map(|i| name(&i.identifier))
                .collect(),
        ),
        name("i"),
    ))];
    vec![funcdef_statement(funcdef(
        &picture_list.identifier,
        vec!["i".to_owned()],
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
        osk::TopLevel::Definition(osk::Definition::Selection(p)) => codegen_picture_selection(p),
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
