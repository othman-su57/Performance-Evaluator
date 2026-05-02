import threading
import customtkinter as ctk
from api import AlgorithmEvaluatorAPI
from frontend.controlpanel import ControlPanel
from frontend.edditor import CodeEditorPanel
from frontend.resultpanel import AnalysisResultsPanel


class PerformanceEvaluatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Performance Evaluator - Dashboard")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # 1. تهيئة المكونات (Components)
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.editor_panel = CodeEditorPanel(self.top_frame, fg_color="transparent")
        self.editor_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # التعديل الأخير هنا: تمرير المحرر (textbox) إلى لوحة النتائج (التي تحتوي على الـ Manual)
        self.results_panel = AnalysisResultsPanel(
            self.top_frame,
            editor_textbox=self.editor_panel.textbox,
            fg_color="transparent"
        )
        self.results_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # نمرر دوال الـ Callbacks للوحة التحكم
        self.control_panel = ControlPanel(
            self,
            run_callback=self.run_analysis,
            case_change_callback=self.on_case_change,
            height=80
        )
        self.control_panel.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.control_panel.grid_propagate(False)

        self.current_json_data = None
        self.api = AlgorithmEvaluatorAPI(0.5)

    # 2. إدارة الأحداث وتدفق البيانات
    def run_analysis(self):
        self.control_panel.set_status("Analyzing...", "orange")
        self.control_panel.set_controls_state("disabled")

        source_code = self.editor_panel.get_code()

        # تشغيل الخيط المعزول
        threading.Thread(target=self._evaluation_worker, args=(source_code,), daemon=True).start()

    def _evaluation_worker(self, source_code):
        result = self.api.evaluate(source_code)

        # العودة بأمان إلى خيط الواجهة الرئيسي
        self.after(
            0,
            lambda: self._on_analysis_complete(result)
        )

    def _on_analysis_complete(self, result_data):
        self.current_json_data = result_data
        self.control_panel.set_status("Analysis Complete", "green")
        self.control_panel.set_controls_state("normal")

        current_case = self.control_panel.case_selector.get().split()[0].lower()
        self.update_view(current_case)

    def on_case_change(self, selected_case):
        if self.current_json_data:
            case_name = selected_case.split()[0].lower()
            self.update_view(case_name)

    def update_view(self, case_name):
        dynamic_data = self.current_json_data["dynamic_analysis"]
        estimation = dynamic_data["complexity_estimation"][case_name]
        raw_plot = dynamic_data["raw_plot_data"][case_name]

        sizes = [point[0] for point in reversed(raw_plot)]
        actual_times = [point[1] for point in reversed(raw_plot)]
        curve_y = list(reversed(estimation["curve_data"]))

        self.results_panel.update_chart(
            sizes=sizes,
            actual_times=actual_times,
            curve_y=curve_y,
            complexity=estimation["detected_complexity"],
            confidence=estimation["confidence_percentage"],
            case_name=case_name
        )


if __name__ == "__main__":
    app = PerformanceEvaluatorApp()
    app.mainloop()