import ast

def parse_expression(expr):
    # Mapping for operators
    operator_map = {
        '+': ast.Add(),
        '-': ast.Sub(),
        '*': ast.Mult(),
        '/': ast.Div(),
        '%': ast.Mod(),
        '**': ast.Pow(),
        '&': ast.BitAnd(),
        '|': ast.BitOr(),
        '^': ast.BitXor(),
        '<<': ast.LShift(),
        '>>': ast.RShift(),
        '**': ast.Pow(),
    }
    
    # Replace bitwise operator symbols with their corresponding AST nodes
    for op, node in operator_map.items():
        expr = expr.replace(op, f' {op} ')

    return ast.parse(expr, mode='eval').body

def apply_substitutions(node):
    if isinstance(node, ast.BinOp):
        
        left = apply_substitutions(node.left)
        right = apply_substitutions(node.right)
        if isinstance(node.op, ast.BitAnd):
            return ast.BinOp(ast.BinOp(left, ast.Add(), right), ast.Sub(), ast.BinOp(left, ast.BitOr(), right))

        # Bitwise Or does not currently work. the transformation is: if the operation is X | Y then apply the substitution ~(~X&~Y)... FIXED !
       
        if isinstance(node.op, ast.BitOr):
            not_x = ast.UnaryOp(ast.Invert(), left)
            not_y = ast.UnaryOp(ast.Invert(), right)
            and_expr = ast.BinOp(not_x, ast.BitAnd(), not_y)
            sum_expr = ast.BinOp(left, ast.Add(), right)
            return ast.BinOp(and_expr, ast.Add(), ast.BinOp(sum_expr, ast.Sub(), and_expr))

        elif isinstance(node.op, ast.BitXor):
            return ast.BinOp(ast.BinOp(left, ast.BitOr(), right), ast.Sub(), ast.BinOp(left, ast.BitAnd(), right))

        elif isinstance(node.op, ast.Sub):
            return ast.BinOp(ast.BinOp(left, ast.BitXor(), ast.UnaryOp(ast.USub(), right)), 
                             ast.Add(), 
                             ast.BinOp(ast.BinOp(left, ast.BitAnd(), ast.UnaryOp(ast.USub(), right)),
                                       ast.Mult(),
                                       ast.Num(2)))

        elif isinstance(node.op, ast.Add):
            return ast.BinOp(ast.BinOp(left, ast.BitAnd(), right), ast.Add(), ast.BinOp(left, ast.BitOr(), right))

        # Default case: return the node as is if no specific rule exists for the operator
        else:
            return ast.BinOp(left, node.op, right)
    return node


def print_equation(node):
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Add):
            operator = '+'
        elif isinstance(node.op, ast.Sub):
            operator = '-'
        elif isinstance(node.op, ast.Mult):
            operator = '*'
        elif isinstance(node.op, ast.Div):
            operator = '/'
        elif isinstance(node.op, ast.Mod):
            operator = '%'
        elif isinstance(node.op, ast.Pow):
            operator = '**'
        elif isinstance(node.op, ast.BitAnd):
            operator = '&'
        elif isinstance(node.op, ast.BitOr):
            operator = '|'
        elif isinstance(node.op, ast.BitXor):
            operator = '^'
        else:
            operator = ''
        
        left = print_equation(node.left)
        right = print_equation(node.right)
        return f"({left} {operator} {right})"
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return f"-{print_equation(node.operand)}"
        elif isinstance(node.op, ast.Invert):
            return f"~{print_equation(node.operand)}"
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Name):
        return node.id
    else:
        return ''


if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    parsed_expression = parse_expression(expression)
    substituted_expression = apply_substitutions(parsed_expression)
    print("Original Expression:")
    print(expression)
    print("Obfuscated Expression:")
    print(print_equation(substituted_expression))
