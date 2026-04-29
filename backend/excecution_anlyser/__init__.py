import inspect
import time

from backend.data_generator import DataGenerator


class ExecutionEngine:
    def __init__(self, timeout_seconds):
        # نحدد نصف ثانية كحد أقصى لتنفيذ الدالة الواحدة
        self.timeout_seconds = timeout_seconds

    def run_analysis(self, user_code: str, func_name: str, sizes) -> dict:
        execution_scope = {}
        # القاموس الذي سيحتوي على النتائج لإرسالها للواجهة
        results = {"best": [], "average": [], "worst": []}

        try:
            # 1. تهيئة البيئة المعزولة وحقن الكود
            exec(user_code, execution_scope)

            if func_name not in execution_scope:
                return {"status": "error", "message": f"Function '{func_name}' not found in the code."}


            target_func = execution_scope[func_name]
            params = inspect.signature(target_func).parameters

            if len(params) == 1:
                func_type = "sort"
            elif len(params) == 2:
                func_type = "search"
            else:
                return {"status": "error", "message": "Unsupported function signature"}
            # 2. اختبار الحالات الثلاث لكل حجم مصفوفة
            for case_type in ["best", "average", "worst"]:
                for size in sizes:
                    # نولد بيانات جديدة لكل محاولة لضمان الدقة
                    # (بافتراض أنك وضعت كلاس DataGenerator في نفس الملف أو قمت باستدعائه)
                    dataset = DataGenerator.generate(size)
                    test_array = dataset[case_type]["list"]
                    target = dataset[case_type]["target"]
                    # --- بدء القياس ---
                    start_time = time.perf_counter()

                    try:
                        # تشغيل دالة المستخدم
                        if func_type == "sort":
                            target_func(test_array.copy())
                        elif func_type == "search":
                            target_func(test_array,target)
                    except Exception as e:
                        # التقاط أي خطأ يحدث أثناء التشغيل (Runtime Error)
                        return {"status": "error",
                                "message": f"Runtime Error in {case_type} case (size {size}): {str(e)}"}

                    end_time = time.perf_counter()
                    # --- انتهاء القياس ---

                    exec_time = end_time - start_time
                    results[case_type].append((size, exec_time))

                    # صمام الأمان: إذا استغرق التنفيذ وقتاً طويلاً، نوقف التكبير في هذه الحالة
                    if exec_time > self.timeout_seconds:
                        print(f"[Warning] Timeout reached for {case_type} case at size {size}. Stopping larger inputs.")
                        break  # نخرج من حلقة الـ sizes وننتقل للحالة التالية (case_type)

            return {"status": "success", "data": results}

        except Exception as e:
            return {"status": "error", "message": f"Execution setup error: {str(e)}"}


# ==========================================
# تجربة الوحدة (Unit Testing)
# ==========================================
if __name__ == "__main__":
    # كود تجريبي لخوارزمية ترتيب فقاعي (Bubble Sort) أداؤها O(n^2)
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
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""
    # أحجام المصفوفات التي نريد اختبارها
    test_sizes = [10, 100, 500, 1000, 2000, 5000]

    engine = ExecutionEngine(timeout_seconds=5)

    # نمرر الكود، اسم الدالة (الذي المفترض أن CodeParser استخرجه)، والأحجام
    output = engine.run_analysis(test_code, "merge_sort", test_sizes)

    import pprint

    pprint.pprint(output)