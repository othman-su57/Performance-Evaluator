import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ResultPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # تقسيم رأسي
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)

        # -------- معلومات --------
        self.info_box = ctk.CTkTextbox(self, height=120)
        self.info_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        # -------- رسم --------
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.canvas = None

    def display_results(self, result: dict):
        self.info_box.delete("1.0", "end")

        if result["status"] != "success":
            self.info_box.insert("1.0", result.get("message", "Error"))
            return

        # -------- معلومات --------
        func_name = result["metadata"]["function_name"]

        static = result.get("static_analysis", {})
        dynamic = result.get("dynamic_analysis", {})

        complexity = dynamic.get("complexity_estimation", {})

        text = f"""
Function: {func_name}

--- Static Analysis ---
Loops: {static.get("loops", {}).get("count")}
Max Depth: {static.get("loops", {}).get("max_depth")}
Recursive: {static.get("recursion", {}).get("is_recursive")}

--- Dynamic Analysis ---
Detected: {complexity.get("detected_complexity")}
Confidence: {complexity.get("confidence_percentage")}%
"""

        self.info_box.insert("1.0", text)

        # -------- رسم --------
        raw_data = dynamic.get("raw_plot_data", {})
        self._draw_graph(raw_data)

    def _draw_graph(self, data):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots()

        colors = {
            "best": "green",
            "average": "blue",
            "worst": "red"
        }

        for key, points in data.items():
            x = [p[0] for p in points if p[1] is not None]
            y = [p[1] for p in points if p[1] is not None]

            if x and y:
                ax.plot(x, y, label=key, color=colors.get(key))

        ax.set_title("Performance Analysis")
        ax.set_xlabel("Input Size")
        ax.set_ylabel("Time")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)