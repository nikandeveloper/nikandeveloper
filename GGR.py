import pygame
import sys
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import io
import contextlib

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
PANEL_WIDTH = 100
PROPERTIES_PANEL_WIDTH = 125
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BUTTON_COLOR = (0, 128, 0)
TEXT_COLOR = (255, 255, 255)
PROPERTIES_PANEL_COLOR = (150, 150, 150)

# Set up fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Engine with Integrated UI Panel")

# Define UI elements
ui_elements = {
    'start_game': pygame.Rect(0, 10, PANEL_WIDTH - 20, 40),
    'stop_game': pygame.Rect(0, 60, PANEL_WIDTH - 20, 40),
    'speed_entry': pygame.Rect(0, 110, PANEL_WIDTH - 20, 30),
    'speed_button': pygame.Rect(0, 150, PANEL_WIDTH - 20, 30),
    'script_button': pygame.Rect(0, 190, PANEL_WIDTH - 20, 30),
    'scenes_button': pygame.Rect(0, 230, PANEL_WIDTH - 20, 40),
}

property_elements = {
    'properties_panel': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH, 0, PROPERTIES_PANEL_WIDTH, SCREEN_HEIGHT),
    'object_name_label': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 10, PROPERTIES_PANEL_WIDTH - 20, 20),
    'object_name_entry': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 30, PROPERTIES_PANEL_WIDTH - 20, 30),
    'object_x_label': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 70, PROPERTIES_PANEL_WIDTH - 20, 20),
    'object_y_label': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 110, PROPERTIES_PANEL_WIDTH - 20, 20),
    'object_speed_label': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 150, PROPERTIES_PANEL_WIDTH - 20, 20),
    'object_speed_entry': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 170, PROPERTIES_PANEL_WIDTH - 20, 30),
    'object_interaction_label': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 210, PROPERTIES_PANEL_WIDTH - 20, 20),
    'object_interaction_button': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 230, PROPERTIES_PANEL_WIDTH - 20, 30),
    'delete_button': pygame.Rect(SCREEN_WIDTH - PROPERTIES_PANEL_WIDTH + 10, 270, PROPERTIES_PANEL_WIDTH - 20, 40),
}

scene_elements = {
    'create_scene_button': pygame.Rect(0, 270, PANEL_WIDTH - 20, 40),
    'rename_scene_button': pygame.Rect(0, 320, PANEL_WIDTH - 20, 40),
}

class GameObject:
    _id_counter = 0

    def __init__(self, x, y, name="Unnamed", image_path=None):
        self.id = GameObject._id_counter
        GameObject._id_counter += 1
        self.x = x
        self.y = y
        self.name = name
        self.image = self.load_image(image_path) if image_path else None

    def load_image(self, image_path):
        try:
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, (50, 50))
        except pygame.error:
            return None

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, WHITE, (self.x, self.y, 50, 50))
        name_surface = font.render(self.name, True, WHITE)
        surface.blit(name_surface, (self.x, self.y - 30))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width() if self.image else 50, self.image.get_height() if self.image else 50)

    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos)

class MovingObject(GameObject):
    def __init__(self, x, y, name="MovingObject", image_path=None, speed=5):
        super().__init__(x, y, name, image_path)
        self.speed = speed

    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH or self.x < 0:
            self.speed = -self.speed

class StationaryObject(GameObject):
    pass

class InteractiveObject(GameObject):
    def __init__(self, x, y, name="InteractiveObject", image_path=None, interact_action=None):
        super().__init__(x, y, name, image_path)
        self.interact_action = interact_action

    def interact(self):
        if self.interact_action:
            self.interact_action()

class Scene:
    def __init__(self, name):
        self.name = name
        self.objects = []
        self.scripts = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def add_script(self, script_content):
        self.scripts.append(script_content)

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def update(self):
        for obj in self.objects:
            if isinstance(obj, MovingObject):
                obj.update()

scenes = {
    'Default': Scene('Default')
}
current_scene_name = 'Default'

def get_current_scene():
    return scenes[current_scene_name]

def create_scene(name):
    if name not in scenes:
        scenes[name] = Scene(name)
    else:
        messagebox.showerror("Error", "Scene with this name already exists.")

def rename_scene(old_name, new_name):
    if old_name in scenes and new_name not in scenes:
        scenes[new_name] = scenes.pop(old_name)
        scenes[new_name].name = new_name
        global current_scene_name
        if old_name == current_scene_name:
            current_scene_name = new_name
    else:
        messagebox.showerror("Error", "Scene name conflict or non-existent scene.")

def delete_scene(name):
    if name in scenes and len(scenes) > 1:
        del scenes[name]
        if name == current_scene_name:
            current_scene_name = next(iter(scenes))
    else:
        messagebox.showerror("Error", "Cannot delete the last scene or non-existent scene.")

def draw_text_input(text, rect, color=TEXT_COLOR):
    if not isinstance(text, str):
        text = str(text)
    text_surface = small_font.render(text, True, color)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))

def draw_ui():
    screen.fill(GRAY, pygame.Rect(0, 0, PANEL_WIDTH, SCREEN_HEIGHT))
    
    for key, rect in ui_elements.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)

    screen.blit(small_font.render("Start Game", True, TEXT_COLOR), (ui_elements['start_game'].x + 10, ui_elements['start_game'].y + 5))
    screen.blit(small_font.render("Stop Game", True, TEXT_COLOR), (ui_elements['stop_game'].x + 10, ui_elements['stop_game'].y + 5))
    screen.blit(small_font.render("Update Speed", True, TEXT_COLOR), (ui_elements['speed_button'].x + 10, ui_elements['speed_button'].y + 5))
    screen.blit(small_font.render("Open Script Editor", True, TEXT_COLOR), (ui_elements['script_button'].x + 10, ui_elements['script_button'].y + 5))
    screen.blit(small_font.render("Scenes", True, TEXT_COLOR), (ui_elements['scenes_button'].x + 10, ui_elements['scenes_button'].y + 5))

    screen.fill(PROPERTIES_PANEL_COLOR, property_elements['properties_panel'])
    
    screen.blit(small_font.render("Name:", True, TEXT_COLOR), (property_elements['object_name_label'].x + 10, property_elements['object_name_label'].y + 5))
    screen.blit(small_font.render("X:", True, TEXT_COLOR), (property_elements['object_x_label'].x + 10, property_elements['object_x_label'].y + 5))
    screen.blit(small_font.render("Y:", True, TEXT_COLOR), (property_elements['object_y_label'].x + 10, property_elements['object_y_label'].y + 5))
    screen.blit(small_font.render("Speed:", True, TEXT_COLOR), (property_elements['object_speed_label'].x + 10, property_elements['object_speed_label'].y + 5))
    screen.blit(small_font.render("Interaction:", True, TEXT_COLOR), (property_elements['object_interaction_label'].x + 10, property_elements['object_interaction_label'].y + 5))

    pygame.draw.rect(screen, WHITE, property_elements['object_name_entry'])
    pygame.draw.rect(screen, WHITE, property_elements['object_speed_entry'])
    
    for key, rect in scene_elements.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)

    screen.blit(small_font.render("Create Scene", True, TEXT_COLOR), (scene_elements['create_scene_button'].x + 10, scene_elements['create_scene_button'].y + 5))
    screen.blit(small_font.render("Rename Scene", True, TEXT_COLOR), (scene_elements['rename_scene_button'].x + 10, scene_elements['rename_scene_button'].y + 5))

def open_script_editor():
    def execute_script():
        code = editor.get("1.0", tk.END).strip()
        if code:
            try:
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    exec(code, globals())
                output = buffer.getvalue()
                terminal_output.config(state=tk.NORMAL)
                terminal_output.insert(tk.END, output)
                terminal_output.config(state=tk.DISABLED)
            except Exception as e:
                terminal_output.config(state=tk.NORMAL)
                terminal_output.insert(tk.END, f"Error: {e}\n")
                terminal_output.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Warning", "No script entered.")
    
    def save_script():
        script = editor.get("1.0", tk.END).strip()
        if script:
            print("Script saved:", script)
            editor_window.destroy()
        else:
            messagebox.showwarning("Warning", "Script cannot be empty.")
    
    editor_window = tk.Tk()
    editor_window.title("Script Editor")
    
    # Set up frames
    editor_frame = tk.Frame(editor_window)
    editor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    terminal_frame = tk.Frame(editor_window)
    terminal_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    # Editor text area
    editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, width=60, height=20)
    editor.grid(row=0, column=0, sticky="nsew")
    
    # Terminal output area
    terminal_output = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, width=30, height=20, state=tk.DISABLED)
    terminal_output.grid(row=0, column=0, sticky="nsew")
    
    # Buttons
    button_frame = tk.Frame(editor_window)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
    
    run_button = tk.Button(button_frame, text="Run", command=execute_script)
    run_button.grid(row=0, column=0, padx=5)
    
    save_button = tk.Button(button_frame, text="Save", command=save_script)
    save_button.grid(row=0, column=1, padx=5)
    
    # Adjust grid weights
    editor_window.grid_columnconfigure(0, weight=2)
    editor_window.grid_columnconfigure(1, weight=1)
    editor_window.grid_rowconfigure(0, weight=1)
    editor_window.grid_rowconfigure(1, weight=0)
    
    editor_window.mainloop()

def open_scene_manager():
    def create_scene_callback():
        new_name = simpledialog.askstring("Create Scene", "Enter scene name:")
        if new_name:
            create_scene(new_name)

    def rename_scene_callback():
        old_name = simpledialog.askstring("Rename Scene", "Enter current scene name:")
        if old_name:
            new_name = simpledialog.askstring("Rename Scene", "Enter new scene name:")
            if new_name:
                rename_scene(old_name, new_name)

    def delete_scene_callback():
        name = simpledialog.askstring("Delete Scene", "Enter scene name to delete:")
        if name:
            delete_scene(name)

    def add_object_to_scene(scene_name):
        x = simpledialog.askinteger("Add Object", "Enter X position:")
        y = simpledialog.askinteger("Add Object", "Enter Y position:")
        name = simpledialog.askstring("Add Object", "Enter object name:")
        if x is not None and y is not None and name:
            new_object = GameObject(x, y, name)
            scenes[scene_name].add_object(new_object)
            print(f"Added object {name} at ({x}, {y}) to scene {scene_name}")

    def add_script_to_scene(scene_name):
        def save_script():
            script_content = script_editor.get("1.0", tk.END).strip()
            if script_content:
                scenes[scene_name].add_script(script_content)
                print(f"Added script to scene {scene_name}")
            else:
                messagebox.showwarning("Warning", "Script cannot be empty.")
            script_window.destroy()

        script_window = tk.Tk()
        script_window.title(f"Script Editor for {scene_name}")
        
        script_editor = scrolledtext.ScrolledText(script_window, width=60, height=20)
        script_editor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        save_button = tk.Button(script_window, text="Save Script", command=save_script)
        save_button.pack(pady=5)
        
        script_window.mainloop()

    def show_objects_scripts(scene_name):
        def on_add_object():
            add_object_to_scene(scene_name)

        def on_add_script():
            add_script_to_scene(scene_name)

        objects_window = tk.Tk()
        objects_window.title(f"{scene_name} - Objects and Scripts")
        
        objects_frame = tk.Frame(objects_window)
        objects_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        list_frame = tk.Frame(objects_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        objects_list = tk.Listbox(list_frame, height=15, width=50)
        objects_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scripts_list = tk.Listbox(list_frame, height=15, width=50)
        scripts_list.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        for obj in scenes[scene_name].objects:
            objects_list.insert(tk.END, obj.name)
        
        for script in scenes[scene_name].scripts:
            scripts_list.insert(tk.END, script[:50] + ('...' if len(script) > 50 else ''))
        
        button_frame = tk.Frame(objects_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Add Object", command=on_add_object).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add Script", command=on_add_script).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=objects_window.destroy).pack(side=tk.LEFT, padx=5)
        
        objects_window.mainloop()

    scene_manager = tk.Tk()
    scene_manager.title("Scene Manager")
    
    scenes_frame = tk.Frame(scene_manager)
    scenes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scenes_list = tk.Listbox(scenes_frame, height=15, width=50)
    for name in scenes:
        scenes_list.insert(tk.END, name)
    
    scenes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    button_frame = tk.Frame(scene_manager)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
    
    tk.Button(button_frame, text="Create New Scene", command=create_scene_callback).pack(pady=5)
    tk.Button(button_frame, text="Rename Scene", command=rename_scene_callback).pack(pady=5)
    tk.Button(button_frame, text="Delete Scene", command=delete_scene_callback).pack(pady=5)
    tk.Button(button_frame, text="Close", command=scene_manager.destroy).pack(pady=5)
    
    def on_right_click(event):
        selection = scenes_list.curselection()
        if selection:
            scene_name = scenes_list.get(selection[0])
            show_objects_scripts(scene_name)
    
    scenes_list.bind("<Button-3>", on_right_click)
    
    scene_manager.mainloop()

def main():
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui_elements['start_game'].collidepoint(event.pos):
                    print("Start Game")
                elif ui_elements['stop_game'].collidepoint(event.pos):
                    print("Stop Game")
                elif ui_elements['speed_button'].collidepoint(event.pos):
                    new_speed = simpledialog.askinteger("Update Speed", "Enter new speed:", initialvalue=speed)
                    if new_speed is not None:
                        speed = new_speed
                elif ui_elements['script_button'].collidepoint(event.pos):
                    open_script_editor()
                elif ui_elements['scenes_button'].collidepoint(event.pos):
                    open_scene_manager()
                elif property_elements['delete_button'].collidepoint(event.pos):
                    obj = get_current_scene().objects
                    if obj:
                        get_current_scene().remove_object(obj[-1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if get_current_scene().objects:
                        get_current_scene().remove_object(get_current_scene().objects[-1])
        
        screen.fill(BLACK)
        get_current_scene().update()
        get_current_scene().draw(screen)
        draw_ui()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
