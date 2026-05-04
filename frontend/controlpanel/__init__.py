import customtkinter as ctk


class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, run_callback, case_change_callback, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.run_btn = ctk.CTkButton(self, text="Run Analysis", command=run_callback)
        self.run_btn.grid(row=0, column=0, padx=20, pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready", text_color="green")
        self.status_label.grid(row=0, column=1, sticky="w")

        self.case_selector = ctk.CTkSegmentedButton(
            self,
            values=["Sorted Case", "Random Case", "Reversed Case"],
            command=case_change_callback,
            state="disabled"
        )
        self.case_selector.set("Random Case")
        self.case_selector.grid(row=0, column=2, padx=20, pady=20)

    def set_status(self, text, color="white"):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def set_controls_state(self, state):
        self.run_btn.configure(state=state)
        self.case_selector.configure(state=state)