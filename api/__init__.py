
from backend.input_parser import CodeParser
from backend.excecution_anlyser import ExecutionEngine
from backend.math_engine import MathAnalyzer


class AlgorithmEvaluatorAPI:
    VALID_CASES = {"sorted", "random", "reversed"}

    def __init__(self, timeout_seconds=0.5):
        self.execution_engine = ExecutionEngine(timeout_seconds=timeout_seconds)
        self.math_analyzer = MathAnalyzer()

    # ==========================
    # PUBLIC
    # ==========================
    def evaluate(self, source_code: str) -> dict:

        # -------- 1) Input Validation --------
        validation_error = self._validate_inputs(source_code)
        if validation_error:
            return validation_error

        # -------- 2) Static Analysis --------
        parse_result = self._run_static_analysis(source_code)
        if parse_result["status"] == "error":
            return parse_result

        func_name = parse_result["function_name"]

        # -------- 3) Dynamic Execution --------
        exec_result = self._run_dynamic_analysis(source_code, func_name)
        if exec_result["status"] == "error":
            return exec_result

        raw_data = exec_result["data"]

        # -------- 4) Math Analysis --------
        math_result = self._run_math_analysis(raw_data)

        # -------- 5) Final Report --------
        return self._build_response(parse_result, math_result, raw_data)

    # ==========================
    # INTERNAL METHODS
    # ==========================

    def _validate_inputs(self, source_code):
        if not source_code.strip():
            return {"status": "error", "message": "Empty source code"}

        return None

    def _run_static_analysis(self, source_code):
        parser = CodeParser(source_code)
        result = parser.parse()

        if result["status"] == "error":
            return result

        return result

    def _run_dynamic_analysis(self, source_code, func_name):
        return self.execution_engine.run_analysis(source_code, func_name)

    def _run_math_analysis(self, raw_data):


        math_results = {}

        for case in [ "sorted", "random","reversed"]:
            case_data = raw_data.get(case, [])

            sizes = [p[0] for p in case_data if p[1] is not None]
            times = [p[1] for p in case_data if p[1] is not None]

            math_results[case] = self.math_analyzer.analyze(sizes, times)

        return math_results


    def _build_response(self, parse_result, math_result, raw_data):
        return {
            "status": "success",

            "metadata": {
                "function_name": parse_result.get("function_name"),
            },

            "static_analysis": parse_result.get("static_analysis", {}),

            "dynamic_analysis": {
                "complexity_estimation": math_result,
                "raw_plot_data": raw_data
            }
        }
if __name__ =="__main__":
    test_code = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
"""
    response = AlgorithmEvaluatorAPI(0.5).evaluate(test_code)
    import json

    print(json.dumps(response, indent=4, ensure_ascii=False))