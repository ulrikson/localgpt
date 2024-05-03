import tkinter as tk
from tkinter import ttk
from claude import claude_completion
from open_ai import open_ai_completion

MODELS = [
    "llama3-8b",
    "gpt-4",
    "sonnet",
    "opus",
    "llama3-70b",
    "mixtral",
    "haiku",
    "gpt-3.5",
    "sonar",
]

TASKS = ["pm_assistant", "message_assistant", "email_assistant"]

LANGUAGES = ["english", "swedish"]


class TextEntry:
    def __init__(self, window, label_text, width, height):
        self.label = tk.Label(window, text=label_text)
        self.label.pack()
        self.entry = tk.Text(window, width=width, height=height)
        self.entry.pack(pady=(5, 10), padx=(25, 25))

    def get_text(self):
        return self.entry.get("1.0", tk.END).strip()

    def set_text(self, text):
        self.entry.delete("1.0", tk.END)
        self.entry.insert("1.0", text)

    def clear_text(self):
        self.entry.delete("1.0", tk.END)


class MainWindow:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Local GPT")

        # Instruction input
        self.instruction_entry = TextEntry(self.window, "Instruction:", 100, 2)
        self.input_entry = TextEntry(self.window, "Input Text:", 100, 5)

        # Create a frame to hold the comboboxes
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=(5, 10), padx=(25, 25))

        # Model selector
        self.model_selector = ttk.Combobox(input_frame, values=MODELS, width=10)
        self.model_selector.set(MODELS[0])
        self.model_selector.grid(row=0, column=0, padx=(0, 10))

        # Language selector
        self.language_selector = ttk.Combobox(input_frame, values=LANGUAGES, width=7)
        self.language_selector.set(LANGUAGES[0])
        self.language_selector.grid(row=0, column=1, padx=(0, 10))

        # Task selector
        self.task_selector = ttk.Combobox(input_frame, values=TASKS, width=14)
        self.task_selector.set(TASKS[0])
        self.task_selector.grid(row=0, column=2)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=(5, 10), padx=(25, 25))

        # Process button
        self.process_button = tk.Button(
            button_frame, text="Process", command=self.process_text
        )
        self.process_button.grid(
            row=0, column=0, padx=(0, 10)
        )  # Place in the left column

        # Copy button
        self.copy_button = tk.Button(button_frame, text="Copy", command=self.copy_text)
        self.copy_button.grid(
            row=0, column=1, padx=(0, 10)
        )  # Place in the middle column

        # Clear button
        self.clear_button = tk.Button(
            button_frame, text="Clear", command=self.clear_text
        )
        self.clear_button.grid(row=0, column=2)  # Place in the right column

        # Output text
        self.output_entry = TextEntry(self.window, "Output:", 100, 20)

    def process_text(self):
        instruction_text = self.instruction_entry.get_text()
        input_text = self.input_entry.get_text()

        selected_model = self.model_selector.get()
        completion_function = self.get_vendor(selected_model)

        task_name = self.task_selector.get()
        language = self.language_selector.get()
        output_text = completion_function(
            instruction_text, input_text, selected_model, task_name, language
        )

        self.output_entry.set_text(output_text)

    def get_vendor(self, model_name):
        if model_name in ["haiku", "sonnet", "opus"]:
            return claude_completion
        else:
            return open_ai_completion

    def clear_text(self):
        self.input_entry.clear_text()
        self.instruction_entry.clear_text()
        self.output_entry.clear_text()

    def copy_text(self):
        output_text = self.output_entry.get_text()
        copy_text = output_text.split("---")[0] # Remove the metadata

        self.output_entry.entry.clipboard_clear()
        self.output_entry.entry.clipboard_append(copy_text)

    def focus_next_widget(self, event, widget):
        widget.focus_set()


if __name__ == "__main__":
    app = MainWindow()
    app.window.mainloop()
