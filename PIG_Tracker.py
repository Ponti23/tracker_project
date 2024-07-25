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
        
        # TEXT BROWSERS
        self.text_left = self.findChild(QTextBrowser, "text_left")
        self.text_right = self.findChild(QTextBrowser, "text_right")

        
        # BUTTONS FOR PLOTTING DATA

            # BUTTON FOR OPENING CSV
        self.open_btn = self.findChild(QPushButton, "open_btn")
        self.open_btn.clicked.connect(self.get_csv)

            # BUTTON FOR RAW DATA
        self.raw_btn = self.findChild(QPushButton, "raw_btn")
        self.raw_btn.clicked.connect(self.plot_raw)

            # BUTTON FOR SPIKE DATA
        self.spike_btn = self.findChild(QPushButton, "spike_btn")
        self.spike_btn.clicked.connect(self.plot_spike)


        # WIDGETS FOR THE GRAPHS

            # GRAPH OF THE RAW DATA
        self.data_raw_frm = self.findChild(QFrame, "data_raw_frm")
        self.data_raw_layout = QHBoxLayout(self.data_raw_frm)
        self.data_raw_layout.setObjectName("data_raw_layout")

        self.raw_figure = Figure()
        self.raw_canvas = FigureCanvas(self.raw_figure)
        self.data_raw_layout.addWidget(self.raw_canvas)

            # GRAPH OF THE SPIKE
        self.data_spike_frm = self.findChild(QFrame, "data_spike_frm")
        self.data_spike_layout = QHBoxLayout(self.data_spike_frm)
        self.data_spike_layout.setObjectName("data_spike_layout")

        self.spike_figure = Figure()
        self.spike_canvas = FigureCanvas(self.spike_figure)
        self.data_spike_layout.addWidget(self.spike_canvas)

        # SHOW ALL
        self.show()




        # IMPORTANT DATA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.spike_data = random.randint(50, size=(100))
        self.raw_data = random.randint(100, size=(100))




   # GRAPHING THE RAW DATA
    def plot_raw(self):
        
        # CLEAR CANVAS

        #self.raw_data = random.randint(100, size=(100))

        self.raw_figure.clear()
        ax = self.raw_figure.add_subplot(111)

        x = range(len(self.raw_data))
        y = self.raw_data
        
        # CREATE PLOT
        ax.plot(x, y, label='raw_data')
        """ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('PLOT OF RAW DATA')"""
        ax.legend()

        self.raw_canvas.draw()


    """# GRAPHING THE SPIKE
    def plot_spike(self):
        self.text_left.setText("YOU PRESSED SPIKE TEST BUTTON!")
        # CLEAR CANVAS
        self.spike_data = random.randint(50, size=(100))

        self.spike_figure.clear()
        ax = self.spike_figure.add_subplot(111)

        x = range(len(self.spike_data))
        y = self.spike_data
        
        # CREATE PLOT
        ax.plot(x, y, label='spike_data')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('PLOT OF SPIKE DATA')
        ax.legend()

        self.spike_canvas.draw()"""




    # FUNCTION TO GET CSV
    def get_csv(self):
        # GETTING THE FILE ADDRESS
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            raw_data = {}
            spike_data = {}
            
            raw_data = read_csv(file_path)
            processed_data = get_spike(raw_data["raw_data"])
            peak_indices = []
            peak_indices = processed_data["peak_indices"]
            print(len(peak_indices))
            #   print(spike_data["peak_indices"])
            
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




app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
