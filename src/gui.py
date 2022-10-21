from pathlib import Path
from threading import Thread
from time import perf_counter

import dearpygui.dearpygui as dpg
import numpy as np

from . import arduino


class GUI:
    def __init__(self):
        self.time_data, self.oscillator_data, self.exciter_data = [], [], []
        self.exciter_frequency = 0
        self.measure = False

        dpg.create_context()
        dpg.create_viewport(
            title="Themenkreis 7 — Pohl's Wheel",
            width=1000,
            height=600,
            resizable=False,
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

            dpg.configure_item(item="connect_button", width=200)

            with dpg.group(horizontal=True):
                dpg.add_text("PORT", tag="serial_port_text", pos=[25, 510])
                dpg.add_input_text(
                    tag="serial_port_input",
                    no_spaces=True,
                    width=150,
                    default_value="/dev/ttyACM0",
                )

                dpg.add_text("FILE NAME", tag="file_name", pos=[625, 510], show=False)
                dpg.add_input_text(
                    tag="file_name_input",
                    no_spaces=True,
                    width=260,
                    default_value="Desktop/data.txt",
                    show=False,
                )

                dpg.add_text(
                    "EXCITER FREQUENCY",
                    tag="exciter_frequency",
                    pos=[625, 545],
                    show=False,
                )
                dpg.add_input_int(
                    tag="exciter_frequency_input",
                    width=75,
                    default_value=0,
                    min_value=0,
                    step=0,
                    min_clamped=True,
                    show=False,
                )
                dpg.add_text("mHz", tag="exciter_frequency_mHz", show=False)

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
                "serial_port_text",
                "serial_port_input",
                "file_name",
                "file_name_input",
                "exciter_frequency",
                "exciter_frequency_input",
                "exciter_frequency_mHz",
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
            pos=[400, 250],
        ) as popup_window:
            dpg.add_text(message)
            dpg.add_button(
                label="CLOSE", callback=lambda: dpg.delete_item(popup_window)
            )

    def initialize(self):
        try:
            self.serial_port = dpg.get_value("serial_port_input")
            self.ardn = arduino.Arduino(self.serial_port)
        except:
            self.popup_message(
                "Arduino Connection", "Error connecting to Arduino!\nCheck serial port!"
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
                    "exciter_frequency_mHz",
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
                    "exciter_frequency_mHz",
                ],
                True,
            )

    def acquire(self):
        self.time_data, self.oscillator_data, self.exciter_data = [], [], []
        self.exciter_frequency = dpg.get_value("exciter_frequency_input")

        if self.exciter_frequency > 0:
            self.ardn.write(f"F{self.exciter_frequency*1.744}\n")

        timer = perf_counter()

        while self.measure:
            try:
                _, oscillator_cur_val, exciter_cur_val = (
                    self.ardn.read().decode("UTF-8").rstrip("\n").split(",")
                )
            except:
                self.stop(join=False)
                self.popup_message(
                    "Arduino Connection",
                    "Error: not enough values to unpack (expected 3)!\nTry restarting the Arduino!",
                )
            else:
                self.time_data.append(perf_counter() - timer)
                self.oscillator_data.append(int(oscillator_cur_val))
                self.exciter_data.append(int(exciter_cur_val))

                dpg.set_value("oscillator_plot", [self.time_data, self.oscillator_data])
                dpg.set_value("exciter_plot", [self.time_data, self.exciter_data])

                dpg.fit_axis_data("oscillator_x_axis")
                dpg.fit_axis_data("oscillator_y_axis")

                dpg.fit_axis_data("exciter_x_axis")
                dpg.fit_axis_data("exciter_y_axis")

    def start(self):
        if self.measure:
            self.stop()
        else:
            try:
                self.ardn
            except:
                self.ardn = arduino.Arduino(self.serial_port)

            self.measure = True
            self.acquire_thread = Thread(target=self.acquire)
            self.acquire_thread.start()

    def stop(self, join=True):
        self.measure = False
        self.ardn.write("F0\n")

        if join:
            self.acquire_thread.join()

        del self.ardn

    def save(self):
        if self.measure:
            self.stop()

        self.data = np.column_stack(
            (self.time_data, self.oscillator_data, self.exciter_data)
        )
        self.filename = f"{dpg.get_value('file_name_input')}{'.txt' if not dpg.get_value('file_name_input').lower().endswith('.txt') else ''}"
        self.header = f"Time t [s]\tAmplitude A (Oscillator) [arb. u.]\tAmplitude A (Exciter: {self.exciter_frequency}mHz) [arb. u.]"

        try:
            np.savetxt(self.filename, self.data, delimiter="\t", header=self.header)
        except:
            self.popup_message(
                "Saving Data", "Error saving data to disk!\nCheck file name!"
            )
        else:
            self.popup_message(
                "Saving Data", f"Successfully saved {Path(self.filename).name} to disk!"
            )
