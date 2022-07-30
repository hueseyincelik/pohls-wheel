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

    def change_item_visibility(self, items, visibility):
        for item in items:
            dpg.configure_item(item, show=visibility)

    def popup_message(self, label, message):
        with dpg.window(
            label=label,
            modal=True,
            no_move=True,
            no_close=True,
            no_resize=True,
            min_size=[200, 50],
            pos=[350, 350],
        ) as popup_window:
            dpg.add_text(message)
            dpg.add_button(
                label="CLOSE", callback=lambda: dpg.delete_item(popup_window)
            )
