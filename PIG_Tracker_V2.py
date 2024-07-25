from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser, QFileDialog, QPushButton, QFrame, QHBoxLayout
from PyQt5 import uic, QtCore
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import random

from ALL_CODE import *


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("PIG_Tracker_V2.ui", self)

        # DEFINE WIDGETS

        # TEXT BROWSERS
        self.text_left = self.findChild(QTextBrowser, "text_left")
        self.text_right = self.findChild(QTextBrowser, "text_right")

        # BUTTONS FOR PLOTTING DATA
        self.open_btn = self.findChild(QPushButton, "open_btn")
        self.open_btn.clicked.connect(self.get_csv)

        self.raw_btn = self.findChild(QPushButton, "raw_btn")
        self.raw_btn.clicked.connect(self.plot_raw)

        self.spike_btn = self.findChild(QPushButton, "spike_btn")
        self.spike_btn.clicked.connect(self.plot_spike)

        self.next_btn = self.findChild(QPushButton, "next_btn")
        self.next_btn.clicked.connect(self.next_spike)

        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.previous_spike)

        # WIDGETS FOR THE GRAPHS
        self.data_raw_frm = self.findChild(QFrame, "data_raw_frm")
        self.data_raw_layout = QHBoxLayout(self.data_raw_frm)
        self.data_raw_layout.setObjectName("data_raw_layout")

        self.raw_figure = Figure()
        self.raw_canvas = FigureCanvas(self.raw_figure)
        self.data_raw_layout.addWidget(self.raw_canvas)

        self.data_spike_frm = self.findChild(QFrame, "data_spike_frm")
        self.data_spike_layout = QHBoxLayout(self.data_spike_frm)
        self.data_spike_layout.setObjectName("data_spike_layout")

        self.spike_figure = Figure()
        self.spike_canvas = FigureCanvas(self.spike_figure)
        self.data_spike_layout.addWidget(self.spike_canvas)

        # SHOW ALL
        self.show()

        # IMPORTANT DATA
        self.spike_data = random.randint(50, size=(100))
        self.raw_data = random.randint(100, size=(100))

        # TRACK CURRENT SPIKE INDEX
        self.current_spike_index = 0
        self.spike_indices = []

    # GRAPHING THE RAW DATA
    def plot_raw(self):
        self.raw_figure.clear()
        ax = self.raw_figure.add_subplot(111)

        x = range(len(self.raw_data))
        y = self.raw_data

        ax.plot(x, y, label='raw_data')
        ax.legend()

        self.raw_canvas.draw()

    # GRAPHING THE SPIKE
    def plot_spike(self):
        if not self.spike_indices:
            self.text_left.setText("No spike indices available!")
            return

        self.spike_figure.clear()
        ax = self.spike_figure.add_subplot(111)

        index = self.spike_indices[self.current_spike_index]
        start = max(0, index - 15)
        end = min(len(self.raw_data), index + 15)
        
        x = range(start, end)
        y = self.raw_data[start:end]

        ax.plot(x, y, label='spike_data')
        ax.axvline(x=index, color='r', linestyle='--', label='Spike Index')
        ax.legend()

        self.spike_canvas.draw()

    # FUNCTION TO GET CSV
    def get_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            raw_data = read_csv(file_path)
            processed_data = get_spike(raw_data["raw_data"])
            self.spike_indices = processed_data["peak_indices"]

            FN = str(raw_data['file_name'])
            TS = str(raw_data['time_start'])
            TV = str(raw_data['tube_voltage'])
            CF = str(raw_data['calibration_factor'])

            rdata = raw_data["raw_data"]
            len_data = len(rdata)
            ldata = []
            ldata.append(len_data)

            RD = str(len(rdata))
            self.spike_data = rdata
            self.raw_data = rdata

            time = get_time(TS, ldata)

            tdays = time["elapsed_days"]
            ctime = time["current_time"]

            message = f"Filename: {FN} \nTime Start: {TS} \nTube Voltage: {TV} \nCalibration Factor: {CF} \n\nElapsed Days: {tdays} \nTime End: {ctime}"
            message2 = f"LENGTH OF DATA: {RD}"
            self.text_right.setText(message)
            self.text_left.setText(message2)

            if self.spike_indices:
                self.plot_spike()

    # SHOW NEXT SPIKE
    def next_spike(self):
        if self.spike_indices:
            self.current_spike_index = (self.current_spike_index + 1) % len(self.spike_indices)
            self.plot_spike()

    # SHOW PREVIOUS SPIKE
    def previous_spike(self):
        if self.spike_indices:
            self.current_spike_index = (self.current_spike_index - 1) % len(self.spike_indices)
            self.plot_spike()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
