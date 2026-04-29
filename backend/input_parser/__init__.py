import ast


class CodeParser:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tree = None

        self.function_name = None
        self.is_valid = False
        self.error_message = ""

        # ---- static metrics ----
        #loop detector
        self.max_loop_depth = 0
        self.loop_count = 0
        #recursion detector
        self.is_recursive = False
        self.recursive_calls = 0
        self.max_recursion_depth_estimate = 0

        self.function_calls = 0
        self.has_divide_and_conquer = False

    # ==========================
    # PUBLIC
    # ==========================
    def parse(self) -> dict:
        try:
            self.tree = ast.parse(self.source_code)
            self.is_valid = True

            func_node= self._extract_function_name()

            if not self.function_name:
                return {
                    "status": "error",
                    "message": "No function found"
                }


            # تحليل الحلقات
            self.max_loop_depth = self._calculate_loop_depth(func_node)
            self.loop_count = self._count_loops(func_node)

            # تحليل الاستدعاءات
            self._analyze_calls(func_node)

            # تحليل recursion
            self._analyze_recursion(func_node)

            return {
                "status": "success",
                "function_name": self.function_name,
                "static_analysis": {
                    "loops": {
                        "count": self.loop_count,
                        "max_depth": self.max_loop_depth
                    },
                    "recursion": {
                        "is_recursive": self.is_recursive,
                        "recursive_calls": self.recursive_calls,
                        "depth_estimate": self.max_recursion_depth_estimate
                    },
                    "calls": {
                        "total_calls": self.function_calls,
                        "divide_and_conquer": self.has_divide_and_conquer
                    }
                }
            }

        except SyntaxError as e:
            return {
                "status": "error",
                "message": f"Syntax Error at line {e.lineno}: {e.msg}"
            }

    # ==========================
    # INTERNAL HELPERS
    # ==========================

    # main method must be the first in code
    def _extract_function_name(self):
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef):
                self.function_name = node.name
                return node



    # -------- Loop Analysis --------
    def _calculate_loop_depth(self, node) -> int:
        max_depth = 0
        for child in ast.iter_child_nodes(node):
            depth = self._calculate_loop_depth(child)
            if isinstance(child, (ast.For, ast.While)):
                depth += 1
            max_depth = max(max_depth, depth)
        return max_depth

    def _count_loops(self, node) -> int:
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                count += 1
        return count

    # -------- Calls Analysis --------
    def _analyze_calls(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                self.function_calls += 1

    # -------- Recursion Analysis --------
    def _analyze_recursion(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    if child.func.id == self.function_name:
                        self.is_recursive = True
                        self.recursive_calls += 1

        # تقدير بسيط للعمق (heuristic)
        if self.is_recursive:
            if self.recursive_calls == 1:
                self.max_recursion_depth_estimate = "O(n)"
            elif self.recursive_calls >= 2:
                self.max_recursion_depth_estimate = "O(log n) or branching"
                self.has_divide_and_conquer = True

import unittest



class TestCodeParser(unittest.TestCase):

    def test_merge_sort_recursion(self):
        code = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return left + right
"""
        parser = CodeParser(code)
        result = parser.parse()

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["static_analysis"]["recursion"]["is_recursive"])
        self.assertTrue(result["static_analysis"]["calls"]["divide_and_conquer"])

    def test_nested_loops(self):
        code = """
def test(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
"""
        parser = CodeParser(code)
        result = parser.parse()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["static_analysis"]["loops"]["max_depth"], 2)

    def test_linear_search_no_recursion(self):
        code = """
def linear_search(arr, target):
    for x in arr:
        if x == target:
            return True
    return False
"""
        parser = CodeParser(code)
        result = parser.parse()

        self.assertFalse(result["static_analysis"]["recursion"]["is_recursive"])
        self.assertEqual(result["static_analysis"]["loops"]["max_depth"], 1)

    def test_syntax_error(self):
        code = """
def broken(
    print("error")
"""
        parser = CodeParser(code)
        result = parser.parse()

        self.assertEqual(result["status"], "error")

    def test_no_function(self):
        code = """
x = 10
y = 20
"""
        parser = CodeParser(code)
        result = parser.parse()

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()