import dearpygui.dearpygui as dpg

import world as wc



def save_callback():
    world = wc.World(dpg.get_value(slider_height), dpg.get_value(slider_width))
    world.print()
    print(f'World Created, {world.width},{world.height} ')

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Edit window"):
    dpg.add_text("Create a new World")
    dpg.add_button(label="Create", callback=save_callback)
    slider_height = dpg.add_slider_int(label="World height", max_value=30, min_value=5, default_value=5)
    slider_width = dpg.add_slider_int(label="World width", max_value=30, min_value=5, default_value=5)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()