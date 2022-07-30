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

        with dpg.font_registry():
            default_font = dpg.add_font("fonts/HelveticaNeue-Regular.otf", 18 * 4)
            bold_font = dpg.add_font("fonts/HelveticaNeue-Bold.otf", 18 * 4)

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

                dpg.add_text(
                    "EXCITER FREQUENCY",
                    tag="exciter_frequency",
                    pos=[625, 545],
                    show=False,
                )
                dpg.add_input_text(
                    tag="exciter_frequency_input",
                    no_spaces=True,
                    decimal=True,
                    width=75,
                    default_value="0",
                    show=False,
                )
                dpg.add_text("MHz", tag="exciter_frequency_MHz", show=False)

            with dpg.plot(label="Oscillator", height=400, width=475, pos=[25, 25]):
                dpg.add_plot_axis(
                    dpg.mvXAxis, label="Time t [s]", tag="oscillator_x_axis"
                )
                dpg.add_plot_axis(
                    dpg.mvYAxis, label=r"Amplitude A [arb. u.]", tag="oscillator_y_axis"
                )
                dpg.add_line_series(
                    self.time_data,
                    self.oscillator_data,
                    parent="oscillator_y_axis",
                    tag="oscillator_plot",
                )

            with dpg.plot(label="Exciter", height=400, width=475, pos=[500, 25]):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time t [s]", tag="exciter_x_axis")
                dpg.add_plot_axis(
                    dpg.mvYAxis, label="Amplitude A [arb. u.]", tag="exciter_y_axis"
                )
                dpg.add_line_series(
                    self.time_data,
                    self.exciter_data,
                    parent="exciter_y_axis",
                    tag="exciter_plot",
                )

            dpg.bind_font(default_font)
            dpg.set_global_font_scale(0.25)

            for item in [
                "connect_button",
                "start_button",
                "stop_button",
                "save_button",
                "com_text",
                "com_port_input",
                "file_name",
                "file_name_input",
                "exciter_frequency",
                "exciter_frequency_input",
                "exciter_frequency_MHz",
            ]:
                dpg.bind_item_font(item, bold_font)

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

    def initialize(self, sender, data):
        try:
            self.com_port = dpg.get_value("com_port_input")
            self.ardn = arduino(f"COM{self.com_port}")
        except:
            self.popup_message(
                "Arduino Connection", "Error connecting to Arduino!\nCheck COM port!"
            )
            self.change_item_visibility(
                [
                    "start_button",
                    "stop_button",
                    "save_button",
                    "file_name",
                    "file_name_input",
                    "exciter_frequency",
                    "exciter_frequency_input",
                    "exciter_frequency_MHz",
                ],
                False,
            )
        else:
            self.popup_message(
                "Arduino Connection", "Successfully connected to Arduino!"
            )
            self.change_item_visibility(
                [
                    "start_button",
                    "stop_button",
                    "save_button",
                    "file_name",
                    "file_name_input",
                    "exciter_frequency",
                    "exciter_frequency_input",
                    "exciter_frequency_MHz",
                ],
                True,
            )
