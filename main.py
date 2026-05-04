import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from api import AlgorithmEvaluatorAPI


class PerformanceEvaluatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Performance Evaluator - Dashboard")
        self.geometry("1100x700")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # =========================
        # Main Grid
        # =========================
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # =========================
        # Top Frame
        # =========================
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(10, 5)
        )

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # =========================
        # Code Editor
        # =========================
        self.editor_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color="transparent"
        )

        self.editor_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.editor_label = ctk.CTkLabel(
            self.editor_frame,
            text="Code Editor",
            font=("Arial", 16, "bold")
        )

        self.editor_label.pack(
            anchor="w",
            pady=(0, 5)
        )

        self.code_textbox = ctk.CTkTextbox(
            self.editor_frame,
            font=("Consolas", 14)
        )

        self.code_textbox.pack(
            fill="both",
            expand=True
        )

        self.code_textbox.insert(
            "0.0",
            "def test_function(arr):\n    pass"
        )

        # =========================
        # Results Panel
        # =========================
        self.results_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color="transparent"
        )

        self.results_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Analysis Results",
            font=("Arial", 16, "bold")
        )

        self.results_label.pack(
            anchor="w",
            pady=(0, 5)
        )

        self.chart_placeholder = ctk.CTkFrame(
            self.results_frame,
            corner_radius=10
        )

        self.chart_placeholder.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

        self.complexity_label = ctk.CTkLabel(
            self.results_frame,
            text="Detected Complexity: --",
            font=("Arial", 16)
        )

        self.complexity_label.pack(anchor="w")

        self.confidence_label = ctk.CTkLabel(
            self.results_frame,
            text="Confidence: --%",
            font=("Arial", 14)
        )

        self.confidence_label.pack(anchor="w")

        self.setup_matplotlib()

        # =========================
        # Bottom Frame
        # =========================
        self.bottom_frame = ctk.CTkFrame(
            self,
            height=80
        )

        self.bottom_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 10)
        )

        self.bottom_frame.grid_propagate(False)

        self.run_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Run Analysis",
            command=self.run_analysis
        )

        self.run_btn.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        self.status_label = ctk.CTkLabel(
            self.bottom_frame,
            text="Status: Ready",
            text_color="green"
        )

        self.status_label.grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.case_selector = ctk.CTkSegmentedButton(
            self.bottom_frame,
            values=[
                "Best Case",
                "Avarage Case",
                "Worst Case"
            ],
            command=self.on_case_change,
            state="disabled"
        )

        self.case_selector.set("Avarage Case")

        self.case_selector.grid(
            row=0,
            column=2,
            padx=20,
            pady=20
        )

        self.current_json_data = None

    # =========================
    # Matplotlib Setup
    # =========================
    def setup_matplotlib(self):

        self.fig = Figure(
            figsize=(5, 4),
            dpi=100
        )

        self.bg_color = "#2b2b2b"
        self.fg_color = "white"

        self.fig.patch.set_facecolor(
            self.bg_color
        )

        self.ax = self.fig.add_subplot(111)

        self.ax.set_facecolor(
            self.bg_color
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.chart_placeholder
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # =========================
    # Events
    # =========================
    def run_analysis(self):

        self.status_label.configure(
            text="Status: Analyzing...",
            text_color="orange"
        )

        self.update()

        source_code = self.code_textbox.get(
            "1.0",
            "end"
        )

        threading.Thread(target=self.evaluation,args=(source_code,),daemon=True)

        self.status_label.configure(
            text="Status: Analysis Complete",
            text_color="green"
        )

        self.case_selector.configure(
            state="normal"
        )

        current_case = self.case_selector.get().split()[0].lower()

        self.update_view(current_case)

    def on_case_change(self, selected_case):

        if self.current_json_data:
            case_name = selected_case.split()[0].lower()
            self.update_view(case_name)

    def update_view(self, case_name):

        dynamic_data = self.current_json_data[
            "dynamic_analysis"
        ]

        estimation = dynamic_data[
            "complexity_estimation"
        ][case_name]

        raw_plot = dynamic_data[
            "raw_plot_data"
        ][case_name]

        complexity = estimation[
            "detected_complexity"
        ]

        confidence = estimation[
            "confidence_percentage"
        ]

        curve_y = list(
            reversed(
                estimation["curve_data"]
            )
        )
        sizes = [
            point[0]
            for point in reversed(raw_plot)
        ]

        actual_times = [
            point[1]
            for point in reversed(raw_plot)
        ]

        self.complexity_label.configure(
            text=f"Detected Complexity: {complexity}"
        )

        self.confidence_label.configure(
            text=f"Confidence: {confidence}%"
        )

        self.ax.clear()

        # measured data
        self.ax.plot(
            sizes,
            actual_times,
            marker="o",
            linewidth=2,
            label="Measured Time"
        )

        # fitted curve
        if curve_y:

            curve_x = np.linspace(
                min(sizes),
                max(sizes),
                len(curve_y)
            )

            self.ax.plot(
                curve_x,
                curve_y,
                linestyle="--",
                linewidth=2,
                label=f"Fitted {complexity}"
            )

        self.ax.set_xlabel(
            "Input Size (n)"
        )

        self.ax.set_ylabel(
            "Time (seconds)"
        )

        self.ax.set_title(
            f"{case_name.capitalize()} Case"
        )

        self.ax.legend()

        self.ax.grid(
            True,
            linestyle=":"
        )

        self.canvas.draw()

    def evaluation(self,source_code):
        self.current_json_data=AlgorithmEvaluatorAPI(
            0.5
        ).evaluate(source_code)
if __name__ == "__main__":
    def insertion_sort(arr):
        for i in range(1, len(arr)):
            for j in range(1, len(arr)):
                for k in range(1, len(arr)):
                    print("hallo")
        return arr
    insertion_sort([1,2,3,4,5,6])