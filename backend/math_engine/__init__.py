import numpy as np
from scipy.optimize import curve_fit
import warnings
import math

class MathAnalyzer:
    def __init__(self):
        self.complexity_classes = {
            "O(1)"      : lambda x, a: a * np.ones_like(x),
            "O(n)"      : lambda x, a: a * x,
            "O(n log n)": lambda x, a: a * x * np.log(np.maximum(x, 1e-10)),
            "O(n^2)"    : lambda x, a: a * x ** 2,
            "O(n^3)"    : lambda x, a: a * x ** 3,
            "O(2^n)"    : lambda x, a: a * (2.0 ** np.minimum(x, 50)),
            "O(n!)"     : lambda x, a: a * math.factorial(np.minimum(x,10))
        }

    def analyze(self, sizes: list, times: list) -> dict:
        if len(sizes) < 3:
            return {
                "status": "error",
                "message": "Not enough data points"
            }

        x = np.array(sizes, dtype=float)
        y = np.array(times, dtype=float)



        best_fit = None
        best_error = float("inf")

        results_debug = {}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            for name, func in self.complexity_classes.items():
                try:
                    popt, _ = curve_fit(func, x, y, maxfev=5000)

                    y_pred = func(x, *popt)

                    # ✔ خطأ نسبي بدل MSE فقط
                    error = np.mean(((y - y_pred) / (y + 1e-10)) ** 2)

                    results_debug[name] = error

                    if error < best_error:
                        best_error = error
                        best_fit = name

                except Exception:
                    continue

        # ✔ حساب confidence منطقي
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
            "debug_errors": results_debug  # مهم جدًا للتطوير
        }