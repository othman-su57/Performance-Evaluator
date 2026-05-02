import customtkinter as ctk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

class CodeEditorPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.pack(fill="both", expand=True, padx=5, pady=5)

        self.lexer = PythonLexer()

        # تعريف الألوان
        self._setup_tags()

        # تحديث عند الكتابة
        self.textbox.bind("<KeyRelease>", self.highlight)

    def get_code(self):
        return self.textbox.get("1.0", "end-1c")

    def _setup_tags(self):
        self.textbox.tag_config("keyword", foreground="#ff79c6")
        self.textbox.tag_config("string", foreground="#f1fa8c")
        self.textbox.tag_config("comment", foreground="#6272a4")
        self.textbox.tag_config("number", foreground="#bd93f9")
        self.textbox.tag_config("name", foreground="#50fa7b")

    def highlight(self, event=None):
        code = self.get_code()

        # إزالة كل التلوين
        for tag in ["keyword", "string", "comment", "number", "name"]:
            self.textbox.tag_remove(tag, "1.0", "end")

        index = "1.0"

        for token, content in lex(code, self.lexer):
            length = len(content)

            if length == 0:
                continue

            end_index = f"{index}+{length}c"

            tag = self._map_token(token)
            if tag:
                self.textbox.tag_add(tag, index, end_index)

            index = end_index

    def _map_token(self, token):
        if token in Token.Keyword:
            return "keyword"
        elif token in Token.String:
            return "string"
        elif token in Token.Comment:
            return "comment"
        elif token in Token.Number:
            return "number"
        elif token in Token.Name:
            return "name"
        return None

# unit test
if __name__ == "__main__":
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.geometry("800x500")

    editor = CodeEditorPanel(app)
    editor.pack(fill="both", expand=True)

    # حقن كود تجريبي
    editor.textbox.insert("1.0", """def test():
    # comment
    x = 10
    print("hello")
""")

    app.after(100, editor.highlight)  # تشغيل التلوين بعد الإدخال

    app.mainloop()
