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

from queue import PriorityQueue

class Manager:
    def __init__(self):
        self._world = None

        self.messageWindow = None
        self.editWindow = None
        self.mainWindow = None
        self.drawList = None
        self.infoWindow = None
        #self.buttonDrawList = None
        self.slider_height = None
        self.slider_width = None

        self.turnQueue = PriorityQueue()
        
        self.choicePosX = 0
        self.choicePosY = 0
        self.popup = None

        self.font = None
        self.scaledFont = None

        self.startDPG()

    
    def startDPG(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_N, callback=self.nextTurnCallback)
            dpg.add_key_press_handler(dpg.mvKey_W, callback=self.upMove)
            dpg.add_key_press_handler(dpg.mvKey_S, callback=self.downMove)
            dpg.add_key_press_handler(dpg.mvKey_A, callback=self.leftMove)
            dpg.add_key_press_handler(dpg.mvKey_D, callback=self.rightMove)

            dpg.add_key_press_handler(dpg.mvKey_R, callback=self.useAbility)

        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf file
            self.font = dpg.add_font("./src/fonts/JetBrainsMono-Bold.ttf", 15)
            self.scaledFont = dpg.add_font("./src/fonts/FreeMonoBoldOblique.otf", 80)
            #second_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 10)
        
        dpg.bind_font(self.font)

        self.addMainWindow()
        self.addEditWindow()    
        self.addMessageWindow()  
            

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def createWorld(self, width, height):
        self._world = World(width, height, self)
    def createEmptyWorld(self, width, height):
        self._world = World(width, height, self, False)
    def world(self):
        return self._world
    
    def baseMove(self, x, y):
        from .functions import Vector2
        player = self._world.player()
        if(player == None):
            return
        vector = Vector2(player.positionX() + x, player.positionY() + y) 
        if(not self._world.isInBounds(vector)):
            return

        from .functions import QueueInfo
        player.move(Vector2(player.positionX() + x, player.positionY() + y))

        self.turnQueue.put(QueueInfo(player.innitiative(), player.index(), player))
        self.nextTurnCallback()
    
    def upMove(self):
        self.baseMove(-1, 0)
    def downMove(self):
        self.baseMove(1, 0)
    def leftMove(self):
        self.baseMove(0, -1)
    def rightMove(self):
        self.baseMove(0, 1)

    def addMessage(self, message):
        dpg.add_text(default_value = message, parent = self.messageWindow)

    def clearMessages(self):
        dpg.delete_item(self.messageWindow, children_only = True)



    def nextTurnCallback(self):
        if(self._world == None):
            return
        self.clearMessages()
        self.nextTurn()
        self.drawChars()

    def create_callback(self):
        if(dpg.get_value("Empty") == False):
            self.createWorld(dpg.get_value(self.slider_height), dpg.get_value(self.slider_width))
        else:
            self.createEmptyWorld(dpg.get_value(self.slider_height), dpg.get_value(self.slider_width))
        self.world().update()
        self.addPlayerInfoWindow()
        self.addCellButtons()
        self.drawChars()

    def useAbility(self):
        if(not self._world.playerAlive()):
            return
        if(not self._world.playerAbilityAvaible()):
            return
        self.world().playerUseAbility()
        self.world().update()
        self.updateInfo()
        self.addMessage("Player used ability")


    def saveCallback(self):
        pass

    def loadCallback(self):
        with dpg.file_dialog(tag="file_dialog_id", directory_selector=False, width = 600, height = 400):
            dpg.add_file_extension(".save")

    def updateInfo(self):
        dpg.configure_item("PlayerStatus", default_value = "Player alive: " + str(self._world.playerAlive()))
        dpg.configure_item("CanUseAbility", default_value = "Can use ability: " + str(self._world.playerAbilityAvaible()))
        dpg.configure_item("AbilityActive", default_value = "Ability active: " + str(self._world.playerAbilityOn()))

    def addPlayerInfoWindow(self):
        if(self.infoWindow != None):
            return
        with dpg.window(label="World Info", tag = "Info", no_close = True, width = 300, height = 200, pos = (100, 100)) as self.infoWindow:
            dpg.add_text("Player alive: " + str(self._world.playerAlive()), tag = "PlayerStatus")
            dpg.add_text("Can use ability: " + str(self._world.playerAbilityAvaible()), tag = "CanUseAbility")
            dpg.add_text("Ability active: " + str(self._world.playerAbilityOn()), tag = "AbilityActive")
            dpg.add_text("Movement: WSAD+QE Next turn: N Ability: R")
            dpg.bind_item_font(self.editWindow, self.font)

    def addEditWindow(self):
        with dpg.window(label="Edit window", tag = "Edit", no_close = True,width = 300, height = 200, pos = (100, 100)) as self.editWindow:
            dpg.add_text("Create a new World")
            dpg.add_button(label="Create", callback=self.create_callback)
            dpg.add_checkbox(label = "Empty World", tag = "Empty", default_value = False)
            self.slider_height = dpg.add_slider_int(label="World height", max_value=30, min_value=5, default_value=5, width = 100)
            self.slider_width = dpg.add_slider_int(label="World width", max_value=30, min_value=5, default_value=5, width = 100)

            with dpg.group(horizontal = True):
                dpg.add_button(label="Save", callback=self.saveCallback)
                dpg.add_button(label="Load", callback=self.loadCallback)

            dpg.bind_item_font(self.editWindow, self.font)
            #dpg.set_primary_window("Edit", True)

    def addMainWindow(self):
        with dpg.window(tag="Main") as self.mainWindow:
            dpg.bind_item_font(self.mainWindow, self.scaledFont)
        dpg.set_primary_window("Main", True)
        #with dpg.viewport_drawlist(tag="ButtonDraw") as self.buttonDrawList:
        #    pass

    def addMessageWindow(self):
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()

        with dpg.window(tag="Message", no_close = True, width = 300, height = 300, pos = (100, viewport_height - 200)) as self.messageWindow:
            dpg.bind_item_font(self.mainWindow, self.font)

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
        self.choicePosX = position[1]
        self.choicePosY = position[0]

        animalList = ["Fox", "Wolf", "CyberSheep", "Sheep", "Turtle", "Antilope"]
        plantList = ["Grass", "Dandelion", "Guarana", "Hogweed", "Belladona"]
        if(self._world.player() == None):
            animalList.append("Player")
        with dpg.window(label="Edit cell", popup = True, pos = mousePos) as self.popup:
            dpg.bind_item_font(self.popup, self.font)
            if(self._world.board()[position[1]][position[0]] != None):
                organism = self._world.board()[position[1]][position[0]]
                dpg.add_text(organism.name())
                dpg.add_text("Strength: " + str(organism.strength()) + " Innitiative: " + str(organism.innitiative()))
                dpg.add_button(label="Kill Organism", callback=self.killOrganismCallback)
            else:
                with dpg.group(horizontal=True):
                    dpg.add_text("Add Animal")
                    dpg.add_combo(items = animalList, callback = self.addOrganism, popup_align_left = False, width = 50)
                with dpg.group(horizontal=True):
                    dpg.add_text("Add Plant")
                    dpg.add_combo(items = plantList, callback = self.addOrganism, popup_align_left = False, width = 50)
            

    def addCellButtons(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        size = min(viewport_height / self._world.width(), viewport_width / self._world.height())
        size = round(size) - 5

        dpg.delete_item("Main", children_only = True)
        self.drawList = None

        boardEnd = min(viewport_width-200, self._world.width() * size + size)

        dpg.configure_item("Edit", pos = (boardEnd, 100))
        dpg.configure_item("Message", pos = (boardEnd, viewport_height-400))
        dpg.configure_item("Info", pos = (boardEnd, viewport_height/2-150))

        for x in range(0, self._world.width()):
            for y in range(0, self._world.height()):
                    dpg.add_button(tag = (str(y) + "|" + str(x)), width = size, height = size, pos = (y * size, x * size), parent = "Main", callback = self.cellButtonCallback)
                    #dpg.bind_item_font(str(x) + "|" + str(y), self.scaledFont)
    
    def drawChars(self):
        self.updateInfo()
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        size = min(viewport_height / self._world.width(), viewport_width / self._world.height())
        size = round(size) - 5

        if(self.drawList == None):
            with dpg.drawlist(tag = "MainDraw", parent = "Main", height = viewport_height, width = viewport_width) as self.drawList:
                dpg.bind_item_font(self.drawList, self.scaledFont)

        dpg.delete_item("MainDraw", children_only=True)
        for x in range(0, self._world.width()):
            for y in range(0, self._world.height()):
                    if(self._world.board()[x][y] != None):
                        
                        displayColor = self._world.board()[x][y].displayColour()
                        #dpg.configure_item(str(x) + "|" + str(y), label=self.world().board()[x][y].displayChar())
                        drawTag = dpg.draw_text((y * size, x * size), self._world.board()[x][y].displayChar(), color = displayColor, size = size, parent = "MainDraw")
                        dpg.bind_item_font(drawTag, self.scaledFont)


    def nextTurn(self):
        from .functions import QueueInfo

        for row in self.world().board():
            for cell in row:
                if(cell != None and cell != self._world.player()):
                    self.turnQueue.put(QueueInfo(cell.innitiative(), cell.index(), cell))

        while not self.turnQueue.empty():
            top = self.turnQueue.get()
            if(not top.organism.isDead()):
                top.organism.action()
        self.world().nextTurn()
        self._world.update()
        self.updateInfo()

    
        