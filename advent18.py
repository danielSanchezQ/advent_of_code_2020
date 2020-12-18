import ast
import operator


def eval_module(expr: ast.Module):
    return eval_expr(expr.body[0].value)


def eval_constant(constant: ast.Constant):
    return constant.value


def binop_constant(binop: ast.BinOp):
    return operation[type(binop.op)](eval_expr(binop.left), eval_expr(binop.right))


def binop_left(binop: ast.BinOp):
    binop.left.left.value = operation[type(binop.op)](binop.left.left.value, binop.right.value)
    return eval_expr(binop.left)


def binop_right(binop: ast.BinOp):
    binop.right.left.value = operation[type(binop.op)](binop.right.left.value, binop.left.value)
    return eval_expr(binop.right)


def eval_binop(binop: ast.BinOp):
    return binop_operation[(type(binop.left), type(binop.right))](binop)


binop_operation = {
    (ast.Constant, ast.Constant): binop_constant,
    (ast.BinOp, ast.Constant): binop_left,
    (ast.Constant, ast.BinOp): binop_right,
}

operation = {
    ast.Add: operator.add,
    ast.Mult: operator.mul
}

eval_nodes = {
    ast.Module: eval_module,
    ast.Constant: eval_constant,
    ast.BinOp: eval_binop
}


def eval_expr(node: ast.AST):
    return eval_nodes[type(node)](node)


def load_data(stream):
    return (ast.parse(line.rstrip(), mode='eval') for line in stream)


def part_1(ast_stream):
    return sum(map(eval_expr, ast_stream))


if __name__ == "__main__":
    # exp = ast.parse("5 + (9 + (7 + 5 + 3 * 8 + 4 * 6) + 9 * 8 * 7)")
    exp = ast.parse("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    print(eval_expr(exp))
    # with open("./input/advent18.txt") as f:
        # print(part_1(load_data(f)))