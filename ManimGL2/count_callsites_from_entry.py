import ast
import sys

class DefCollector(ast.NodeVisitor):
    def __init__(self):
        self.order = []
        self.bodies = {}

    def visit_FunctionDef(self, node):
        name = node.name
        if name not in self.bodies:
            self.order.append(name)
            self.bodies[name] = node
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        name = node.name
        if name not in self.bodies:
            self.order.append(name)
            self.bodies[name] = node
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = item.name
                if name not in self.bodies:
                    self.order.append(name)
                    self.bodies[name] = item
        self.generic_visit(node)

class CallCollector(ast.NodeVisitor):
    def __init__(self, defs):
        self.defs = defs
        self.calls = {}

    def visit_Call(self, node):
        name = None
        f = node.func
        if isinstance(f, ast.Name):
            name = f.id
        elif isinstance(f, ast.Attribute):
            name = f.attr
        if name is not None and name in self.defs:
            self.calls[name] = self.calls.get(name, 0) + 1
        self.generic_visit(node)

def build_call_graph(source):
    tree = ast.parse(source)
    dc = DefCollector()
    dc.visit(tree)
    defs = set(dc.bodies.keys())
    graph = {name: {} for name in defs}
    for name, node in dc.bodies.items():
        cc = CallCollector(defs)
        for stmt in node.body:
            cc.visit(stmt)
        graph[name] = cc.calls
    return dc.order, graph

def accumulate_from_entry(order, graph, entry):
    total = {name: 0 for name in order}
    visited = set()
    def dfs(fn):
        if fn in visited:
            return
        visited.add(fn)
        for callee, cnt in graph.get(fn, {}).items():
            total[callee] += cnt
            dfs(callee)
    if entry in graph:
        dfs(entry)
        total[entry] += 1
    return total

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_callsites_from_entry.py file.py [entry_func]")
        sys.exit(1)
    path = sys.argv[1]
    entry = sys.argv[2] if len(sys.argv) >= 3 else "construct"
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    order, graph = build_call_graph(src)
    if entry not in graph:
        print(f"Entry function '{entry}' not found. Available functions:")
        for name in order:
            print(" ", name)
        sys.exit(1)
    total = accumulate_from_entry(order, graph, entry)
    print(f"File: {path}, entry = {entry}")
    print(f"{'Function':25} {'FromEntryCalls'}")
    print("-" * 40)
    for name in order:
        print(f"{name:25} {total[name]}")

if __name__ == "__main__":
    main()
