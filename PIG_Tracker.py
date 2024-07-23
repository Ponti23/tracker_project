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

        uic.loadUi("PIG_Tracker.ui", self)

        # DEFINE WIDGETS
        self.text_left = self.findChild(QTextBrowser, "text_left")
        self.text_right = self.findChild(QTextBrowser, "text_right")

        # BUTTON FOR OPENING CSV
        self.open_btn = self.findChild(QPushButton, "open_btn")
        self.open_btn.clicked.connect(self.get_csv)
        
        # BUTTON FOR PLOTTING DATA (IN TEST)
        self.test_button = self.findChild(QPushButton, "test_button")
        self.test_button.clicked.connect(self.plotData)

        # ANOTHER
        self.test_button2 = self.findChild(QPushButton, "test_button2")
        self.test_button2.clicked.connect(self.plotData2)


        # DEFINE WIDGETS FOR PLOTTING
        self.data_spike_frm = self.findChild(QFrame, "data_spike_frm")
        self.data_spike_layout = QHBoxLayout(self.data_spike_frm)
        self.data_spike_layout.setObjectName("data_spike_layout")

        self.spike_figure = Figure()
        self.spike_canvas = FigureCanvas(self.spike_figure)
        self.data_spike_layout.addWidget(self.spike_canvas)

        self.data_graph_frm = self.findChild(QFrame, "data_graph_frm")
        self.data_graph_layout = QHBoxLayout(self.data_graph_frm)
        self.data_graph_layout.setObjectName("data_graph_layout")

        self.graph_figure = Figure()
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.data_graph_layout.addWidget(self.graph_canvas)

        self.show()

        self.spike_data = random.randint(50, size=(100))
        self.graph_data = random.randint(100, size=(100))  # <--- NEW LINE

    # FUNCTION TO PLOT ON SPIKE CANVAS
    def plotData(self):
        # CLEAR CANVAS

        self.spike_data = random.randint(50, size=(100))

        self.spike_figure.clear()
        ax = self.spike_figure.add_subplot(111)  # <--- CHANGED LINE

        x = range(len(self.spike_data))
        y = self.spike_data
        
        # CREATE PLOT
        ax.plot(x, y, label='col2')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('PLOT OF DATA')
        ax.legend()

        self.spike_canvas.draw()

    # FUNCTION TO PLOT ON GRAPH CANVAS
    def plotData2(self):
        # CLEAR CANVAS

        self.graph_data = random.randint(100, size=(100))

        self.graph_figure.clear()
        ax = self.graph_figure.add_subplot(111)  # <--- CHANGED LINE

        x = range(len(self.graph_data))
        y = self.graph_data
        
        # CREATE PLOT
        ax.plot(x, y, label='col2')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('PLOT OF DATA')
        ax.legend()

        self.graph_canvas.draw()

    # FUNCTION TO GET CSV
    def get_csv(self):
        # GETTING THE FILE ADDRESS
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            raw_data = {}
            spike_data = {}
            
            raw_data = read_csv(file_path)
            #   spike_data = get_spike(raw_data["real_data"])
            #   print(spike_data["peak_indices"])
            
            FN = str(raw_data['file_name'])
            TS = str(raw_data['time_start'])
            TV = str(raw_data['tube_voltage'])
            CF = str(raw_data['calibration_factor'])

            rdata = raw_data["real_data"]
            len_data = len(rdata)
            ldata = []
            ldata.append(len_data)

            RD = str(len(rdata))
            self.spike_data = rdata
            self.graph_data = rdata  # <--- NEW LINE

            time = get_time(TS, ldata)

            tdays = time["elapsed_days"]
            ctime = time["current_time"]

            message = f"Filename: {FN} \nTime Start: {TS} \nTube Voltage: {TV} \nCalibration Factor: {CF} \n\nElapsed Days: {tdays} \nTime End: {ctime}"
            message2 = f"LENGTH OF DATA: {RD}"
            self.text_right.setText(message)
            self.text_left.setText(message2)




app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
