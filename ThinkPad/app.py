import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import json
import os

class ThinkPadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ThinkPad")
        self.notes = []
        self.load_notes()

        # Header
        header_frame = tk.Frame(self.root, bg="white")
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="ThinkPad", font=("Roboto", 24, "bold"), fg="gray20")
        title_label.pack(side=tk.LEFT)

        add_button = tk.Button(header_frame, text="+ Add Note", command=self.add_note, bg="#88C0D0", fg="white", font=("Roboto", 12), relief=tk.RAISED)
        add_button.pack(side=tk.RIGHT)

        # Notes Container with Scrollbar
        container_frame = tk.Frame(self.root, bg="gray90")
        container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container_frame, bg="gray90")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.notes_container = tk.Frame(canvas, bg="gray90")
        canvas.create_window((0, 0), window=self.notes_container, anchor="nw")

        # Refresh the notes view at startup
        self.refresh_notes()

    def add_note(self):
        self.open_note_modal(title="Add New Note", note_index=None)

    def open_note_modal(self, title, note_index):
        modal = tk.Toplevel(self.root)
        modal.title(title)
        modal.geometry("400x300")
        modal.grab_set()

        title_label = tk.Label(modal, text="Title", font=("Roboto", 12))
        title_label.pack(pady=5)
        title_entry = tk.Entry(modal, font=("Roboto", 12))
        title_entry.pack(fill=tk.X, padx=10, pady=5)

        content_label = tk.Label(modal, text="Content", font=("Roboto", 12))
        content_label.pack(pady=5)
        content_text = tk.Text(modal, font=("Roboto", 12), height=8)
        content_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        if note_index is not None:
            title_entry.insert(0, self.notes[note_index]["title"])
            content_text.insert("1.0", self.notes[note_index]["content"])

        def save_note():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if not title or not content:
                messagebox.showerror("Error", "Both Title and Content are required.")
                return

            if note_index is None:
                self.notes.append({"title": title, "content": content})
            else:
                self.notes[note_index] = {"title": title, "content": content}

            self.save_notes()
            self.refresh_notes()
            modal.destroy()

        save_button = tk.Button(modal, text="Save", command=save_note, bg="#88C0D0", fg="white", font=("Roboto", 12), relief=tk.RAISED)
        save_button.pack(pady=10)

    def refresh_notes(self):
        for widget in self.notes_container.winfo_children():
            widget.destroy()

        for index, note in enumerate(self.notes):
            note_frame = tk.Frame(self.notes_container, bg="white", bd=1, relief=tk.SOLID)
            note_frame.pack(fill=tk.X, pady=5)

            title_label = tk.Label(note_frame, text=note["title"], font=("Roboto", 14, "bold"), anchor="w", fg="gray20")
            title_label.pack(fill=tk.X, padx=10, pady=5)

            content_label = tk.Label(note_frame, text=note["content"], font=("Roboto", 12), anchor="w", fg="gray50")
            content_label.pack(fill=tk.X, padx=10, pady=5)

            actions_frame = tk.Frame(note_frame, bg="white")
            actions_frame.pack(fill=tk.X, pady=5)

            edit_button = tk.Button(actions_frame, text="Edit", command=lambda i=index: self.open_note_modal("Edit Note", i), bg="#88C0D0", fg="white", font=("Roboto", 10))
            edit_button.pack(side=tk.LEFT, padx=5)

            delete_button = tk.Button(actions_frame, text="Delete", command=lambda i=index: self.delete_note(i), bg="#BF616A", fg="white", font=("Roboto", 10))
            delete_button.pack(side=tk.RIGHT, padx=5)

    def delete_note(self, note_index):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this note?"):
            self.notes.pop(note_index)
            self.save_notes()
            self.refresh_notes()

    def save_notes(self):
        with open("thinkpad_notes.json", "w") as f:
            json.dump(self.notes, f)
            print("Notes saved successfully.")

    def load_notes(self):
        if os.path.exists("thinkpad_notes.json"):
            with open("thinkpad_notes.json", "r") as f:
                self.notes = json.load(f)
            print("Notes loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = ThinkPadApp(root)
    root.mainloop()
