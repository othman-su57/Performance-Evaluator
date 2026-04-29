from os import name

import customtkinter as ctk



# 2. كلاس لوحة التحكم (الأزرار)
class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # هنا نضع الأزرار والقوائم المنسدلة
        self.analyze_btn = ctk.CTkButton(self, text="Run Analysis",command=self.handle_run)
        self.analyze_btn.pack(side="left", padx=10, pady=10)
        self.complexity_menu = ctk.CTkOptionMenu(self, values=["worst", "average", "best"])
        self.complexity_menu.pack(side="left", padx=10, pady=10)
        self.on_run = None


    def get_complexity(self):
        return self.complexity_menu.get()

    def handle_run(self):
        if self.on_run:
            self.on_run()