import dearpygui.dearpygui as dpg


class GUI:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(
            title="Themenkreis 7", width=1000, height=600, resizable=False
        )
        dpg.setup_dearpygui()

        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        dpg.destroy_context()
