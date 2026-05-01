import random


class DataGenerator:
    @staticmethod
    def generate(size: int) -> dict:
        # -------- Lists --------
        best_case = list(range(1, size + 1))
        worst_case = list(range(size, 0, -1))

        average_case = best_case.copy()
        random.shuffle(average_case)

        # -------- Targets --------
        best_target = best_case[0]  # موجود في البداية

        average_target = average_case[random.randint(0, size - 1)]

        worst_target = -1  # غير موجود → worst case حقيقي

        return {
            "best": {
                "list": best_case,
                "target": best_target
            },
            "avarage": {
                "list": average_case,
                "target": average_target
            },
            "worst": {
                "list": worst_case,
                "target": worst_target
            }
        }