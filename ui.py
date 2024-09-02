import tkinter as tk
from tkinter import ttk


class GameEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Editor")
        self.geometry("1400x800")
        self.configure(bg='#2e2e2e')  # Dark background

        self.create_toolbar()
        self.create_side_panels()
        self.create_canvas_area()

    def create_toolbar(self):
        toolbar = tk.Frame(self, bg='#3a3a3a', height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        new_scene_btn = tk.Button(toolbar, text="New Scene", bg='#555555', fg='white')
        new_scene_btn.pack(side=tk.LEFT, padx=2, pady=2)

        add_rect_btn = tk.Button(toolbar, text="Add Rectangle", bg='#555555', fg='white')
        add_rect_btn.pack(side=tk.LEFT, padx=2, pady=2)

        add_img_btn = tk.Button(toolbar, text="Add Image", bg='#555555', fg='white')
        add_img_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # More toolbar buttons can be added here

    def create_side_panels(self):
        # Left panel for Scene Management
        left_panel = tk.Frame(self, bg='#3a3a3a', width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        scenes_label = tk.Label(left_panel, text="Scenes", bg='#3a3a3a', fg='white')
        scenes_label.pack(padx=10, pady=10)

        scene_list = tk.Listbox(left_panel, bg='#4e4e4e', fg='white')
        scene_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        create_scene_btn = tk.Button(left_panel, text="Create Scene", bg='#555555', fg='white')
        create_scene_btn.pack(fill=tk.X, padx=10, pady=5)

        rename_scene_btn = tk.Button(left_panel, text="Rename Scene", bg='#555555', fg='white')
        rename_scene_btn.pack(fill=tk.X, padx=10, pady=5)

        delete_scene_btn = tk.Button(left_panel, text="Delete Scene", bg='#555555', fg='white')
        delete_scene_btn.pack(fill=tk.X, padx=10, pady=5)

        # Right panel for Object Properties
        right_panel = tk.Frame(self, bg='#3a3a3a', width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        properties_label = tk.Label(right_panel, text="Object Properties", bg='#3a3a3a', fg='white')
        properties_label.pack(padx=10, pady=10)

        property_tabs = ttk.Notebook(right_panel)
        basic_tab = tk.Frame(property_tabs, bg='#4e4e4e')
        advanced_tab = tk.Frame(property_tabs, bg='#4e4e4e')

        property_tabs.add(basic_tab, text="Basic")
        property_tabs.add(advanced_tab, text="Advanced")
        property_tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add widgets to basic_tab and advanced_tab as needed

    def create_canvas_area(self):
        canvas_frame = tk.Frame(self, bg='#2e2e2e')
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg='white', bd=0, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Example of adding a grid (optional)
        for i in range(0, 1400, 20):
            canvas.create_line(i, 0, i, 800, fill='#d3d3d3', stipple='gray25')
        for j in range(0, 800, 20):
            canvas.create_line(0, j, 1400, j, fill='#d3d3d3', stipple='gray25')


if __name__ == "__main__":
    app = GameEditorApp()
    app.mainloop()
