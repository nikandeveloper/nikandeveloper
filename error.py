import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import io
import contextlib
import sys

# Initialize scenes and current scene
scenes = {'Default': {'objects': [], 'scripts': []}}
current_scene_name = 'Default'

# Main Application Class
class GameEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Editor")
        self.geometry("1200x800")
        
        # Create frames for different panels
        self.create_panels()
        self.update_scene_list()

    def create_panels(self):
        # Left panel for Scene Management
        self.scene_manager_frame = tk.Frame(self, width=200, bg='#f0f0f0')
        self.scene_manager_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.scene_manager_frame, text="Scenes", bg='#f0f0f0').pack(pady=10)
        self.scene_listbox = tk.Listbox(self.scene_manager_frame)
        self.scene_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.scene_listbox.bind("<Button-3>", self.show_scene_context_menu)
        
        self.create_scene_button = tk.Button(self.scene_manager_frame, text="Create Scene", command=self.create_scene)
        self.create_scene_button.pack(pady=5)

        self.rename_scene_button = tk.Button(self.scene_manager_frame, text="Rename Scene", command=self.rename_scene)
        self.rename_scene_button.pack(pady=5)

        self.delete_scene_button = tk.Button(self.scene_manager_frame, text="Delete Scene", command=self.delete_scene)
        self.delete_scene_button.pack(pady=5)
        
        # Right panel for Object Properties
        self.object_properties_frame = tk.Frame(self, width=300, bg='#e0e0e0')
        self.object_properties_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.object_properties_frame, text="Object Properties", bg='#e0e0e0').pack(pady=10)
        self.object_name_entry = tk.Entry(self.object_properties_frame)
        tk.Label(self.object_properties_frame, text="Name").pack()
        self.object_name_entry.pack(padx=10, pady=5)

        self.object_x_entry = tk.Entry(self.object_properties_frame)
        tk.Label(self.object_properties_frame, text="X").pack()
        self.object_x_entry.pack(padx=10, pady=5)

        self.object_y_entry = tk.Entry(self.object_properties_frame)
        tk.Label(self.object_properties_frame, text="Y").pack()
        self.object_y_entry.pack(padx=10, pady=5)

        self.object_speed_entry = tk.Entry(self.object_properties_frame)
        tk.Label(self.object_properties_frame, text="Speed").pack()
        self.object_speed_entry.pack(padx=10, pady=5)

        self.delete_object_button = tk.Button(self.object_properties_frame, text="Delete Object", command=self.delete_object)
        self.delete_object_button.pack(pady=10)

        # Center panel for Script Editor and Main Canvas
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.script_editor = tk.Toplevel(self)
        self.script_editor.title("Script Editor")
        self.script_editor.geometry("600x400")

        self.editor_text = scrolledtext.ScrolledText(self.script_editor, wrap=tk.WORD)
        self.editor_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.run_script_button = tk.Button(self.script_editor, text="Run Script", command=self.run_script)
        self.run_script_button.pack(pady=5)

        self.script_output = tk.Text(self.script_editor, height=10)
        self.script_output.pack(fill=tk.BOTH, padx=10, pady=10)

    def update_scene_list(self):
        self.scene_listbox.delete(0, tk.END)
        for scene_name in scenes.keys():
            self.scene_listbox.insert(tk.END, scene_name)

    def show_scene_context_menu(self, event):
        try:
            index = self.scene_listbox.curselection()[0]
            scene_name = self.scene_listbox.get(index)
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Add Object", command=lambda: self.add_object_to_scene(scene_name))
            context_menu.add_command(label="Add Script", command=lambda: self.add_script_to_scene(scene_name))
            context_menu.post(event.x_root, event.y_root)
        except IndexError:
            pass

    def create_scene(self):
        new_name = simpledialog.askstring("Create Scene", "Enter new scene name:")
        if new_name:
            if new_name not in scenes:
                scenes[new_name] = {'objects': [], 'scripts': []}
                self.update_scene_list()
                messagebox.showinfo("Success", f"Scene '{new_name}' created.")
            else:
                messagebox.showerror("Error", "Scene already exists.")

    def rename_scene(self):
        old_name = simpledialog.askstring("Rename Scene", "Enter current scene name:")
        if old_name and old_name in scenes:
            new_name = simpledialog.askstring("Rename Scene", "Enter new scene name:")
            if new_name:
                if new_name not in scenes:
                    scenes[new_name] = scenes.pop(old_name)
                    self.update_scene_list()
                    messagebox.showinfo("Success", f"Scene renamed to '{new_name}'.")
                else:
                    messagebox.showerror("Error", "Scene with this name already exists.")
        else:
            messagebox.showerror("Error", "Scene not found.")

    def delete_scene(self):
        name = simpledialog.askstring("Delete Scene", "Enter scene name to delete:")
        if name and name in scenes:
            if len(scenes) > 1:
                del scenes[name]
                self.update_scene_list()
                messagebox.showinfo("Success", f"Scene '{name}' deleted.")
            else:
                messagebox.showerror("Error", "Cannot delete the last scene.")
        else:
            messagebox.showerror("Error", "Scene not found.")

    def add_object_to_scene(self, scene_name):
        # Add object to the selected scene
        pass

    def add_script_to_scene(self, scene_name):
        # Add script to the selected scene
        pass

    def delete_object(self):
        # Delete selected object from current scene
        pass

    def run_script(self):
        script = self.editor_text.get("1.0", tk.END)
        # Execute the script and display output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(script)
            except Exception as e:
                print(f"Error: {e}")
        self.script_output.delete("1.0", tk.END)
        self.script_output.insert(tk.END, output.getvalue())

if __name__ == "__main__":
    app = GameEditorApp()
    app.mainloop()
