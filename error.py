import tkinter as tk
from tkinter import colorchooser, messagebox, scrolledtext, filedialog, simpledialog
from PIL import Image, ImageTk
import pygame
import pygame.surfarray
import numpy as np
import traceback

class PygameCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize Pygame
        pygame.init()
        self.surface = pygame.Surface((1400, 600))  # Use a surface to draw objects
        self.objects = []
        self.dragging_object = None  # Track the object being dragged
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def add_image(self, image_path, x, y, width, height):
        try:
            # Load and scale the image
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (width, height))

            # Store image information
            img_dict = {
                'type': 'image',
                'image_path': image_path,  # Corrected from 'path'
                'x': x,
                'y': y,
                'width': width,
                'height': height
            }
            # Remove previous image of the same name if it exists
            self.objects = [obj for obj in self.objects if not (obj['type'] == 'image' and obj['image_path'] == image_path)]
            self.objects.append(img_dict)

            # Redraw objects
            self.draw_objects(self.objects)
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Failed to load image: {e}")

    def draw_objects(self, objects):
        self.objects = objects
        self.surface.fill((255, 255, 255))  # Clear the surface with white background

        for obj in objects:
            obj_type = obj.get('type', 'rect')
            color = pygame.Color(obj.get('color', '#0000FF'))  # Default color if not set
            x, y, width, height = obj['x'], obj['y'], obj['width'], obj['height']

            if obj_type == 'rect':
                pygame.draw.rect(self.surface, color, pygame.Rect(x, y, width, height))

            elif obj_type == 'image':  # Corrected from `if obj_type == 'image':`
                image_path = obj.get('image_path')
                if image_path:
                    try:
                        image = pygame.image.load(image_path)
                        image = pygame.transform.scale(image, (width, height))  # Scale image to object size
                        self.surface.blit(image, (x, y))  # Draw image on surface
                        print(f"Rendering image from {image_path} at ({x}, {y}) with size ({width}, {height})")
                    except pygame.error as e:
                        print(f"Error loading image from {image_path}: {e}")
                else:
                    print(f"No image path provided for object: {obj.get('name')}")

            else:
                print(f"Unknown object type: {obj_type}")

        self.pygame_to_tk()

    def update_object(self, updated_object):
        for obj in self.objects:
            if obj['name'] == updated_object['name']:
                obj.update(updated_object)
                break
        self.draw_objects(self.objects)

    def rotate_and_scale_image(self, image_path, angle, scale):
        try:
            image = pygame.image.load(image_path)
            width, height = image.get_size()
            scaled_size = (int(width * scale), int(height * scale))
            image = pygame.transform.scale(image, scaled_size)
            rotated_image = pygame.transform.rotate(image, angle)
            return rotated_image
        except Exception as e:
            messagebox.showerror("Image Processing Error", f"Failed to process image: {e}")
            return None

    def pygame_to_tk(self):
        pygame_image = pygame.surfarray.array3d(self.surface)
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Transpose to (width, height, color)
        pygame_image = Image.fromarray(pygame_image)
        pygame_image = pygame_image.convert('RGB')

        self.tk_image = ImageTk.PhotoImage(image=pygame_image)
        self.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_click(self, event):
        for obj in self.objects:
            rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            if rect.collidepoint(event.x, event.y):
                self.dragging_object = obj
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                break

    def on_drag(self, event):
        if self.dragging_object:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.dragging_object['x'] += dx
            self.dragging_object['y'] += dy
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # Redraw objects
            self.draw_objects(self.objects)

            # Update the properties in the UI to reflect the new position
            self.update_object_properties_ui()

            # Use `self` to access the method, not `GameEditorApp`
            self.master.select_object_from_hierarchy()

    def update_object_properties_ui(self):
        """Update the UI elements with the current object's properties."""
        if self.dragging_object:
            self.master.object_name_entry.delete(0, tk.END)
            self.master.object_name_entry.insert(0, self.dragging_object['name'])
            self.master.object_x_entry.delete(0, tk.END)
            self.master.object_x_entry.insert(0, self.dragging_object['x'])
            self.master.object_y_entry.delete(0, tk.END)
            self.master.object_y_entry.insert(0, self.dragging_object['y'])
            self.master.object_width_entry.delete(0, tk.END)
            self.master.object_width_entry.insert(0, self.dragging_object['width'])
            self.master.object_height_entry.delete(0, tk.END)
            self.master.object_height_entry.insert(0, self.dragging_object['height'])
            self.master.object_speed_entry.delete(0, tk.END)
            self.master.object_speed_entry.insert(0, self.dragging_object['speed'])
            self.master.collider_var.set(self.dragging_object.get('collider', False))
            self.master.color_button.config(bg=self.dragging_object['color'])

    def on_release(self, event):
        if self.dragging_object:
            self.dragging_object = None
            self.pygame_to_tk()


class GameEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.global_script = ''
        self.title("Game Editor")
        self.geometry("1200x800")
        global current_scene_name
        current_scene_name = None
        self.selected_object = None

        # Create frames for different panels
        self.create_panels()
        self.update_scene_list()

    def load_image(self):
        if not self.selected_object:
            messagebox.showwarning("No Object Selected", "Please select an object before loading an image.")
            return

        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if image_path:
            width = self.selected_object['width']
            height = self.selected_object['height']
            self.pygame_canvas.add_image(image_path, self.selected_object['x'], self.selected_object['y'], width,
                                         height)

    def create_panels(self):
        # Left panel for Scene Management
        self.scene_manager_frame = tk.Frame(self, width=200, bg='#f0f0f0')
        self.scene_manager_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.scene_manager_frame, text="Scenes", bg='#f0f0f0').pack(pady=10)
        self.scene_listbox = tk.Listbox(self.scene_manager_frame)
        self.scene_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.scene_listbox.bind("<ButtonRelease-1>", self.select_scene)
        self.scene_listbox.bind("<Button-3>", self.show_scene_context_menu)

        self.create_scene_button = tk.Button(self.scene_manager_frame, text="Create Scene", command=self.create_scene)
        self.create_scene_button.pack(pady=5)
        self.rename_scene_button = tk.Button(self.scene_manager_frame, text="Rename Scene", command=self.rename_scene)
        self.rename_scene_button.pack(pady=5)
        self.delete_scene_button = tk.Button(self.scene_manager_frame, text="Delete Scene", command=self.delete_scene)
        self.delete_scene_button.pack(pady=5)

        # Right panel for Object Management
        self.object_manager_frame = tk.Frame(self, width=200, bg='#f0f0f0')
        self.object_manager_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.object_manager_frame, text="Objects", bg='#f0f0f0').pack(pady=10)
        self.object_listbox = tk.Listbox(self.object_manager_frame)
        self.object_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.object_listbox.bind("<ButtonRelease-1>", self.select_object_from_hierarchy)
        self.object_listbox.bind("<Button-3>", self.show_object_context_menu)

        self.create_object_button = tk.Button(self.object_manager_frame, text="Add Object", command=self.add_object)
        self.create_object_button.pack(pady=5)
        self.delete_object_button = tk.Button(self.object_manager_frame, text="Delete Object",
                                              command=self.delete_selected_object)
        self.delete_object_button.pack(pady=5)

        # Middle panel for Property Management
        self.property_manager_frame = tk.Frame(self, width=200, bg='#f0f0f0')
        self.property_manager_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.property_manager_frame, text="Object Properties", bg='#f0f0f0').pack(pady=10)

        tk.Label(self.property_manager_frame, text="Name:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_name_entry = tk.Entry(self.property_manager_frame)
        self.object_name_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="X:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_x_entry = tk.Entry(self.property_manager_frame)
        self.object_x_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="Y:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_y_entry = tk.Entry(self.property_manager_frame)
        self.object_y_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="Width:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_width_entry = tk.Entry(self.property_manager_frame)
        self.object_width_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="Height:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_height_entry = tk.Entry(self.property_manager_frame)
        self.object_height_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="Speed:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.object_speed_entry = tk.Entry(self.property_manager_frame)
        self.object_speed_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.property_manager_frame, text="Color:", anchor=tk.W, bg='#f0f0f0').pack(anchor=tk.W, padx=10)
        self.color_button = tk.Button(self.property_manager_frame, bg="#000000", command=self.choose_color)
        self.color_button.pack(fill=tk.X, padx=10, pady=5)

        self.collider_var = tk.BooleanVar()
        self.collider_checkbox = tk.Checkbutton(self.property_manager_frame, text="Collider",
                                                variable=self.collider_var, bg='#f0f0f0')
        self.collider_checkbox.pack(anchor=tk.W, padx=10)

        # Add canvas for drawing objects
        self.pygame_canvas = PygameCanvas(self)
        self.pygame_canvas.pack(fill=tk.BOTH, expand=True)

    def create_scene(self):
        scene_name = simpledialog.askstring("Scene Name", "Enter a name for the new scene:")
        if scene_name:
            if scene_name in scenes:
                messagebox.showwarning("Duplicate Scene", "A scene with this name already exists.")
            else:
                scenes[scene_name] = {
                    'objects': [],
                    'script': ''
                }
                self.update_scene_list()
                self.scene_listbox.select_set(tk.END)
                self.select_scene(None)

    def update_scene_list(self):
        self.scene_listbox.delete(0, tk.END)
        for scene_name in scenes.keys():
            self.scene_listbox.insert(tk.END, scene_name)

    def select_scene(self, event):
        global current_scene_name
        selection = self.scene_listbox.curselection()
        if selection:
            current_scene_name = self.scene_listbox.get(selection[0])
            self.update_object_listbox()
            self.pygame_canvas.draw_objects(scenes[current_scene_name]['objects'])
            print(f"Selected scene: {current_scene_name}")

    def rename_scene(self):
        global current_scene_name
        if current_scene_name:
            new_scene_name = simpledialog.askstring("New Scene Name", "Enter the new name for the scene:")
            if new_scene_name and new_scene_name not in scenes:
                scenes[new_scene_name] = scenes.pop(current_scene_name)
                current_scene_name = new_scene_name
                self.update_scene_list()
                self.select_scene(None)

    def delete_scene(self):
        global current_scene_name
        if current_scene_name:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the scene '{current_scene_name}'?")
            if confirm:
                scenes.pop(current_scene_name)
                current_scene_name = None
                self.update_scene_list()
                self.update_object_listbox()
                self.pygame_canvas.draw_objects([])  # Clear the canvas

    def open_scene_script_editor(self):
        if current_scene_name:
            self.open_script_editor(scenes[current_scene_name])

    def open_script_editor(self, script_data):
        script_window = tk.Toplevel(self)
        script_window.title("Script Editor")

        script_text = scrolledtext.ScrolledText(script_window)
        script_text.insert(tk.END, script_data['script'])
        script_text.pack(fill=tk.BOTH, expand=True)

        def save_script():
            script_data['script'] = script_text.get("1.0", tk.END)
            script_window.destroy()

        save_button = tk.Button(script_window, text="Save", command=save_script)
        save_button.pack(pady=10)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Color")
        if color_code:
            self.color_button.config(bg=color_code[1])
            if self.selected_object:
                self.selected_object['color'] = color_code[1]
                self.pygame_canvas.update_object(self.selected_object)

    def select_object_from_hierarchy(self, event=None):
        global current_scene_name
        selection = self.object_listbox.curselection()
        if selection and current_scene_name:
            selected_object_name = self.object_listbox.get(selection[0])
            for obj in scenes[current_scene_name]['objects']:
                if obj['name'] == selected_object_name:
                    self.selected_object = obj
                    self.update_object_properties_ui()
                    break

    def add_object(self):
        global current_scene_name
        if current_scene_name:
            new_object_name = simpledialog.askstring("Object Name", "Enter the name for the new object:")
            if new_object_name:
                new_object = {
                    'name': new_object_name,
                    'type': 'rect',
                    'x': 50,
                    'y': 50,
                    'width': 100,
                    'height': 100,
                    'color': '#0000FF',  # Default color is blue
                    'speed': 0,
                    'collider': False,
                    'image_path': None  # No image by default
                }
                scenes[current_scene_name]['objects'].append(new_object)
                self.update_object_listbox()
                self.pygame_canvas.draw_objects(scenes[current_scene_name]['objects'])
                print(f"Added new object: {new_object}")

    def update_object_listbox(self):
        self.object_listbox.delete(0, tk.END)
        if current_scene_name:
            for obj in scenes[current_scene_name]['objects']:
                self.object_listbox.insert(tk.END, obj['name'])

    def show_scene_context_menu(self, event):
        scene_menu = tk.Menu(self, tearoff=0)
        scene_menu.add_command(label="Open Script Editor", command=self.open_scene_script_editor)
        scene_menu.post(event.x_root, event.y_root)

    def show_object_context_menu(self, event):
        object_menu = tk.Menu(self, tearoff=0)
        object_menu.add_command(label="Delete Object", command=self.delete_selected_object)
        object_menu.post(event.x_root, event.y_root)

    def delete_selected_object(self):
        selected_object_name = self.object_listbox.curselection()
        if selected_object_name:
            obj_name = self.object_listbox.get(selected_object_name)
            scenes[current_scene_name]['objects'] = [obj for obj in scenes[current_scene_name]['objects'] if obj['name'] != obj_name]
            self.update_object_listbox()
            self.pygame_canvas.draw_objects(scenes[current_scene_name]['objects'])
            print(f"Deleted object: {obj_name}")

if __name__ == "__main__":
    scenes = {}  # Dictionary to store scenes
    app = GameEditorApp()
    app.mainloop()
