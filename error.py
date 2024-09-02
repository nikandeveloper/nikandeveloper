import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QLabel, QLineEdit,
    QFrame, QListWidget, QFormLayout, QFileDialog, QInputDialog, QColorDialog, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PyQt6.QtGui import QColor, QPixmap, QPainter, QIcon
from PyQt6.QtCore import Qt, QRectF, QPointF
from collections import deque
import os


class DraggableGraphicsItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            if self.scene():
                editor = self.scene().parent().parent()
                editor.update_property_fields()
        return super().itemChange(change, value)


class DraggablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, True)

    def itemChange(self, change, value):
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemPositionChange:
            if self.scene():
                editor = self.scene().parent().parent()
                editor.update_property_fields()
        return super().itemChange(change, value)


class GameEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphical Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #2e2e2e;")  # Dark background

        self.scenes = {}
        self.current_scene = None
        self.current_item = None
        self.current_item_index = -1

        self.undo_stack = deque()
        self.redo_stack = deque()

        self.initUI()

    def initUI(self):
        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Toolbar
        self.create_toolbar(main_layout)

        # Main Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left Panel (Sidebar)
        self.create_side_panels(splitter)

        # Right Panel (Inspector)
        self.create_inspector_panel(splitter)

        # Canvas Area
        self.create_canvas_area(splitter)

    def create_toolbar(self, layout):
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(2)

        new_scene_btn = QPushButton()
        new_scene_btn.setIcon(QIcon("path/to/new_scene_icon.png"))
        new_scene_btn.setToolTip("Create a new scene")
        new_scene_btn.setStyleSheet("background-color: #555555; color: white;")
        new_scene_btn.clicked.connect(self.create_scene)
        toolbar.addWidget(new_scene_btn)

        add_rect_btn = QPushButton()
        add_rect_btn.setIcon(QIcon("path/to/add_rectangle_icon.png"))
        add_rect_btn.setToolTip("Add Rectangle")
        add_rect_btn.setStyleSheet("background-color: #555555; color: white;")
        add_rect_btn.clicked.connect(self.add_rectangle)
        toolbar.addWidget(add_rect_btn)

        add_img_btn = QPushButton()
        add_img_btn.setIcon(QIcon("path/to/add_image_icon.png"))
        add_img_btn.setToolTip("Add Image")
        add_img_btn.setStyleSheet("background-color: #555555; color: white;")
        add_img_btn.clicked.connect(self.add_image)
        toolbar.addWidget(add_img_btn)

        undo_btn = QPushButton()
        undo_btn.setIcon(QIcon("path/to/undo_icon.png"))
        undo_btn.setToolTip("Undo")
        undo_btn.setStyleSheet("background-color: #555555; color: white;")
        undo_btn.clicked.connect(self.undo)
        toolbar.addWidget(undo_btn)

        redo_btn = QPushButton()
        redo_btn.setIcon(QIcon("path/to/redo_icon.png"))
        redo_btn.setToolTip("Redo")
        redo_btn.setStyleSheet("background-color: #555555; color: white;")
        redo_btn.clicked.connect(self.redo)
        toolbar.addWidget(redo_btn)

        layout.addLayout(toolbar)

    def create_side_panels(self, splitter):
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #3a3a3a;")
        left_panel.setFixedWidth(200)
        left_panel_layout = QVBoxLayout(left_panel)

        scenes_label = QLabel("Scenes")
        scenes_label.setStyleSheet("color: white;")
        left_panel_layout.addWidget(scenes_label)

        self.scene_list = QListWidget()
        self.scene_list.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.scene_list.currentItemChanged.connect(self.select_scene)
        left_panel_layout.addWidget(self.scene_list)

        scene_buttons_layout = QVBoxLayout()

        create_scene_btn = QPushButton("Create Scene")
        create_scene_btn.setStyleSheet("background-color: #555555; color: white;")
        create_scene_btn.clicked.connect(self.create_scene)
        scene_buttons_layout.addWidget(create_scene_btn)

        rename_scene_btn = QPushButton("Rename Scene")
        rename_scene_btn.setStyleSheet("background-color: #555555; color: white;")
        rename_scene_btn.clicked.connect(self.rename_scene)
        scene_buttons_layout.addWidget(rename_scene_btn)

        delete_scene_btn = QPushButton("Delete Scene")
        delete_scene_btn.setStyleSheet("background-color: #555555; color: white;")
        delete_scene_btn.clicked.connect(self.delete_scene)
        scene_buttons_layout.addWidget(delete_scene_btn)

        left_panel_layout.addLayout(scene_buttons_layout)
        splitter.addWidget(left_panel)

    def create_inspector_panel(self, splitter):
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #3a3a3a;")
        right_panel.setFixedWidth(300)

        inspector_layout = QVBoxLayout(right_panel)

        self.properties_table = QTableWidget()
        self.properties_table.setColumnCount(2)
        self.properties_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.properties_table.horizontalHeader().setStretchLastSection(True)
        self.properties_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.properties_table.setStyleSheet("background-color: #4e4e4e; color: white;")
        inspector_layout.addWidget(self.properties_table)

        self.properties_table.itemChanged.connect(self.handle_item_edited)

        splitter.addWidget(right_panel)

    def create_canvas_area(self, splitter):
        canvas_frame = QFrame()
        canvas_frame.setStyleSheet("background-color: #2e2e2e;")
        canvas_layout = QVBoxLayout(canvas_frame)

        self.canvas_scene = QGraphicsScene()
        self.canvas_view = QGraphicsView(self.canvas_scene)
        self.canvas_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.canvas_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.canvas_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.canvas_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.canvas_view.setScene(self.canvas_scene)
        canvas_layout.addWidget(self.canvas_view)

        splitter.addWidget(canvas_frame)

        # Optional grid
        self.draw_grid()

    def draw_grid(self):
        for i in range(-2000, 2000, 20):
            self.canvas_scene.addLine(i, -2000, i, 2000, QColor("#d3d3d3"))
        for j in range(-2000, 2000, 20):
            self.canvas_scene.addLine(-2000, j, 2000, j, QColor("#d3d3d3"))

    def create_scene(self):
        name, ok = QInputDialog.getText(self, "Create Scene", "Enter scene name:")
        if ok and name:
            if name not in self.scenes:
                self.scenes[name] = []
                self.scene_list.addItem(name)
                self.select_scene(self.scene_list.currentItem())
                self.perform_action({'action': 'create_scene', 'name': name})
            else:
                QMessageBox.warning(self, "Warning", "Scene already exists.")

    def select_scene(self, item):
        if item:
            scene_name = item.text()
            if scene_name in self.scenes:
                self.current_scene = scene_name
                self.current_item = None
                self.current_item_index = -1
                self.update_object_hierarchy()
                self.update_canvas()

    def rename_scene(self):
        if self.current_scene:
            new_name, ok = QInputDialog.getText(self, "Rename Scene", "Enter new scene name:")
            if ok and new_name and new_name not in self.scenes:
                row = self.scene_list.currentRow()
                self.scene_list.takeItem(row)
                self.scene_list.insertItem(row, new_name)
                self.scenes[new_name] = self.scenes.pop(self.current_scene)
                self.current_scene = new_name
                self.update_canvas()
                self.perform_action({'action': 'rename_scene', 'old_name': self.current_scene, 'new_name': new_name})
            else:
                QMessageBox.warning(self, "Warning", "Invalid scene name or scene already exists.")

    def delete_scene(self):
        if self.current_scene:
            self.scenes.pop(self.current_scene)
            row = self.scene_list.currentRow()
            self.scene_list.takeItem(row)
            self.current_scene = None
            self.update_canvas()
            self.perform_action({'action': 'delete_scene', 'name': self.current_scene})

    def add_rectangle(self):
        if not self.current_scene:
            return

        x, ok_x = QInputDialog.getInt(self, "Rectangle Position", "Enter X position:")
        y, ok_y = QInputDialog.getInt(self, "Rectangle Position", "Enter Y position:")
        width, ok_w = QInputDialog.getInt(self, "Rectangle Size", "Enter width:")
        height, ok_h = QInputDialog.getInt(self, "Rectangle Size", "Enter height:")
        angle, ok_a = QInputDialog.getInt(self, "Rectangle Angle", "Enter angle:")
        color = QColorDialog.getColor()

        if ok_x and ok_y and ok_w and ok_h and ok_a and color.isValid() and width > 0 and height > 0:
            obj = {
                'type': 'rectangle', 'name': f"Rectangle {len(self.scenes[self.current_scene])+1}",
                'x': x, 'y': y, 'width': width, 'height': height, 'angle': angle, 'color': color.name()
            }
            self.scenes[self.current_scene].append(obj)
            self.update_object_hierarchy()
            self.update_canvas()
            self.perform_action({'action': 'add_rectangle', 'object': obj})

    def add_image(self):
        if not self.current_scene:
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            x, ok_x = QInputDialog.getInt(self, "Image Position", "Enter X position:")
            y, ok_y = QInputDialog.getInt(self, "Image Position", "Enter Y position:")

            if ok_x and ok_y and os.path.isfile(file_path):
                obj = {'type': 'image', 'name': f"Image {len(self.scenes[self.current_scene])+1}",
                       'file_path': file_path, 'x': x, 'y': y}
                self.scenes[self.current_scene].append(obj)
                self.update_object_hierarchy()
                self.update_canvas()
                self.perform_action({'action': 'add_image', 'object': obj})
            else:
                QMessageBox.warning(self, "Warning", "Invalid file path or position.")

    def handle_item_edited(self, item):
        if self.current_item is not None and self.current_scene:
            column = item.column()
            if column == 1:
                value = item.text()
                if self.current_item['type'] == 'rectangle':
                    if item.row() == 1:  # Position
                        x, y = [int(v) for v in value.split(',')]
                        self.current_item['x'] = x
                        self.current_item['y'] = y
                    elif item.row() == 2:  # Size
                        width, height = [int(v) for v in value.split(',')]
                        self.current_item['width'] = width
                        self.current_item['height'] = height
                    elif item.row() == 3:  # Angle
                        self.current_item['angle'] = int(value)
                    elif item.row() == 4:  # Color
                        self.current_item['color'] = value
                elif self.current_item['type'] == 'image':
                    if item.row() == 1:  # File
                        if os.path.isfile(value):
                            self.current_item['file_path'] = value
                        else:
                            QMessageBox.warning(self, "Warning", "Invalid file path.")
                    elif item.row() == 2:  # Position
                        x, y = [int(v) for v in value.split(',')]
                        self.current_item['x'] = x
                        self.current_item['y'] = y
                self.update_canvas()
                self.perform_action({'action': 'edit_item', 'item': self.current_item})

    def update_object_hierarchy(self):
        self.properties_table.setRowCount(0)
        if self.current_scene:
            for index, obj in enumerate(self.scenes.get(self.current_scene, [])):
                row_position = self.properties_table.rowCount()
                self.properties_table.insertRow(row_position)
                self.properties_table.setItem(row_position, 0, QTableWidgetItem(obj['name']))
                if obj['type'] == 'rectangle':
                    self.properties_table.setItem(
                        row_position, 1, QTableWidgetItem(
                            f"Pos: ({obj['x']}, {obj['y']}), Size: ({obj['width']}x{obj['height']}), Angle: {obj['angle']}, Color: {obj['color']}"
                        )
                    )
                elif obj['type'] == 'image':
                    self.properties_table.setItem(
                        row_position, 1, QTableWidgetItem(
                            f"File: {obj['file_path']}, Pos: ({obj['x']}, {obj['y']})"
                        )
                    )

                self.properties_table.cellClicked.connect(self.object_selected)

    def update_canvas(self):
        self.canvas_scene.clear()
        self.draw_grid()
        if self.current_scene:
            for obj in self.scenes.get(self.current_scene, []):
                if obj['type'] == 'rectangle':
                    rect = DraggableGraphicsItem(obj['x'], obj['y'], obj['width'], obj['height'])
                    rect.setBrush(QColor(obj['color']))
                    rect.setTransformOriginPoint(obj['x'] + obj['width'] / 2, obj['y'] + obj['height'] / 2)
                    rect.setRotation(obj['angle'])
                    self.canvas_scene.addItem(rect)
                elif obj['type'] == 'image':
                    pixmap = QPixmap(obj['file_path'])
                    pixmap_item = DraggablePixmapItem(pixmap)
                    pixmap_item.setPos(obj['x'], obj['y'])
                    self.canvas_scene.addItem(pixmap_item)

    def object_selected(self, row, column):
        if self.current_scene:
            self.current_item_index = row
            self.current_item = self.scenes[self.current_scene][self.current_item_index]
            self.update_property_fields()

    def update_property_fields(self):
        if self.current_item is not None:
            self.properties_table.setRowCount(0)
            self.properties_table.insertRow(0)
            self.properties_table.setItem(0, 0, QTableWidgetItem("Name"))
            self.properties_table.setItem(0, 1, QTableWidgetItem(self.current_item['name']))

            if self.current_item['type'] == 'rectangle':
                self.properties_table.insertRow(1)
                self.properties_table.setItem(1, 0, QTableWidgetItem("Position"))
                self.properties_table.setItem(1, 1, QTableWidgetItem(f"X: {self.current_item['x']}, Y: {self.current_item['y']}"))

                self.properties_table.insertRow(2)
                self.properties_table.setItem(2, 0, QTableWidgetItem("Size"))
                self.properties_table.setItem(2, 1, QTableWidgetItem(f"Width: {self.current_item['width']}, Height: {self.current_item['height']}"))

                self.properties_table.insertRow(3)
                self.properties_table.setItem(3, 0, QTableWidgetItem("Angle"))
                self.properties_table.setItem(3, 1, QTableWidgetItem(str(self.current_item['angle'])))

                self.properties_table.insertRow(4)
                self.properties_table.setItem(4, 0, QTableWidgetItem("Color"))
                self.properties_table.setItem(4, 1, QTableWidgetItem(self.current_item['color']))

            elif self.current_item['type'] == 'image':
                self.properties_table.insertRow(1)
                self.properties_table.setItem(1, 0, QTableWidgetItem("File"))
                self.properties_table.setItem(1, 1, QTableWidgetItem(self.current_item['file_path']))

                self.properties_table.insertRow(2)
                self.properties_table.setItem(2, 0, QTableWidgetItem("Position"))
                self.properties_table.setItem(2, 1, QTableWidgetItem(f"X: {self.current_item['x']}, Y: {self.current_item['y']}"))

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            self.perform_action(action, undo=True)

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            self.perform_action(action)

    def perform_action(self, action, undo=False):
        action_type = action.get('action')

        if action_type == 'create_scene':
            if undo:
                scene_name = action['name']
                self.scenes.pop(scene_name)
                row = self.scene_list.findItems(scene_name, Qt.MatchFlag.MatchExactly)[0]
                self.scene_list.takeItem(self.scene_list.row(row))
            else:
                scene_name = action['name']
                self.scenes[scene_name] = []
                self.scene_list.addItem(scene_name)

        elif action_type == 'rename_scene':
            old_name = action['old_name']
            new_name = action['new_name']
            if undo:
                self.scenes[old_name] = self.scenes.pop(new_name)
                row = self.scene_list.findItems(new_name, Qt.MatchFlag.MatchExactly)[0]
                self.scene_list.takeItem(self.scene_list.row(row))
                self.scene_list.insertItem(self.scene_list.row(row), old_name)
            else:
                self.scenes[new_name] = self.scenes.pop(old_name)
                row = self.scene_list.findItems(old_name, Qt.MatchFlag.MatchExactly)[0]
                self.scene_list.takeItem(self.scene_list.row(row))
                self.scene_list.insertItem(self.scene_list.row(row), new_name)

        elif action_type == 'delete_scene':
            scene_name = action['name']
            if undo:
                self.scenes[scene_name] = []
                self.scene_list.addItem(scene_name)
            else:
                self.scenes.pop(scene_name)
                row = self.scene_list.findItems(scene_name, Qt.MatchFlag.MatchExactly)[0]
                self.scene_list.takeItem(self.scene_list.row(row))

        elif action_type == 'add_rectangle':
            obj = action['object']
            if undo:
                self.scenes[self.current_scene].remove(obj)
            else:
                self.scenes[self.current_scene].append(obj)
            self.update_canvas()

        elif action_type == 'add_image':
            obj = action['object']
            if undo:
                self.scenes[self.current_scene].remove(obj)
            else:
                self.scenes[self.current_scene].append(obj)
            self.update_canvas()

        elif action_type == 'edit_item':
            item = action['item']
            if undo:
                pass  # Implement undo logic for editing
            else:
                pass  # Implement redo logic for editing

        self.update_canvas()

    def save_scene(self):
        if not self.current_scene:
            QMessageBox.warning(self, "Warning", "No scene selected.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Scene", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(self.scenes, file)
            QMessageBox.information(self, "Success", "Scene saved successfully.")

    def load_scene(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Scene", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                self.scenes = json.load(file)
            self.select_scene(self.scene_list.currentItem())
            QMessageBox.information(self, "Success", "Scene loaded successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameEditorApp()
    window.show()
    sys.exit(app.exec())
