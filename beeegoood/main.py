from ursina import *

app = Ursina()

GRID_SIZE = 5
maadeha = ['water', 'grass', 'jungle', 'mountain']
seeelected = ['house', 'farm', "People"]



blocks = {}
window.fullscreen = True



class Block(Entity):
    def __init__(self, position, color=color.white):
        super().__init__(model='cube', color=color, scale=(1, 1, 1), position=position, collider='box')
        self.position = position

class Scene1:
    def __init__(self):
        self.cube = Entity(model='cube', color=color.orange, scale=(2, 2, 2), position=(0, 0, 0), collider='box')
        camera.position = (-3, 0.05, -10)
        camera.rotation = (5, 15, 5)
        self.txtcube1 = Text(text='PLLLAAY!', parent=self.cube, position=(-0.40, 0.2, -0.51), scale=10, color=color.black)

    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity == self.cube:
            print("Cube clicked in Scene 1!")
            borbsin(scene_2)

    def update(self):
        pass

class Scene2:
    def __init__(self):
        Sky()
        self.background_music = Audio('01 6 smyphonie.mp3', loop=True, autoplay=True)
        self.wood = 0
        self.stone = 0
        self.food = 0
        self.farm = 0
        self.house = 0
        self.martauma = 0
        self.maade = maadeha[0]
        self.edimode = True
        self.people_placed = False
        self.peoplecapacit = 0
        self.grass = 0
        self.jungle = 0
        self.mountain = 0
        self.everything = 0
        self.colorr = color.red
        camera.position = (0, 3, -10)
        camera.rotation = (20, 0, 0)
        self.selected = seeelected[0]
        panel = Panel(scale=(0.3, 5), color=color.rgba(36, 36, 36), position=(-0.745, 1))
        self.txtselected = Text(text="", position=(-0.88, 0.5))
        self.txtwarn = Text(text="", position=(-0.45, 0.5), color=color.black)
        self.population_txt = Text(text="", position=(-0.88, 0.45))
        self.food_txt = Text(text="", position=(-0.88, 0.40))
        self.wood_txt = Text(text="", position=(-0.88, 0.35))
        self.stone_txt = Text(text="", position=(-0.88, 0.30))
        self.z_txt = Text(text="Z key to select grass", position=(-0.88, 0.25))
        self.x_txt = Text(text="X key to select jungle", position=(-0.88, 0.20))
        self.c_txt = Text(text="C key to select mountain", position=(-0.88, 0.15))
        self.v_txt = Text(text="V key to select water", position=(-0.88, 0.10))
        self.v_txt = Text(text="E, Q, R, F key to rotate", position=(-0.88, 0.05))

        for x in range(-GRID_SIZE, GRID_SIZE):
            for z in range(-GRID_SIZE, GRID_SIZE):
                self.plan = Entity(model='cube', color=color.gray, scale=(1, 0.1, 1), position=(x, -0.5, z), collider='box')
                self.plan.model_name = "stone"

        for x in range(GRID_SIZE):
            for z in range(GRID_SIZE - 2 * GRID_SIZE):
                position = Vec3(x, -0.4, z)
                self.model = f'be_god_3d/water.glb'
                block = Entity(position=position, model=self.model, scale=(0.2, 0.2, 0.2))
                blocks[position] = block

        self.schedule_periodic_update()

    def schedule_periodic_update(self):
        invoke(self.update_periodically, delay=1)

    def update_periodically(self):
        self.uppppdate()
        invoke(self.update_periodically, delay=1)

    def bardarblock(self, position):
        if self.edimode:
            if position in blocks:
                blocks[position].disable()
                del blocks[position]
                self.everything -= 1

    def bezarblock(self, position, color=color.white):
        if self.edimode:
            if position not in blocks:
                self.everything += 1
                self.model = f'be_god_3d/{self.maade}.glb'
                self.block = Entity(position=position - (0, 0.4, 0.1), model=self.model, scale=(0.2, 0.2, 0.2), collider="box")
                blocks[position] = self.block
                if self.maade == "grass":
                    self.block.model_name = "grass"
                    self.grass += 1
                elif self.maade == "jungle":
                    self.block.model_name = "jungle"
                    self.jungle += 1
                elif self.maade == "mountain":
                    self.block.model_name = "mountain"
                    self.mountain += 1
                else:
                    self.block.model_name = "water"

                print(position)

    def update(self):
        if not self.edimode:
            self.txtselected.text = f"selected object: {self.selected}"
            self.txtwarn.text = "J key to select humanity to create,  h to select farm to build,  g to select house to build"
        else:
            self.txtselected.text = f"selected object: {self.maade}"
            self.txtwarn.text = "you should fill all of the land and then end creation with key Y"


        self.population_txt.text = f"population: {int(self.martauma)}"
        self.food_txt.text = f"food: {round(self.food)}"
        self.wood_txt.text = f"wood: {round(self.wood)}"
        self.stone_txt.text = f"stone: {round(self.stone)}"

    def gameover(self):
        self.gameovertxt = Text(text="GAME OVER, create more grass to save people from starving", position=(-0.08, 0))
        for position in list(blocks.keys()):
            blocks[position].disable()
            del blocks[position]

    def uppppdate(self):
        self.peoplecapacit = (self.grass*15) + (self.mountain*5) + (self.jungle*10) + (self.house*5)
        if self.martauma <= self.peoplecapacit:
           self.martauma *= 1.05
        self.food += (self.grass * 1 * (self.martauma/4)) + self.farm*5
        self.food -= self.martauma * 2
        self.stone += self.mountain * 0.15 * self.martauma / 4
        self.wood += self.jungle * 0.25 * self.martauma / 4
        if self.food < 0:
            self.martauma = 0
            self.farm = 0
            self.house = 0
            self.stone = 0
            self.wood = 0
            destroy(self.sakhteman)
            self.edimode = True
            self.people_placed = False
            self.food = 0
            self.gameover()
            destroy(self.gameovertxt, delay=3)

    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity:
                try:
                  if not self.edimode:
                    if mouse.hovered_entity.model_name == 'grass':
                        if self.selected == seeelected[2] and not self.people_placed:
                            self.people_placed = True
                            self.sakhteman = Entity(position=mouse.hovered_entity.position + Vec3(0, 0.61, 0), model=f'be_god_3d/{self.selected}.glb', scale=(0.2, 0.2, 0.2), collider="box")
                            mouse.hovered_entity.model_name = "notgrass"
                            print("people_placed")
                            self.martauma += 2
                        if self.selected == seeelected[1]:
                            if self.wood >= 20 and self.stone >= 6:
                                self.sakhteman = Entity(position=mouse.hovered_entity.position + Vec3(0, 0.61, 0), model=f'be_god_3d/{self.selected}.glb', scale=(0.2, 0.2, 0.2), collider="box")
                                mouse.hovered_entity.model_name = "notgrass"
                                self.farm += 1
                                self.stone -= 6
                                self.wood -= 20
                        if self.selected == seeelected[0]:
                            if self.wood >= 30 and self.stone >= 18:
                                self.sakhteman = Entity(position=mouse.hovered_entity.position + Vec3(0, 0.61, 0), model=f'be_god_3d/{self.selected}.glb', scale=(0.2, 0.2, 0.2), collider="box")
                                mouse.hovered_entity.model_name = "notgrass"
                                self.house += 1
                                self.stone -= 30
                                self.wood -= 18
                    elif mouse.hovered_entity.model_name == 'water':
                        print("Clicked on water block!")
                    else:
                        print("Clicked on something else.")
                except AttributeError:
                    print("The clicked object doesn't have a model_name.")
                pos = mouse.hovered_entity.position
                grid_pos = Vec3(round(pos.x), round(pos.y), round(pos.z))
                self.bezarblock(grid_pos)

        if key == 'right mouse down':
            if mouse.hovered_entity:
                try:
                    if mouse.hovered_entity.model_name == 'grass':
                        self.grass -= 1
                    elif mouse.hovered_entity.model_name == 'jungle':
                        self.jungle -= 1
                    elif mouse.hovered_entity.model_name == 'mountain':
                        self.mountain -= 1
                except AttributeError:
                    print("The clicked object doesn't have a model_name.")
                pos = mouse.hovered_entity.position
                grid_pos = Vec3(round(pos.x), round(pos.y), round(pos.z))
                self.bardarblock(grid_pos)

        if held_keys['w']:
            camera.position += Vec3(0, 0, time.dt * 5)
        if held_keys['s']:
            camera.position -= Vec3(0, 0, time.dt * 5)
        if held_keys['a']:
            camera.position -= Vec3(time.dt * 5, 0, 0)
        if held_keys['d']:
            camera.position += Vec3(time.dt * 5, 0, 0)
        if held_keys['r']:
            camera.rotation_x -= time.dt * 100
        if held_keys['f']:
            camera.rotation_x += time.dt * 100
        if held_keys["e"]:
            camera.rotation_y += time.dt * 100
        if held_keys["q"]:
            camera.rotation_y -= time.dt * 100
        if held_keys["z"]:
            self.maade = maadeha[1]
        if held_keys["x"]:
            self.maade = maadeha[2]
        if held_keys["c"]:
            self.maade = maadeha[3]
        if held_keys["v"]:
            self.maade = maadeha[0]
        if held_keys["g"]:
            self.selected = seeelected[0]
        if held_keys["h"]:
            self.selected = seeelected[1]
        if held_keys["j"] and not self.people_placed:
            self.selected = seeelected[2]
        if held_keys["y"] and self.everything == 100:
            self.edimode = False
        if held_keys["o"]:
            self.edimode = False

def borbsin(scene_class):
    nabod()
    global current_scene
    current_scene = scene_class()

def nabod():
    for entity in scene.entities:
        destroy(entity)

def update():
    current_scene.update()

def input(key):
    current_scene.input(key)

scene_1 = Scene1
scene_2 = Scene2
current_scene = scene_1()

app.run()
