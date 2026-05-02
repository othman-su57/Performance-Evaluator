import inspect
import multiprocessing
import time

from backend.data_generator import DataGenerator
from size_generator import GrowthPace, SizeGenerator


# ==========================================
# الدالة المعزولة (العامل المستقل)
# يجب أن تكون هنا في الخارج لتجنب خطأ Pickle
# ==========================================
def isolated_worker(user_code: str, func_name: str, func_type: str, size: int, case_type: str,
                    q: multiprocessing.Queue):
    try:
        # 1. تهيئة البيئة واستخراج الدالة
        scope = {}
        exec(user_code, scope)
        target_func = scope[func_name]

        # 2. توليد البيانات مرة واحدة (البيانات الأصلية)
        dataset = DataGenerator.generate(size)
        original_array = dataset[case_type]["list"]
        target = dataset[case_type]["target"]

        num_runs = 20
        total_time = 0.0

        # 3. حلقة القياس المتعدد
        for _ in range(num_runs):
            # أخذ نسخة من البيانات في كل مرة، لأن بعض الخوارزميات (مثل Sort)
            # تعدل المصفوفة في نفس المكان (In-place)، وإذا لم نأخذ نسخة،
            # ستكون المصفوفة مرتبة في اللفة الثانية وتفسد القياس!
            test_array = original_array.copy()

            # بدء القياس
            start_time = time.perf_counter()

            if func_type == "sort":
                target_func(test_array)
            elif func_type == "search":
                target_func(test_array, target)

            # إيقاف القياس
            end_time = time.perf_counter()

            total_time += (end_time - start_time)

        # 4. حساب المتوسط وإرساله
        average_time = total_time / num_runs
        q.put(("success", average_time))

    except Exception as e:
        q.put(("error", str(e)))


# ==========================================
# محرك التشغيل الرئيسي
# ==========================================
class ExecutionEngine:
    def __init__(self, timeout_seconds):
        self.timeout_seconds = timeout_seconds

    def run_analysis(self, user_code: str, func_name: str) -> dict:
        results = {"best": [], "avarage": [], "worst": []}

        # فحص مبدئي سريع لنوع الدالة لتمريره للعامل
        try:
            temp_scope = {}
            exec(user_code, temp_scope)
            if func_name not in temp_scope:
                return {"status": "error", "message": f"Function '{func_name}' not found in the code."}

            params = inspect.signature(temp_scope[func_name]).parameters
            if len(params) == 1:
                func_type = "sort"
            elif len(params) == 2:
                func_type = "search"
            else:
                return {"status": "error", "message": "Unsupported function signature"}
        except Exception as e:
              print({"status": "error", "message": f"Execution setup error: {str(e)}"})

        growth_paces = list(GrowthPace)

        for case_type in ["best", "avarage", "worst"]:
            for i in range(15,4, -3):
                for growth_pace in growth_paces:
                    sizes = SizeGenerator.generate_sizes(growth_pace,i)
                    print(growth_pace)
                    print(sizes)
                    for size in sizes:
                        # تجهيز قناة الاتصال والعملية المعزولة
                        q = multiprocessing.Queue()
                        p = multiprocessing.Process(
                            target=isolated_worker,
                            args=(user_code, func_name, func_type, size, case_type, q)
                        )

                        p.start()
                        p.join(self.timeout_seconds)

                        # معالجة الـ Timeout
                        if p.is_alive():
                            p.terminate()
                            p.join()
                            print(
                                f"[Warning] Timeout reached for {case_type} case at size {size}. Falling back to slower pace.")
                            results[case_type].clear()
                            break  # كسر حلقة الأحجام والانتقال للسرعة الأبطأ

                        # جلب النتائج إذا نجحت العملية
                        if not q.empty():
                            status, exec_time_or_error = q.get()

                            if status == "error":
                                # 1. اعتراض خطأ الـ Recursion
                                if "recursion depth exceeded" in exec_time_or_error.lower():
                                    print(
                                        f"[Warning] Recursion limit reached for {case_type} case at size {size}. Falling back to slower pace.")
                                    results[case_type].clear()
                                    break  # كسر الحلقة للانتقال للسرعة الأبطأ (نفس سلوك الـ Timeout)

                                # 2. أي خطأ آخر (Syntax, TypeError) هو خطأ مميت
                                else:
                                    return {
                                        "status": "error",
                                        "message": f"Runtime Error in {case_type} case (size {size}): {exec_time_or_error}"
                                    }
                            elif status == "success":
                                results[case_type].append((size, exec_time_or_error))
                        else:
                            return {"status": "error", "message": "Unknown multiprocessing error: Queue empty."}

                # إذا اكتملت قائمة الأحجام بالكامل بنجاح نغادر حلقة السرعة
                    if len(results[case_type]) == len(sizes):
                        break
                if len(results[case_type]) == i:
                    break

        return {"status": "success", "data": results}


# ==========================================
# تجربة الوحدة (Unit Testing)
# ==========================================
if __name__ == "__main__":
    test_code = """
def exponential_test(arr):
    n = len(arr)
    
    def branch(x):
        if x <= 0:
            return 1
        return branch(x - 1) + branch(x - 1)
        
    return branch(n)
"""

    engine = ExecutionEngine(timeout_seconds=0.5)
    output = engine.run_analysis(test_code, "exponential_test")

    import pprint

    pprint.pprint(output)