import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from manualdebugging import ManualModePanel

# تم تحويل الكلاس ليرث من CTkTabview بدلاً من CTkFrame
class AnalysisResultsPanel(ctk.CTkTabview):
    def __init__(self, master, editor_textbox=None, **kwargs):
        super().__init__(master, **kwargs)

        # 1. إنشاء التبويبات
        self.add("Dynamic Profiler")
        self.add("Manual Debugger")

        # ==========================================
        # محتويات التبويب الأول (Dynamic Profiler)
        # ==========================================
        dynamic_tab = self.tab("Dynamic Profiler")

        self.results_label = ctk.CTkLabel(dynamic_tab, text="Analysis Results", font=("Arial", 16, "bold"))
        self.results_label.pack(anchor="w", pady=(0, 5))

        self.complexity_label = ctk.CTkLabel(dynamic_tab, text="Detected Complexity: --", font=("Arial", 16))
        self.complexity_label.pack(anchor="w")

        self.confidence_label = ctk.CTkLabel(dynamic_tab, text="Confidence: --%", font=("Arial", 14))
        self.confidence_label.pack(anchor="w")

        self.chart_placeholder = ctk.CTkFrame(dynamic_tab, corner_radius=10)
        self.chart_placeholder.pack(fill="both", expand=True, pady=(10, 10))

        self._setup_matplotlib()

        # ==========================================
        # محتويات التبويب الثاني (Manual Debugger)
        # ==========================================
        manual_tab = self.tab("Manual Debugger")

        if editor_textbox:
            # دمج كلاس ManualModePanel الذي أرسلته لك سابقاً هنا
            self.manual_panel = ManualModePanel(manual_tab, editor_textbox=editor_textbox, fg_color="transparent")
            self.manual_panel.pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(manual_tab, text="Error: Please pass editor_textbox").pack(expand=True)

    def _setup_matplotlib(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.bg_color, self.fg_color = "#2b2b2b", "white"
        self.fig.patch.set_facecolor(self.bg_color)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.bg_color)

        # ضبط ألوان النصوص والمحاور لتناسب الـ Dark Mode
        self.ax.tick_params(colors=self.fg_color)
        self.ax.xaxis.label.set_color(self.fg_color)
        self.ax.yaxis.label.set_color(self.fg_color)
        self.ax.title.set_color(self.fg_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_placeholder)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_chart(self, sizes, actual_times, curve_y, complexity, confidence, case_name):
        self.complexity_label.configure(text=f"Detected Complexity: {complexity}")
        self.confidence_label.configure(text=f"Confidence: {confidence}%")

        self.ax.clear()

        # رسم البيانات بألوان واضحة
        self.ax.plot(sizes, actual_times, marker="o", linewidth=2, label="Measured Time", color="#50fa7b")

        if curve_y:
            curve_x = np.linspace(min(sizes), max(sizes), len(curve_y))
            self.ax.plot(curve_x, curve_y, linestyle="--", linewidth=2, label=f"Fitted {complexity}", color="#ff79c6")

        self.ax.set_xlabel("Input Size (n)")
        self.ax.set_ylabel("Time (seconds)")
        self.ax.set_title(f"{case_name.capitalize()} Case")

        # إصلاح لون نص الـ Legend ليظهر بوضوح
        legend = self.ax.legend()
        for text in legend.get_texts():
            text.set_color("black")

        self.ax.grid(True, linestyle=":", color="#6272a4", alpha=0.5)
        self.canvas.draw()