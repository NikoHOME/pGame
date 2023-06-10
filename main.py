import dearpygui.dearpygui as dpg

import world as wc
import organism as org



def create_callback():
    world = wc.World(dpg.get_value(slider_height), dpg.get_value(slider_width))
    test = org.Organism(1, 1, 3, 4)
    world.add_organismn(test)
    world.print()
    print(f'World Created, {world.width},{world.height} ')

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Edit window"):
    dpg.add_text("Create a new World")
    dpg.add_button(label="Create", callback=create_callback)
    slider_height = dpg.add_slider_int(label="World height", max_value=30, min_value=5, default_value=5)
    slider_width = dpg.add_slider_int(label="World width", max_value=30, min_value=5, default_value=5)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()