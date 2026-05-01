import numpy as np
from scipy.optimize import curve_fit
from scipy.special import factorial
import warnings
import math

from sympy.ntheory import generate


class MathAnalyzer:
    def __init__(self):
        self.complexity_classes = {
            "O(1)"      : lambda x, a: a * np.ones_like(x),
            "O(lg n)"   : lambda x, a: a * np.log(np.maximum(x, 1e-10)),
            "O(n)"      : lambda x, a: a * x,
            "O(n log n)": lambda x, a: a * x * np.log(np.maximum(x, 1e-10)),
            "O(n^2)"    : lambda x, a: a * x ** 2,
            "O(n^3)"    : lambda x, a: a * x ** 3,
            "O(2^n)"    : lambda x, a: a * (2.0 ** np.minimum(x, 50)),
            # تم استخدام scipy.special.factorial لدعم مصفوفات NumPy دون أخطاء
            "O(n!)"     : lambda x, a: a * factorial(np.minimum(x, 10))
        }

    def analyze(self, sizes: list, times: list) -> dict:

        x = np.array(sizes, dtype=float)
        y = np.array(times, dtype=float)

        best_fit = None
        best_error = float("inf")
        best_y_pred = None

        results_debug = {}
        y_preds_debug = {}  # لتخزين المنحنيات واستدعائها عند التعارض

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # --- أولًا: تحليل الحالات التوكسك ---
            toxic_result = self.analyze_toxics(x, y)

            # --- ثانيًا: curve fitting ---
            params_debug = {}
            for name, func in self.complexity_classes.items():
                try:
                    popt, _ = curve_fit(func, x, y, maxfev=5000)
                    params_debug[name] = popt
                    y_pred = func(x, *popt)

                    error = np.mean(((y - y_pred) / (y + 1e-10)) ** 2)

                    results_debug[name] = error
                    y_preds_debug[name] = y_pred

                    if error < best_error:
                        best_error = error
                        best_fit = name
                        best_popt = params_debug[best_fit]

                except Exception:
                    continue

        # --- حل التعارض بين n و n log n ---
    #   ""
    #if best_fit in {"O(n)", "O(n log n)"}:
    #        if "O(n)" in results_debug and "O(n log n)" in results_debug:
    #
    #           e1 = results_debug["O(n)"]
    #           e2 = results_debug["O(n log n)"]

    #           if abs(e1 - e2) / (e1 + 1e-10) < 0.2:
    #               best_fit = toxic_result
    #            # تحديث الرسم البياني ونسبة الخطأ بناءً على الفائز الجديد
    #               best_y_pred = y_preds_debug[toxic_result]
    #               best_error = results_debug[toxic_result]
    #               best_popt = params_debug[best_fit]

        # --- حساب الثقة ---
        sorted_errors = sorted(results_debug.values())
        if len(sorted_errors) >= 2:
            gap = sorted_errors[1] - sorted_errors[0]
            confidence = min(100, max(0, gap * 5000))
        else:
            confidence = 50

        return {
            "status": "success",
            "detected_complexity": best_fit,
            "error_score": best_error,
            "confidence_percentage": round(confidence, 2),
            "debug_errors": results_debug,
            "curve_data": self.generate_smooth_curve(
                        self.complexity_classes[best_fit],
                         x[0],
                         x[-1],
                         best_popt
                         )
        }

    def analyze_toxics(self, n, T):
        # نأخذ أكبر 3 أحجام فقط لنتجاهل ضجيج بايثون في الأحجام الصغيرة

        n_large = n
        T_large = T
        ratio_n = T_large *1e6 / (n_large + 1e-10)
        # نستخدم log2 لأن تعقيد الخوارزميات عادة يكون للاساس 2
        ratio_nlogn = T_large*1e6 / (n_large * np.log2(np.maximum(n_large, 1e-10)))

        score_n = np.std(ratio_n) / (np.mean(ratio_n) + 1e-10)
        score_nlogn = np.std(ratio_nlogn) / (np.mean(ratio_nlogn) + 1e-10)

        if score_n < score_nlogn:
            return "O(n)"
        else:
            return "O(n log n)"

    def generate_smooth_curve(self, func, min_size: int, max_size: int, popt: list, num_points: int = 200) -> list:
        x_smooth = np.linspace(min_size, max_size, num_points)
        y_smooth = func(x_smooth, *popt)
        return y_smooth.tolist()