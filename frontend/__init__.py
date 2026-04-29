import customtkinter as ctk

from api import AlgorithmEvaluatorAPI
from frontend.controlpanel import ControlPanel
from frontend.edditor import EditorPanel
from frontend.resultpanel import ResultPanel


class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Complexity Analyzer")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")

        # إعداد الشبكة الرئيسية (Grid System)
        self.grid_rowconfigure(0, weight=1)  # الصف العلوي يأخذ المساحة الأكبر
        self.grid_rowconfigure(1, weight=0)  # الصف السفلي للوحة التحكم ثابت
        self.grid_columnconfigure(0, weight=1)  # عمود المحرر
        self.grid_columnconfigure(1, weight=1)  # عمود النتائج

        # استنساخ (Instantiation) اللوحات وتوزيعها
        self.editor_panel = EditorPanel(self)

        self.editor_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        self.result_panel = ResultPanel(self)
        self.result_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 0))

        self.control_panel = ControlPanel(self)
        self.control_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.control_panel.on_run = self.on_click
    def on_click(self):
        self.result_panel.display_results(self.handle_analysis())
    def handle_analysis(self):
    # 1. نسحب الكود من لوحة المحرر
        code = self.editor_panel.get_code()

    # 2. نسحب نوع التعقيد من لوحة التحكم (سنتعلم كيف نصل لها لاحقاً)
        complexity_type = self.control_panel.get_complexity()

    # 3. نرسل البيانات للمحرك (الذي عرفناه سابقاً كـ API)
        api = AlgorithmEvaluatorAPI()
        return  api.evaluate(
            source_code=code,
            test_sizes=[10, 100, 1000],
            complexity=complexity_type
        )


if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()