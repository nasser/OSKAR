use crate::ast as osk;
use python_parser::ast as py;
use python_parser::visitors::printer::format_module;

fn to_python_statements(code: &str) -> Vec<py::Statement> {
    match python_parser::file_input(python_parser::make_strspan(code)) {
        Ok((_, stmnts)) => stmnts,
        Err(_) => panic!("could not parse {}", code),
    }
}

fn to_python_expression(code: &str) -> py::Expression {
    match to_python_statements(code) {
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

fn py_print(args: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        Box::new(name("print")),
        args.into_iter()
            .map(|a| py::Argument::Positional(a))
            .collect(),
    )
}

fn py_return(expression: py::Expression) -> py::Statement {
    py::Statement::Return(vec![expression])
}

fn py_print_stmt(args: Vec<py::Expression>) -> py::Statement {
    py::Statement::Expressions(vec![py_print(args)])
}

fn mcall(target: py::Expression, name: &str, arguments: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(py::Expression::Attribute(_box(target), name.to_string())),
        arguments
            .into_iter()
            .map(|a| py::Argument::Positional(a))
            .collect(),
    )
}

fn fcall(target: py::Expression, arguments: Vec<py::Expression>) -> py::Expression {
    py::Expression::Call(
        _box(target),
        arguments
            .into_iter()
            .map(|a| py::Argument::Positional(a))
            .collect(),
    )
}

fn bop_or(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Bop(py::Bop::Or, _box(lhs), _box(rhs))
}

fn statement(ex: py::Expression) -> py::Statement {
    py::Statement::Expressions(vec![ex])
}

fn subscript(lhs: py::Expression, rhs: py::Expression) -> py::Expression {
    py::Expression::Subscript(_box(lhs), vec![py::Subscript::Simple(rhs)])
}

fn typed_args_list(names: Vec<&str>) -> py::TypedArgsList {
    let args = names.iter().map(|n| (n.to_string(), None, None)).collect();
    py::TypedArgsList {
        args,
        posonly_args: vec![],
        star_args: py::StarParams::No,
        keyword_args: vec![],
        star_kwargs: None,
    }
}

fn funcdef(name: &str, params: Vec<&str>, code: Vec<py::Statement>) -> py::Statement {
    let name = name.to_string();
    let r#async = false;
    let decorators = vec![];
    let parameters = typed_args_list(params);
    let return_type = None;

    py::Statement::Compound(_box(py::CompoundStatement::Funcdef(py::Funcdef {
        r#async,
        decorators,
        name,
        return_type,
        code,
        parameters,
    })))
}

fn hou_make_visible(target: py::Expression) -> py::Expression {
    mcall(target, "setDisplayFlag", vec![py::Expression::Int(1)])
}

fn codegen_film(film: osk::Film) -> Vec<py::Statement> {
    let mut film_func_body = vec![
        assign(
            name("node"),
            fcall(
                name(&film.picture.identifier),
                vec![name("root"), name("t")],
            ),
        ),
        statement(hou_make_visible(name("node"))),
    ];
    film.film_parameters
        .iter()
        .for_each(|(k, v)| match k.as_ref() {
            "Frames" => film_func_body.push(statement(mcall(
                name("hou.playbar"),
                "setFrameRange",
                vec![integer(0), integer(v.parse::<u64>().unwrap())],
            ))),
            _ => (),
        });
    let film_func = funcdef("Film", vec!["root", "t"], film_func_body);
    vec![
        film_func,
        statement(fcall(name("Film"), vec![name("root"), name("global_time")])),
    ]
}

fn iter_begin_name(i: usize) -> py::Expression {
    name(&format!("xform{}_iter_begin", i))
}

fn iter_end_name(i: usize) -> py::Expression {
    name(&format!("xform{}_iter_end", i))
}

fn iter_meta_name(i: usize) -> py::Expression {
    name(&format!("xform{}_iter_meta_path", i))
}

fn time_func_name_str(i: usize) -> String {
    format!("xform{}_time", i)
}

fn time_func_name(i: usize) -> py::Expression {
    name(&time_func_name_str(i))
}

fn env_func_name_str(i: usize) -> String {
    format!("xform{}_env", i)
}

fn env_func_name(i: usize) -> py::Expression {
    name(&env_func_name_str(i))
}

fn prelude_name(i: usize) -> py::Expression {
    name(&format!("xform{}_prelude", i))
}

fn basis_name(i: usize) -> py::Expression {
    name(&format!("xform{}_basis", i))
}

fn out_name(i: usize) -> py::Expression {
    name(&format!("xform{}_out", i))
}

fn xform_set_node_name(xform_num: usize, node_num: usize) -> py::Expression {
    name(&format!("xform{}_node{}", xform_num, node_num))
}

fn iteration_networks(
    picture: &osk::Picture,
    transforms: &Vec<osk::TransformSet>,
) -> Vec<py::Statement> {
    let mut ret = vec![];
    transforms.iter().enumerate().for_each(|(i, t)| {
        if t.iteration {
            let iter_name = format!("{}_xform{}", picture.identifier, i);
            let iter_value = to_python_expression(&t.num_pics.number);
            ret.push(assign(
                tuple(vec![
                    iter_begin_name(i),
                    iter_end_name(i),
                    iter_meta_name(i),
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

fn get_iteration_value(i: usize) -> py::Expression {
    fcall(name("iteration_value"), vec![iter_meta_name(i)])
}

fn env_func(xforms: &Vec<osk::TransformSet>, i: usize) -> py::Statement {
    let pt = if i == 0 {
        name("_pt")
    } else {
        time_func_name(i - 1)
    };
    let mut body = vec![
        // time variables
        assign(name("pt"), fcall(pt, vec![])),
        assign(name("t"), name("pt")),
    ];
    xforms.iter().enumerate().rev().for_each(|(j, t)| {
        // iteration variables
        if j >= i {
            // later xform sets cannot see earlier iteration vars
            let identifier = match &t.num_pics.identifier {
                Some(id) => name(&id),
                _ => name("i"),
            };
            let value = if t.iteration {
                get_iteration_value(j)
            } else {
                integer(0)
            };
            body.push(assign(identifier, value));
        }
    });

    match &xforms[i].top_level_expression {
        Some(lines) => lines
            .iter()
            .for_each(|l| body.append(&mut to_python_statements(l))),
        _ => (),
    };
    body.push(py_return(fcall(name("locals"), vec![])));
    funcdef(&env_func_name_str(i), vec![], body)
}

fn time_func(i: usize) -> py::Statement {
    funcdef(
        &time_func_name_str(i),
        vec![],
        vec![py_return(subscript(
            fcall(env_func_name(i), vec![]),
            string("t"),
        ))],
    )
}

fn basis_value(picture: &osk::Picture, i: usize) -> py::Statement {
    let basis_value = if i == 0 {
        // TODO not sure which time value to pass in here
        fcall(
            name(&picture.basis.identifier),
            vec![name("root"), time_func_name(i)],
        )
    } else {
        out_name(i - 1)
    };
    assign(basis_name(i), basis_value)
}

fn or_default_expression(x: &Option<String>, d: &str) -> py::Expression {
    match x {
        Some(s) => string(s),
        None => string(d),
    }
}

fn transform_set_nodes(
    picture: &osk::Picture,
    t: &osk::TransformSet,
    i: usize,
) -> Vec<py::Statement> {
    let mut ret = vec![];
    t.transforms.iter().enumerate().for_each(|(j, node)| {
        let (f, x, y, z) = match node {
            osk::Transform::Translate(x, y, z) => (
                name("translate"),
                or_default_expression(x, "0"),
                or_default_expression(y, "0"),
                or_default_expression(z, "0"),
            ),
            osk::Transform::Rotate(x, y, z) => (
                name("rotate"),
                or_default_expression(x, "0"),
                or_default_expression(y, "0"),
                or_default_expression(z, "0"),
            ),
            osk::Transform::Scale(x, y, z) => (
                name("scale"),
                or_default_expression(x, "1"),
                or_default_expression(y, "1"),
                or_default_expression(z, "1"),
            ),
        };
        ret.push(assign(
            xform_set_node_name(i, j),
            fcall(
                f,
                vec![
                    name("root"),
                    string(&format!("{}_{}_{}", picture.identifier, i, j)),
                    prelude_name(i),
                    x,
                    y,
                    z,
                ],
            ),
        ));
        let in_node = if j == 0 {
            basis_name(i)
        } else {
            xform_set_node_name(i, j - 1)
        };
        ret.push(statement(fcall(
            name("connect"),
            vec![xform_set_node_name(i, j), in_node],
        )))
    });
    ret
}

fn establish_out(xform: &osk::TransformSet, i: usize) -> Vec<py::Statement> {
    let out_node = if xform.transforms.len() == 0 {
        basis_name(i)
    } else {
        xform_set_node_name(i, xform.transforms.len() - 1)
    };
    if xform.iteration {
        vec![
            statement(fcall(name("connect"), vec![iter_begin_name(i), out_node])),
            assign(out_name(i), iter_end_name(i)),
        ]
    } else {
        vec![assign(out_name(i), out_node)]
    }
}

fn codegen_standard_picture_transforms(
    picture: &osk::Picture,
    xforms: &Vec<osk::TransformSet>,
) -> Vec<py::Statement> {
    let mut body = vec![];
    // 1. create iteration networks
    body.append(&mut iteration_networks(picture, &xforms));

    // 2. for each transform set
    xforms.iter().enumerate().for_each(|(i, t)| {
        // 2.1 declare environment function
        body.push(env_func(&xforms, i));
        // 2.2 declare local time function
        body.push(time_func(i));
        // 2.3 establish prelude
        body.push(assign(
            prelude_name(i),
            fcall(name("expression_prelude"), vec![env_func_name(i)]),
        ));
        // 2.4 establish basis for this transform set
        body.push(basis_value(picture, i));

        // 2.5 generate transform set nodes
        // 2.6 wire transform set nodes together
        body.append(&mut transform_set_nodes(picture, t, i));

        // 2.7 establish out
        body.append(&mut establish_out(t, i))
    });
    // 3. clean up and return last node
    body.push(statement(mcall(name("root"), "layoutChildren", vec![])));
    body.push(py_return(out_name(xforms.len() - 1)));

    vec![funcdef(&picture.identifier, vec!["root", "_pt"], body)]
}

fn codegen_standard_picture_csg(
    _picture: &osk::Picture,
    _csgs: &Vec<osk::Csg>,
) -> Vec<py::Statement> {
    panic!("CSG not supported yet")
}

fn codegen_standard_picture(picture: osk::Picture) -> Vec<py::Statement> {
    match picture.operations {
        osk::Operations::TransformSet(ref xforms) => {
            codegen_standard_picture_transforms(&picture, xforms)
        }
        osk::Operations::Csg(ref csgs) => codegen_standard_picture_csg(&picture, csgs),
    }
}

pub fn codegen_toplevel(tl: osk::TopLevel) -> Vec<py::Statement> {
    match tl {
        osk::TopLevel::Film(f) => codegen_film(f),
        osk::TopLevel::Definition(osk::Definition::Standard(p)) => codegen_standard_picture(p),
        osk::TopLevel::Skip => unreachable!(),
        osk::TopLevel::PythonCodeBlock(_) => unreachable!(),
        _ => vec![py_print_stmt(vec![string("?")])],
    }
}

pub fn preamble() -> &'static str {
    include_str!("preamble.py")
}

pub fn establish_root(root_name: &str) -> String {
    // TODO does root_name need to be processed here? turn spaces into underscores?
    format_module(&vec![
        assign(
            name("root"),
            bop_or(
                mcall(
                    name("hou"),
                    "node",
                    vec![string(&format!("/obj/{}", root_name))],
                ),
                mcall(
                    mcall(name("hou"), "node", vec![string("/obj")]),
                    "createNode",
                    vec![string("geo")],
                ),
            ),
        ),
        statement(mcall(name("root"), "setName", vec![string(root_name)])),
    ])
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
