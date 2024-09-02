import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw

class TkinterCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.image_objects = []
        self.canvas_image = None
        self.drag_data = {'object': None, 'start_x': 0, 'start_y': 0}
        self.collision_detection_enabled = False
        self.selected_object = None

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Button-3>", self.on_right_click)  # Right click for gizmo

    def add_image(self, image_path, x, y, width, height):
        try:
            image = Image.open(image_path).resize((width, height))
            image_obj = {
                'type': 'image',
                'image_path': image_path,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'image': ImageTk.PhotoImage(image)
            }
            self.image_objects.append(image_obj)
            self.draw_objects()
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Failed to load image: {e}")

    def draw_objects(self):
        self.delete("all")
        self.canvas_image = Image.new("RGB", (1400, 600), color="white")
        draw = ImageDraw.Draw(self.canvas_image)

        for obj in self.image_objects:
            if obj['type'] == 'rect':
                draw.rectangle([obj['x'], obj['y'], obj['x'] + obj['width'], obj['y'] + obj['height']], fill=obj['color'])
            elif obj['type'] == 'image':
                self.canvas_image.paste(obj['image'].convert("RGB"), (obj['x'], obj['y']))

        self.tk_image = ImageTk.PhotoImage(self.canvas_image)
        self.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        if self.selected_object:
            self.draw_gizmo()

        if self.collision_detection_enabled:
            self.check_collisions()

    def draw_gizmo(self):
        obj = self.selected_object
        if obj['type'] == 'rect':
            x, y, width, height = obj['x'], obj['y'], obj['width'], obj['height']
            self.create_rectangle(x - 5, y - 5, x + width + 5, y + height + 5, outline='blue', width=2)
            self.create_rectangle(x - 10, y - 10, x - 5, y - 5, fill='blue', outline='blue', tags='gizmo')
            self.create_rectangle(x + width + 5, y - 10, x + width + 10, y - 5, fill='blue', outline='blue', tags='gizmo')
            self.create_rectangle(x - 10, y + height + 5, x - 5, y + height + 10, fill='blue', outline='blue', tags='gizmo')
            self.create_rectangle(x + width + 5, y + height + 5, x + width + 10, y + height + 10, fill='blue', outline='blue', tags='gizmo')

    def on_click(self, event):
        self.drag_data['object'] = None
        self.selected_object = None
        for obj in self.image_objects:
            if obj['type'] == 'rect' or obj['type'] == 'image':
                if obj['x'] <= event.x <= obj['x'] + obj['width'] and obj['y'] <= event.y <= obj['y'] + obj['height']:
                    self.drag_data['object'] = obj
                    self.drag_data['start_x'] = event.x
                    self.drag_data['start_y'] = event.y
                    self.master.select_object(obj)
                    self.selected_object = obj
                    break

    def on_drag(self, event):
        obj = self.drag_data['object']
        if obj:
            dx = event.x - self.drag_data['start_x']
            dy = event.y - self.drag_data['start_y']
            obj['x'] += dx
            obj['y'] += dy
            self.drag_data['start_x'] = event.x
            self.drag_data['start_y'] = event.y
            self.draw_objects()

    def on_release(self, event):
        self.drag_data['object'] = None
        self.drag_data['start_x'] = 0
        self.drag_data['start_y'] = 0

    def on_right_click(self, event):
        obj = self.selected_object
        if obj:
            x, y = event.x, event.y
            # Check if the right-click was on one of the gizmo handles
            if (obj['x'] - 10 <= x <= obj['x'] - 5 and obj['y'] - 10 <= y <= obj['y'] - 5) or \
               (obj['x'] + obj['width'] + 5 <= x <= obj['x'] + obj['width'] + 10 and obj['y'] - 10 <= y <= obj['y'] - 5) or \
               (obj['x'] - 10 <= x <= obj['x'] - 5 and obj['y'] + obj['height'] + 5 <= y <= obj['y'] + obj['height'] + 10) or \
               (obj['x'] + obj['width'] + 5 <= x <= obj['x'] + obj['width'] + 10 and obj['y'] + obj['height'] + 5 <= y <= obj['y'] + obj['height'] + 10):
                # Handle resizing or rotation here
                pass
            else:
                self.draw_gizmo()

    def check_collisions(self):
        colliding_pairs = []
        for i, obj1 in enumerate(self.image_objects):
            for obj2 in self.image_objects[i+1:]:
                if self.is_colliding(obj1, obj2):
                    colliding_pairs.append((obj1, obj2))

        self.highlight_collisions(colliding_pairs)

    def is_colliding(self, obj1, obj2):
        if obj1['type'] == 'rect' and obj2['type'] == 'rect':
            return (obj1['x'] < obj2['x'] + obj2['width'] and
                    obj1['x'] + obj1['width'] > obj2['x'] and
                    obj1['y'] < obj2['y'] + obj2['height'] and
                    obj1['y'] + obj1['height'] > obj2['y'])
        return False

    def highlight_collisions(self, colliding_pairs):
        for obj1, obj2 in colliding_pairs:
            self.create_rectangle(obj1['x'], obj1['y'],
                                  obj1['x'] + obj1['width'],
                                  obj1['y'] + obj1['height'],
                                  outline='red', width=2)
            self.create_rectangle(obj2['x'], obj2['y'],
                                  obj2['x'] + obj2['width'],
                                  obj2['y'] + obj2['height'],
                                  outline='red', width=2)

class GameEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Editor")
        self.geometry("1200x800")

        self.selected_object = None
        self.scenes = {}
        self.current_scene = None

        self.create_ui()

    def create_ui(self):
        self.create_panels()
        self.center_canvas()

    def create_panels(self):
        self.scene_manager_frame = tk.Frame(self, bg='#f0f0f0')
        self.scene_manager_frame.grid(row=0, column=0, sticky='ns', padx=10, pady=10)
        self.object_properties_frame = tk.Frame(self, bg='#e0e0e0')
        self.object_properties_frame.grid(row=0, column=2, sticky='ns', padx=10, pady=10)
        self.object_hierarchy_frame = tk.Frame(self, bg='#f0f0f0')
        self.object_hierarchy_frame.grid(row=0, column=3, sticky='ns', padx=10, pady=10)

        tk.Label(self.scene_manager_frame, text="Scenes", bg='#f0f0f0').pack(pady=10)
        self.scene_listbox = tk.Listbox(self.scene_manager_frame)
        self.scene_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.scene_listbox.bind("<ButtonRelease-1>", self.select_scene)

        self.create_scene_button = tk.Button(self.scene_manager_frame, text="Create Scene", command=self.create_scene)
        self.create_scene_button.pack(pady=5)
        self.rename_scene_button = tk.Button(self.scene_manager_frame, text="Rename Scene", command=self.rename_scene)
        self.rename_scene_button.pack(pady=5)
        self.delete_scene_button = tk.Button(self.scene_manager_frame, text="Delete Scene", command=self.delete_scene)
        self.delete_scene_button.pack(pady=5)

        tk.Label(self.object_properties_frame, text="Object Properties", bg='#e0e0e0').pack(pady=10)
        tk.Label(self.object_properties_frame, text="Name").pack(pady=5)
        self.object_name_entry = tk.Entry(self.object_properties_frame)
        self.object_name_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="X Position").pack(pady=5)
        self.object_x_entry = tk.Entry(self.object_properties_frame)
        self.object_x_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="Y Position").pack(pady=5)
        self.object_y_entry = tk.Entry(self.object_properties_frame)
        self.object_y_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="Width").pack(pady=5)
        self.object_width_entry = tk.Entry(self.object_properties_frame)
        self.object_width_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="Height").pack(pady=5)
        self.object_height_entry = tk.Entry(self.object_properties_frame)
        self.object_height_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="Speed").pack(pady=5)
        self.object_speed_entry = tk.Entry(self.object_properties_frame)
        self.object_speed_entry.pack(pady=5)
        tk.Label(self.object_properties_frame, text="Color").pack(pady=5)
        self.color_button = tk.Button(self.object_properties_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(pady=5)

        tk.Label(self.object_hierarchy_frame, text="Object Hierarchy", bg='#f0f0f0').pack(pady=10)
        self.object_listbox = tk.Listbox(self.object_hierarchy_frame)
        self.object_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.add_object_button = tk.Button(self, text="Add Object", command=self.add_object)
        self.add_object_button.grid(row=1, column=1, pady=10, sticky='ew')

    def center_canvas(self):
        self.tk_canvas = TkinterCanvas(self)
        self.tk_canvas.grid(row=0, column=1, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

    def add_object(self):
        obj_type = simpledialog.askstring("Object Type", "Enter the type of the object (rect or image):")
        if not obj_type:
            return
        if obj_type == 'rect':
            x = simpledialog.askinteger("Object X Position", "Enter the X position:", minvalue=0)
            y = simpledialog.askinteger("Object Y Position", "Enter the Y position:", minvalue=0)
            width = simpledialog.askinteger("Object Width", "Enter the width:", minvalue=1)
            height = simpledialog.askinteger("Object Height", "Enter the height:", minvalue=1)
            color = colorchooser.askcolor(title="Choose Color")[1]
            new_obj = {
                'type': 'rect',
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'color': color or '#0000FF'
            }
            self.tk_canvas.image_objects.append(new_obj)
            if self.current_scene:
                self.scenes[self.current_scene] = self.tk_canvas.image_objects.copy()
            self.tk_canvas.draw_objects()
            self.update_object_hierarchy()
        elif obj_type == 'image':
            image_path = simpledialog.askstring("Image Path", "Enter the path to the image:")
            x = simpledialog.askinteger("Image X Position", "Enter the X position:", minvalue=0)
            y = simpledialog.askinteger("Image Y Position", "Enter the Y position:", minvalue=0)
            width = simpledialog.askinteger("Image Width", "Enter the width:", minvalue=1)
            height = simpledialog.askinteger("Image Height", "Enter the height:", minvalue=1)
            self.tk_canvas.add_image(image_path, x, y, width, height)
            if self.current_scene:
                self.scenes[self.current_scene] = self.tk_canvas.image_objects.copy()
            self.tk_canvas.draw_objects()
            self.update_object_hierarchy()

    def update_object_hierarchy(self):
        self.object_listbox.delete(0, tk.END)
        if self.current_scene:
            for obj in self.scenes.get(self.current_scene, []):
                obj_desc = f"{obj.get('type', 'unknown')} at ({obj['x']}, {obj['y']})"
                self.object_listbox.insert(tk.END, obj_desc)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.color_button.config(bg=color)

    def select_object(self, obj):
        self.selected_object = obj
        self.object_name_entry.delete(0, tk.END)
        self.object_name_entry.insert(0, obj.get('name', ''))
        self.object_x_entry.delete(0, tk.END)
        self.object_x_entry.insert(0, obj.get('x', ''))
        self.object_y_entry.delete(0, tk.END)
        self.object_y_entry.insert(0, obj.get('y', ''))
        self.object_width_entry.delete(0, tk.END)
        self.object_width_entry.insert(0, obj.get('width', ''))
        self.object_height_entry.delete(0, tk.END)
        self.object_height_entry.insert(0, obj.get('height', ''))
        self.object_speed_entry.delete(0, tk.END)
        self.object_speed_entry.insert(0, obj.get('speed', ''))
        self.color_button.config(bg=obj.get('color', '#0000FF'))

    def toggle_collision_detection(self):
        self.tk_canvas.collision_detection_enabled = not self.tk_canvas.collision_detection_enabled
        self.tk_canvas.draw_objects()

    def create_scene(self):
        scene_name = simpledialog.askstring("Create Scene", "Enter scene name:")
        if scene_name and scene_name not in self.scenes:
            self.scenes[scene_name] = []
            self.current_scene = scene_name
            self.scene_listbox.insert(tk.END, scene_name)
            self.select_scene(None)  # Refresh to show new scene objects

    def rename_scene(self):
        if not self.current_scene:
            messagebox.showwarning("No Scene Selected", "No scene is currently selected.")
            return
        new_name = simpledialog.askstring("Rename Scene", "Enter new scene name:")
        if new_name and new_name not in self.scenes:
            self.scenes[new_name] = self.scenes.pop(self.current_scene)
            self.current_scene = new_name
            self.scene_listbox.delete(0, tk.END)
            for scene in self.scenes.keys():
                self.scene_listbox.insert(tk.END, scene)
            self.select_scene(None)  # Refresh to show new scene objects

    def delete_scene(self):
        if not self.current_scene:
            messagebox.showwarning("No Scene Selected", "No scene is currently selected.")
            return
        if messagebox.askyesno("Delete Scene", f"Are you sure you want to delete the scene '{self.current_scene}'?"):
            del self.scenes[self.current_scene]
            self.scene_listbox.delete(self.scene_listbox.curselection())
            self.current_scene = None
            self.tk_canvas.image_objects = []
            self.tk_canvas.draw_objects()
            self.update_object_hierarchy()

    def select_scene(self, event):
        selected_index = self.scene_listbox.curselection()
        if selected_index:
            scene_name = self.scene_listbox.get(selected_index)
            self.current_scene = scene_name
            self.tk_canvas.image_objects = self.scenes.get(scene_name, []).copy()
            self.tk_canvas.draw_objects()
            self.update_object_hierarchy()

if __name__ == "__main__":
    app = GameEditorApp()
    app.mainloop()
