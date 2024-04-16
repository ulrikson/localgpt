import tkinter as tk
from tkinter import ttk
from chatgpt import chatgpt_completion
from claude import claude_completion
from perplexity import perplexity_completion


MODELS = ["gpt-4", "haiku", "sonar", "mistral", "mixtral", "codellama"]
DEFAULT_MODEL = "gpt-4"

TASKS = ["message_assistant", "pm_assistant"]
DEFAULT_TASK = "message_assistant"


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
        combobox_frame = tk.Frame(self.window)
        combobox_frame.pack(pady=(5, 10), padx=(25, 25))

        # Model selector
        self.model_selector = ttk.Combobox(combobox_frame, values=MODELS)
        self.model_selector.set(DEFAULT_MODEL)  # Set the default value
        self.model_selector.grid(row=0, column=0, padx=(0, 10))  # Place in the left column

        # Task selector
        self.task_selector = ttk.Combobox(combobox_frame, values=TASKS)
        self.task_selector.set(DEFAULT_TASK)  # Set the default value
        self.task_selector.grid(row=0, column=1)  # Place in the right column

        # Process button
        self.process_button = tk.Button(
            self.window, text="Process", command=self.process_text
        )
        self.process_button.pack(pady=(5, 5), padx=(25, 25))

        # Copy button
        self.copy_button = tk.Button(self.window, text="Copy", command=self.copy_text)
        self.copy_button.pack(pady=(5, 5), padx=(25, 25))

        # Output text
        self.output_entry = TextEntry(self.window, "Output:", 100, 20)

        # Clear button
        self.clear_button = tk.Button(
            self.window, text="Clear", command=self.clear_text
        )
        self.clear_button.pack(pady=(5, 25), padx=(25, 25))

    def process_text(self):
        instruction_text = self.instruction_entry.get_text()
        input_text = self.input_entry.get_text()

        model_functions = {
            "haiku": claude_completion,
            "sonar": perplexity_completion,
            "mistral": perplexity_completion,
            "codellama": perplexity_completion,
            "mixtral": perplexity_completion,
            "gpt-4": chatgpt_completion,
        }

        selected_model = self.model_selector.get()
        completion_function = model_functions.get(
            selected_model, "Model not supported..."
        )

        task_name = self.task_selector.get()
        output_text = completion_function(instruction_text, input_text, selected_model, task_name)

        self.output_entry.set_text(output_text)

    def clear_text(self):
        self.input_entry.clear_text()
        self.instruction_entry.clear_text()
        self.output_entry.clear_text()

    def copy_text(self):
        output_text = self.output_entry.get_text()
        self.output_entry.entry.clipboard_clear()
        self.output_entry.entry.clipboard_append(output_text)

    def focus_next_widget(self, event, widget):
        widget.focus_set()


if __name__ == "__main__":
    app = MainWindow()
    app.window.mainloop()
