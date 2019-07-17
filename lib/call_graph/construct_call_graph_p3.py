#!/usr/bin/env python

"""
    generates call graph of given python code file
    in dot format input for graphviz.

    limitations:
    * statically tried to figure out functions calls
    * does not understand classes
    * algorithm is naive and may not statically find
      all cases
"""

import sys
import ast
import symbol
import token
import optparse
import parser

"""
    Redundant block (from Python2) 
    TODO: Remove this block
    try:
        s = set()
    except Exception as e:
        print(repr(e))
        import sets
        set = sets.Set
"""

code_type = None

def annotate_ast_list(ast_list):
    code = ast_list[0]
    if code in symbol.sym_name:
        code = symbol.sym_name[code]
    else:
        code = token.tok_name[code]
    ast_list[0] = code

    for index, item in enumerate(ast_list):
        if index == 0: continue
        if isinstance(item, list):
            ast_list[index] = annotate_ast_list(item)
    return ast_list


def get_atom_name(atom):
    first_child = atom[1]
    first_child_code = first_child[0]
    if first_child_code != token.NAME: return None
    return first_child[1]


def get_fn_call_data(ast_list):
    if len(ast_list) < 3: return None
    first_child, second_child = ast_list[1:3]
    first_child_code = first_child[0]
    if first_child_code != symbol.atom: return None
    fn_name = get_atom_name(first_child)

    second_child_code = second_child[0]
    if second_child_code != symbol.trailer: return None

    if len(second_child) < 3: return None
    if second_child[1][0] == token.LPAR and second_child[-1][0] == token.RPAR:
        return fn_name
    else:
        return None


def find_fn_call(ast_list, calls):
    code = ast_list[0]
    if code == symbol.power:
        fn_name = get_fn_call_data(ast_list)
        if fn_name != None and getattr(__builtins__, fn_name, None) == None: calls.add(fn_name)

    for item in ast_list[1:]:
        if isinstance(item, list):
            find_fn_call(item, calls)


def process_fn(fn_ast_list, call_graph):
    dummy, dummy, func_name = fn_ast_list[:3]
    dummy, func_name = func_name

    calls = set()
    find_fn_call(fn_ast_list, calls)

    call_graph[func_name] = list(calls)


def construct_call_graph(ast_list_obj_body, call_graph):
    global code_type

    # print('Constructing call_graph')

    # print('ast_list_obj_body', repr(ast_list_obj_body))
    # print('call_graph', repr(call_graph))

    code = ast_list_obj_body[0]
    print('type code', type(ast_list_obj_body), 'type [0]', code, type(code))


    if code == symbol.funcdef:
        code_type = code
        print('code_type', code_type)
        process_fn(ast_list_obj_body, call_graph)

    for item in ast_list_obj_body[1:]:
        if isinstance(item, list):
            construct_call_graph(item, call_graph)

    return call_graph



def generate_dot_code(python_file):
    """
    generate_dot_code
    :param py_code:
    :return:
    """
    with open(python_file) as source:
        ast_module_obj = parser.suite(source.read())
        ast_obj_list = parser.st2list(ast_module_obj)

        # ast_module_obj = ast.parse(source.read(), python_file, mode='exec')
        # ast_module_obj_body = ast_module_obj.body

    ast_obj = ast_obj_list


    print('ast_list\n', repr(ast_module_obj))
    print('ast_iter_tuple\n', ast.iter_fields(ast_module_obj))
    # print('ast_body\n', ast_module_obj_body)
    print('ast_obj\n\n', repr(ast_obj))


    # print('ast.iter_child_nodes\n', ast.iter_child_nodes(ast_obj))
    # for b in ast.walk(ast_obj):
    #     print('ast_obj\n', repr(b))

    call_graph = {}
    construct_call_graph(ast_obj, call_graph)

    # pprint.pprint(call_graph)

    dot = []

    dot.append("digraph G {")
    dot.append("rankdir=LR")
    for from_fn, to_fns in call_graph.items():
        if not to_fns:
            dot.append('%s;' % from_fn)

        for to_fn in to_fns:
            if to_fn not in call_graph: continue
            dot.append('%s -> %s;' % (from_fn, to_fn))
    dot.append("}")

    return '\n'.join(dot)






if __name__ == '__main__':
    oparser = optparse.OptionParser()

    oparser.add_option('-i', '--input-file', default=None, metavar='FILE', help='python code file to process')

    options, args = oparser.parse_args()

    dot_code = generate_dot_code(options.input_file)

    print('\nDOT CODE\n', dot_code)
