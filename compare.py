import ast
from difflib import SequenceMatcher
import argparse


class Normalizer(ast.NodeTransformer):
    @staticmethod
    def normalize(node):
        # Упрощаем docstrings
        if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
            node.body = node.body[1:]
        # Упрощаем аннотаций функций
        node.args.kwonlyargs = []
        node.args.kw_defaults = []
        node.args.kwarg = None
        # Заменяем имена переменных
        for arg in node.args.args:
            arg.arg = "arg"
        return node


class SimilarityChecker:
    @staticmethod
    def check_similarity(code_1, code_2):
        tree_code_1 = ast.parse(code_1)
        tree_code_2 = ast.parse(code_2)
        Normalizer().visit(tree_code_1)
        Normalizer().visit(tree_code_2)

        # Возвращаем деревья обратно в код
        normalized_code_1 = ast.unparse(tree_code_1)
        normalized_code_2 = ast.unparse(tree_code_2)

        matcher = SequenceMatcher(None, normalized_code_1, normalized_code_2)
        return matcher.ratio()


verification_class = SimilarityChecker()

# добавляем входные данные через консоль
parser = argparse.ArgumentParser()
parser.add_argument("code_input_1", help="first code")
parser.add_argument("code_input_2", help="second code")
args = parser.parse_args()
code_input_1 = args.code_input_1
code_input_2 = args.code_input_2

result = verification_class.check_similarity(code_input_1, code_input_2)
print(result)
