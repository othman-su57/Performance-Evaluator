from backend.input_parser import CodeParser
from backend.excecution_anlyser import ExecutionEngine
from backend.math_engine import MathAnalyzer


class AlgorithmEvaluatorAPI:
    VALID_CASES = {"best", "average", "worst"}

    def __init__(self, timeout_seconds=0.5):
        self.execution_engine = ExecutionEngine(timeout_seconds=timeout_seconds)
        self.math_analyzer = MathAnalyzer()

    # ==========================
    # PUBLIC
    # ==========================
    def evaluate(self, source_code: str, test_sizes: list, complexity: str = "worst") -> dict:

        # -------- 1) Input Validation --------
        validation_error = self._validate_inputs(source_code, test_sizes, complexity)
        if validation_error:
            return validation_error

        # -------- 2) Static Analysis --------
        parse_result = self._run_static_analysis(source_code)
        if parse_result["status"] == "error":
            return parse_result

        func_name = parse_result["function_name"]

        # -------- 3) Dynamic Execution --------
        exec_result = self._run_dynamic_analysis(source_code, func_name, test_sizes)
        if exec_result["status"] == "error":
            return exec_result

        raw_data = exec_result["data"]

        # -------- 4) Math Analysis --------
        math_result = self._run_math_analysis(raw_data, complexity)

        # -------- 5) Final Report --------
        return self._build_response(parse_result, math_result, raw_data)

    # ==========================
    # INTERNAL METHODS
    # ==========================

    def _validate_inputs(self, source_code, test_sizes, complexity):
        if not source_code.strip():
            return {"status": "error", "message": "Empty source code"}

        if not isinstance(test_sizes, list) or len(test_sizes) < 2:
            return {"status": "error", "message": "test_sizes must be a list with at least 2 values"}

        if complexity not in self.VALID_CASES:
            return {"status": "error", "message": f"Invalid complexity type: {complexity}"}

        return None

    def _run_static_analysis(self, source_code):
        parser = CodeParser(source_code)
        result = parser.parse()

        if result["status"] == "error":
            return result

        return result

    def _run_dynamic_analysis(self, source_code, func_name, test_sizes):
        return self.execution_engine.run_analysis(source_code, func_name, test_sizes)

    def _run_math_analysis(self, raw_data, complexity):
        case_data = raw_data.get(complexity, [])

        if not case_data:
            return {
                "status": "error",
                "message": "No data available for selected case"
            }

        sizes = [p[0] for p in case_data if p[1] is not None]
        times = [p[1] for p in case_data if p[1] is not None]

        if len(sizes) < 2:
            return {
                "status": "error",
                "message": "Insufficient valid data points"
            }

        return self.math_analyzer.analyze(sizes, times)

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
