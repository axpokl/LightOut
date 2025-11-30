import ast
from collections import Counter
import sys

class CallsiteCounter(ast.NodeVisitor):
    def __init__(self):
        self.defined_funcs = []
        self._seen = set()
        self.calls = Counter()

    def _add_func(self, name):
        if name not in self._seen:
            self._seen.add(name)
            self.defined_funcs.append(name)

    def visit_FunctionDef(self, node):
        self._add_func(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._add_func(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in self._seen:
                self.calls[name] += 1
        self.generic_visit(node)

def main(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    tree = ast.parse(code, filename=path)
    counter = CallsiteCounter()
    counter.visit(tree)
    print(f"File: {path}")
    print(f"{'Function':20} Callsites")
    print("-" * 32)
    for name in counter.defined_funcs:
        print(f"{name:20} {counter.calls.get(name, 0)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_callsites.py your_file.py")
        sys.exit(1)
    main(sys.argv[1])
