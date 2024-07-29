from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QPushButton, QFrame, QHBoxLayout
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

        uic.loadUi("PIG_Tracker_V3.ui", self)

        # DEFINE WIDGETS

        # INFORMATION TEXT
        self.file_name_text = self.findChild(QLabel, "file_name_text")
        
        self.date_start_text = self.findChild(QLabel, "date_start_text")
        self.time_start_text = self.findChild(QLabel, "time_start_text")

        self.date_end_text = self.findChild(QLabel, "date_end_text")
        self.time_end_text = self.findChild(QLabel, "time_end_text")
        
        self.calibration_text = self.findChild(QLabel, "calibration_text")
        self.tube_voltage_text = self.findChild(QLabel, "tube_voltage_text")

        self.threshold_text = self.findChild(QLabel, "date_threshold_text")
        self.background_text = self.findChild(QLabel, "background_text")

        self.peak_amount_text = self.findChild(QLabel, "peak_amount_text")
        self.peak_date_text = self.findChild(QLabel, "peak_date_text")
        self.peak_time_text = self.findChild(QLabel, "peak_time_text")
        self.peak_value_text = self.findChild(QLabel, "peak_value_text")


        # BUTTONS
        self.open_file_button = self.findChild(QPushButton, "open_file_button")
        self.open_file_button.clicked.connect(self.open_csv)
        self.export_file_button = self.findChild(QPushButton, "export_file_button")
        #self.export_file_button.clicked.connect(self.export_csv)

        self.peak_next_button = self.findChild(QPushButton, "peak_next_button")
        self.peak_next_button.clicked.connect(self.next_spike)
        self.peak_back_button = self.findChild(QPushButton, "peak_back_button")
        self.peak_back_button.clicked.connect(self.previous_spike)
        


        # WIDGETS FOR THE GRAPHS
        self.raw_data_frame = self.findChild(QFrame, "raw_data_graph_frame")
        self.raw_data_layout = QHBoxLayout(self.raw_data_frame)
        self.raw_data_layout.setObjectName("raw_data_layout")

        self.raw_figure = Figure()
        self.raw_canvas = FigureCanvas(self.raw_figure)
        self.raw_data_layout.addWidget(self.raw_canvas)

        self.peak_data_frame = self.findChild(QFrame, "peak_data_graph_frame")
        self.peak_data_layout = QHBoxLayout(self.peak_data_frame)
        self.peak_data_layout.setObjectName("peak_data_layout")

        self.peak_data_figure = Figure()
        self.peak_data_canvas = FigureCanvas(self.peak_data_figure)
        self.peak_data_layout.addWidget(self.peak_data_canvas)

        # SHOW ALL
        self.show()

        # IMPORTANT DATA
        self.peak_data = random.randint(50, size=(100))
        self.raw_data = random.randint(100, size=(100))

        # TRACK CURRENT SPIKE INDEX
        self.current_peak_data_index = 0
        self.peak_data_indices = []

    # GRAPHING THE RAW DATA
    def plot_raw_data(self):
        self.raw_figure.clear()
        ax = self.raw_figure.add_subplot(111)

        x = range(len(self.raw_data))
        y = self.raw_data

        ax.plot(x, y, label='raw_data')
        ax.legend()

        self.raw_canvas.draw()

    # GRAPHING THE SPIKE
    def plot_peak_data(self):
        if not self.peak_data_indices:
            self.text_left.setText("No spike indices available!")
            return

        self.peak_data_figure.clear()
        ax = self.peak_data_figure.add_subplot(111)

        index = self.peak_data_indices[self.current_peak_data_index]
        start = max(0, index - 15)
        end = min(len(self.raw_data), index + 15)
        
        x = range(start, end)
        y = self.raw_data[start:end]

        ax.plot(x, y, label='peak_data')
        ax.axvline(x=index, color='r', linestyle='--', label='Spike Index')
        ax.legend()

        self.peak_data_canvas.draw()

    # FUNCTION TO GET CSV
    def open_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            raw_data = read_csv(file_path)
            processed_data = get_spike(raw_data["raw_data"])
            self.peak_data_indices = processed_data["peak_indices"]

            FN = str(raw_data['file_name'])
            TS = str(raw_data['time_start'])
            TV = str(raw_data['tube_voltage'])
            CF = str(raw_data['calibration_factor'])

            rdata = raw_data["raw_data"]
            len_data = len(rdata)
            ldata = []
            ldata.append(len_data)

            RD = str(len(rdata))
            self.peak_data = rdata
            self.raw_data = rdata

            time = get_time(TS, ldata)

            tdays = time["elapsed_days"]
            ctime = time["current_time"]

            message = f"Filename: {FN} \nTime Start: {TS} \nTube Voltage: {TV} \nCalibration Factor: {CF} \n\nElapsed Days: {tdays} \nTime End: {ctime}"
            message2 = f"LENGTH OF DATA: {RD}"
            #self.text_right.setText(message)
            #self.text_left.setText(message2)

            if self.peak_data_indices:
                self.plot_peak_data()
                self.plot_raw_data()





    # SHOW NEXT SPIKE
    def next_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index + 1) % len(self.peak_data_indices)
            self.plot_peak_data()

    # SHOW PREVIOUS SPIKE
    def previous_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index - 1) % len(self.peak_data_indices)
            self.plot_peak_data()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
