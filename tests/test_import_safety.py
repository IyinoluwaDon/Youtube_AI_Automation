import ast
from pathlib import Path

def test_manual_integrations_have_no_top_level_calls():
    for path in Path(__file__).parent.glob("test_*.py"):
        if path.name=="test_import_safety.py":continue
        tree=ast.parse(path.read_text(encoding="utf-8"))
        assert all(isinstance(node,(ast.If,ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef)) or (isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant)) for node in tree.body),path.name
