import dearpygui.dearpygui as dpg


class GUI:
    def __init__(self):
        self.time_data, self.oscillator_data, self.exciter_data = [], [], []
        self.measure = False

        dpg.create_context()
        dpg.create_viewport(
            title="Themenkreis 7", width=1000, height=600, resizable=False
        )
        dpg.setup_dearpygui()

        with dpg.window(tag="main_window"):
            for label, tag, pos, callback, visibility in zip(
                ["CONNECT", "START", "STOP", "SAVE"],
                ["connect_button", "start_button", "stop_button", "save_button"],
                [[25, 450], [625, 450], [750, 450], [875, 450]],
                [self.initialize, self.start, self.stop, self.save],
                [True, False, False, False],
            ):
                dpg.add_button(
                    label=label,
                    tag=tag,
                    width=100,
                    height=50,
                    pos=pos,
                    callback=callback,
                    show=visibility,
                )

            with dpg.group(horizontal=True):
                dpg.add_text("COM", tag="com_text", pos=[25, 510])
                dpg.add_input_text(
                    tag="com_port_input",
                    no_spaces=True,
                    decimal=True,
                    width=55,
                    default_value="4",
                )

                dpg.add_text("FILE NAME", tag="file_name", pos=[625, 510], show=False)
                dpg.add_input_text(
                    tag="file_name_input",
                    no_spaces=True,
                    width=260,
                    default_value="data.txt",
                    show=False,
                )

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
