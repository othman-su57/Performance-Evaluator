import time
import random


user_code = """
def my_algorithm(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr
"""

# 1. إنشاء قاموس فارغ لالتقاط ما سيكتبه المستخدم
execution_scope = {}

try:
    # 2. تنفيذ النص البرمجي بأمان نسبي
    # نمرر {} للمتغيرات العامة (Globals) ونمرر القاموس للمتغيرات المحلية (Locals)
    exec(user_code, {}, execution_scope)

    # 3. استخراج الدالة من القاموس 
    # في مشروعك، يمكنك إجبار المستخدم على اسم معين للدالة، أو البحث عن أول دالة قابلة للاستدعاء
    func_name = 'my_algorithm'

    if func_name in execution_scope:
        target_function = execution_scope[func_name]

        # --- اختبار التنفيذ وقياس الوقت ---
        # توليد مصفوفة عشوائية للتجربة
        test_array = [random.randint(1, 100) for _ in range(1000)]

        # بدء العداد بدقة عالية جداً
        start_time = time.perf_counter()

        # تشغيل دالة المستخدم وتمرير المصفوفة لها
        result = target_function(test_array)

        # إيقاف العداد
        end_time = time.perf_counter()

        execution_time = end_time - start_time

        print(f"Time taken for array size {len(test_array)}: {execution_time:.6f} seconds")

    else:
        print(f"Error: Function '{func_name}' not found in user code.")

except Exception as e:
    # التقاط أي خطأ في كود المستخدم (مثل أخطاء الـ Syntax)
    print(f"Compilation or Execution Error: {e}")