import customtkinter as ctk
import ast
import json

from debuger import Debugger


class ManualModePanel(ctk.CTkFrame):
    def __init__(self, master, editor_textbox, **kwargs):
        super().__init__(master, **kwargs)

        self.editor_textbox = editor_textbox  # نحتاج المحرر لعمل تظليل (Highlight) للسطر
        self.history = []
        self.current_step = 0

        # --- شريط التحكم العلوي ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.top_bar, text="Input Array: ", font=("Arial", 14)).pack(side="left")
        self.array_input = ctk.CTkEntry(self.top_bar, width=150)
        self.array_input.pack(side="left", padx=10)
        self.array_input.insert(0, "[5, 3, 1, 4]")  # صيغة مصفوفة بايثون

        self.start_btn = ctk.CTkButton(self.top_bar, text="Start Debugging", command=self.start_debug)
        self.start_btn.pack(side="left", padx=10)

        # --- منطقة عرض البيانات ---
        self.display_frame = ctk.CTkFrame(self, corner_radius=10)
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.step_label = ctk.CTkLabel(self.display_frame, text="Step: 0 / 0 | Line: --", font=("Arial", 16, "bold"),
                                       text_color="#50fa7b")
        self.step_label.pack(pady=10)

        self.locals_textbox = ctk.CTkTextbox(self.display_frame, font=("Consolas", 14))
        self.locals_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # --- شريط التنقل السفلي ---
        self.bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_bar.pack(fill="x", padx=10, pady=10)

        self.prev_btn = ctk.CTkButton(self.bottom_bar, text="<< Prev", command=self.prev_step, state="disabled")
        self.prev_btn.pack(side="left", expand=True, padx=5)

        self.next_btn = ctk.CTkButton(self.bottom_bar, text="Next >>", command=self.next_step, state="disabled")
        self.next_btn.pack(side="right", expand=True, padx=5)

    def start_debug(self):
        source_code = self.editor_textbox.get("1.0", "end-1c")

        # تحويل النص المدخل إلى مصفوفة بايثون فعلية
        try:
            arr_input = ast.literal_eval(self.array_input.get())
            if not isinstance(arr_input, list):
                raise ValueError
        except Exception:
            self.locals_textbox.delete("1.0", "end")
            self.locals_textbox.insert("1.0", "Error: Invalid array format. Use [1, 2, 3]")
            return

        try:
            # تشغيل محرك الديباجر الخاص بك (تأكد من استدعاء كلاس Debugger هنا)
            debug_engine = Debugger(source_code)
            response = debug_engine.run(arr_input)

            # جلب البيانات كما برمجتها أنت في الـ Backend
            self.history = response["date"]
            self.current_step = 0

            # إعداد لون التظليل في المحرر
            self.editor_textbox.tag_config("highlight", background="#44475a")

            if self.history:
                self.update_ui()
            else:
                self.locals_textbox.insert("1.0", "No steps recorded.")

        except Exception as e:
            self.locals_textbox.delete("1.0", "end")
            self.locals_textbox.insert("1.0", f"Runtime Error:\n{str(e)}")

    def update_ui(self):
        if not self.history: return

        step_data = self.history[self.current_step]
        line_num = step_data["line"]
        func_name = step_data["function"]
        locals_dict = step_data["locals"]

        # 1. تحديث النصوص (رقم الخطوة، واسم الدالة)
        self.step_label.configure(
            text=f"Step: {self.current_step + 1} / {len(self.history)} | Func: {func_name} | Line: {line_num}")

        # 2. عرض المتغيرات المحلية بتنسيق JSON مرتب
        locals_str = json.dumps(locals_dict, indent=4, ensure_ascii=False)
        self.locals_textbox.delete("1.0", "end")
        self.locals_textbox.insert("1.0", f"Local Variables:\n{locals_str}")

        # 3. سحر تظليل السطر في المحرر وتتبعه (Auto-scroll)
        self.editor_textbox.tag_remove("highlight", "1.0", "end")
        self.editor_textbox.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
        self.editor_textbox.see(f"{line_num}.0")


        # 4. تفعيل وتعطيل الأزرار
        self.prev_btn.configure(state="normal" if self.current_step > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_step < len(self.history) - 1 else "disabled")

    def next_step(self):
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.update_ui()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui()