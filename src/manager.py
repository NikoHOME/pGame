import dearpygui.dearpygui as dpg
from .world import World

from .animals.sheep import Sheep
from .animals.wolf import Wolf
from .animals.antilope import Antilope
from .animals.player import Player
from .animals.fox import Fox
from .animals.cyberSheep import CyberSheep
from .animals.turtle import Turtle

from .plants.grass import Grass
from .plants.belladona import Belladona
from .plants.dandelion import Dandelion
from .plants.hogweed import Hogweed
from .plants.guarana import Guarana

class Manager:
    def __init__(self):
        self._world = None
        self._messages = []
        self.editWindow = None
        self.mainWindow = None
        self.drawList = None
        self.slider_height = None
        self.slider_width = None
        self.startDPG()

        self.choicePosX = 0
        self.choicePosY = 0
        self.popup = None

        self.font
        self.scaledFont

    
    def startDPG(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_N, callback=self.nextTurnCallback)

        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf file
            self.font = dpg.add_font("./src/fonts/JetBrainsMono-Bold.ttf", 15)
            self.scaledFont = dpg.add_font("./src/fonts/FreeMonoBoldOblique.otf", 50)
            #second_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 10)
        
        dpg.bind_font(self.scaledFont)

        self.addMainWindow()
        self.addEditWindow()      
            

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def createWorld(self, width, height):
        self._world = World(width, height, self)
    def world(self):
        return self._world
    
    def nextTurnCallback(self):
        if(self._world == None):
            return
        self.nextTurn()
        self.world().print()
        #self.drawWorld()
        self.drawChars()
        print("")

    def create_callback(self):
        self.createWorld( dpg.get_value(self.slider_height), dpg.get_value(self.slider_width))
        self.world().print()
        dpg.delete_item("Main", children_only=True)
        self.addCellButtons()
        self.drawChars()
        #self.drawWorld()
        
        print(f'World Created, {self.world().width()},{self.world().height()} ')

    def addEditWindow(self):
        with dpg.window(label="Edit window", tag = "Edit", no_close = True, no_background = False) as self.editWindow:
            dpg.add_text("Create a new World")
            dpg.add_button(label="Create", callback=self.create_callback)
            self.slider_height = dpg.add_slider_int(label="World height", max_value=30, min_value=5, default_value=5, width = 100)
            self.slider_width = dpg.add_slider_int(label="World width", max_value=30, min_value=5, default_value=5, width = 100)
            dpg.bind_item_font(self.editWindow, self.font)

    def addMainWindow(self):
        with dpg.window(tag="Main") as self.mainWindow:
            dpg.bind_item_font(self.mainWindow, self.scaledFont)
        dpg.set_primary_window("Main", True)

    def killOrganismCallback(self):
        self._world.board()[self.choicePosX][self.choicePosY].die()
        self.drawChars()
        dpg.configure_item(self.popup, show=False)
        


    def addOrganism(self, tag):
        from .functions import str_to_class
        newOrganism = str_to_class(dpg.get_value(tag))(self.choicePosX, self.choicePosY)
        if(isinstance(newOrganism, Player)):
            self._world.player(newOrganism)
        self._world.add_organism(newOrganism)
        self.drawChars()
        dpg.configure_item(self.popup, show=False)
    
    def cellButtonCallback(self, tag):

        mousePos = dpg.get_mouse_pos()
        lis = tag.split("|")
        position = [eval(i) for i in lis]
        self.choicePosX = position[0]
        self.choicePosY = position[1]

        animalList = ["Fox", "Wolf", "CyberSheep", "Sheep", "Turtle", "Antilope"]
        plantList = ["Grass", "Dandelion", "Guarana", "Hogweed", "Belladona"]
        if(self._world.player() == None):
            animalList.append("Player")

        with dpg.window(label="Edit cell", popup = True, pos = mousePos) as self.popup:
            with dpg.group(horizontal=True):
                dpg.add_text("Add Animal")
                dpg.add_combo(items = animalList, callback = self.addOrganism, popup_align_left = False, width = 50)
            with dpg.group(horizontal=True):
                dpg.add_text("Add Plant")
                dpg.add_combo(items = plantList, callback = self.addOrganism, popup_align_left = False, width = 50)

            if(self._world.board()[position[0]][position[1]] != None):
                dpg.add_button(label="Kill Organism", callback=self.killOrganismCallback)

    def addCellButtons(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        size = min(viewport_height / self._world.height(), viewport_width / self._world.width())
        size = round(size)

        if(self.drawList == None):
            with dpg.viewport_drawlist(tag = "MainDraw") as self.drawList:
                dpg.bind_item_font(self.drawList, self.scaledFont)
            
            

        for x in range(0, self._world.width()):
            for y in range(0, self._world.height()):
                    dpg.add_button(tag = (str(x) + "|" + str(y)), width = size, height = size, pos = (x * size, y * size), parent = "Main", callback = self.cellButtonCallback)
    
    def drawChars(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        size = min(viewport_height / self._world.height(), viewport_width / self._world.width())
        size = round(size)
        #with dpg.viewport_drawlist():
        #    dpg.draw_rectangle((0, 0), (viewport_width, viewport_height), fill=(0, 0, 0, 255), thickness=0, parent = "Main")

        dpg.delete_item("MainDraw", children_only=True)

        for x in range(0, self._world.width()):
            for y in range(0, self._world.height()):
                    if(self._world.board()[x][y] != None):
                        dpg.draw_text((x * size, y * size), self._world.board()[x][y].displayChar(), color=(255, 255, 255, 255), size = size, parent = "MainDraw")

    def nextTurn(self):
        from queue import PriorityQueue
        from .functions import QueueInfo
        q = PriorityQueue()

        for row in self.world().board():
            for cell in row:
                if(cell != None and cell != self._world.player()):
                    q.put(QueueInfo(cell.innitiative(), cell.index(), cell))

        while not q.empty():
            top = q.get()
            top.organism.action()
        self._world.update()
        