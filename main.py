from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QPushButton, QFrame, QHBoxLayout, QSizePolicy
from PyQt5 import uic, QtCore
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from all_code import *
from exporting import export_pdf

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("main.ui", self)

        
        ########################################
        ####            TEXTS               ####
        ########################################

        self.file_name_text = self.findChild(QLabel, "file_name_text")

        self.date_start_text = self.findChild(QLabel, "date_start_text")
        self.time_start_text = self.findChild(QLabel, "time_start_text")
        self.date_end_text = self.findChild(QLabel, "date_end_text")
        self.time_end_text = self.findChild(QLabel, "time_end_text")
        self.calibration_text = self.findChild(QLabel, "calibration_text")
        self.tube_voltage_text = self.findChild(QLabel, "tube_voltage_text")

        self.threshold_text = self.findChild(QLabel, "threshold_text")
        self.background_text = self.findChild(QLabel, "background_text")

        self.peak_current_index = self.findChild(QLabel, "peak_current_index")
        self.peak_total_index = self.findChild(QLabel, "peak_total_index")

        self.peak_date_text = self.findChild(QLabel, "peak_date_text")
        self.peak_time_text = self.findChild(QLabel, "peak_time_text")

        self.peak_value_text = self.findChild(QLabel, "peak_value_text")

        ########################################
        ####            BUTTONS             ####
        ########################################

        # OPENNING FILE
        self.open_file_button = self.findChild(QPushButton, "open_file_button")
        self.open_file_button.clicked.connect(self.open_csv)

        # EXPORTING FILE
        self.export_file_button = self.findChild(QPushButton, "export_file_button")
        self.export_file_button.clicked.connect(self.export_pdf)

        # NEXT PEAK
        self.peak_next_button = self.findChild(QPushButton, "peak_next_button")
        self.peak_next_button.clicked.connect(self.next_spike)

        # PREVIOUS PEAK
        self.peak_back_button = self.findChild(QPushButton, "peak_back_button")
        self.peak_back_button.clicked.connect(self.previous_spike)

        ########################################
        ####        GRAPHING WIDGETS        ####
        ########################################

        self.raw_data_frame = self.findChild(QFrame, "raw_data_graph_frame")
        self.raw_data_layout = QHBoxLayout(self.raw_data_frame)
        self.raw_data_layout.setObjectName("raw_data_layout")
        self.raw_data_figure = Figure()
        self.raw_data_canvas = FigureCanvas(self.raw_data_figure)
        self.raw_data_canvas.setFixedSize(981, 391)  # Set canvas size
        self.raw_data_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.raw_data_layout.addWidget(self.raw_data_canvas, 0, QtCore.Qt.AlignCenter)  # Center the canvas

        self.peak_data_frame = self.findChild(QFrame, "peak_data_graph_frame")
        self.peak_data_layout = QHBoxLayout(self.peak_data_frame)
        self.peak_data_layout.setObjectName("peak_data_layout")
        self.peak_data_figure = Figure()
        self.peak_data_canvas = FigureCanvas(self.peak_data_figure)
        self.peak_data_layout.addWidget(self.peak_data_canvas)

        # SHOW ALL
        self.show()

        # DATA
        self.peak_data = None
        self.raw_data = None
        self.background_data = None
        self.threshold_data = None
        self.data_information = None
        self.background_data_average = None
        self.threshold_data_average = None

        # TRACK CURRENT SPIKE INDEX
        self.current_peak_data_index = 0
        self.peak_data_indices = []

    def export_pdf(self):
        export_pdf = export_pdf

    def change_text(self):
        self.file_name_text.setText(self.data_information["file_name"])
        self.date_start_text.setText(self.data_information["date_start"])
        self.time_start_text.setText(self.data_information["time_start"])
        self.date_end_text.setText(self.data_information["date_end"])
        self.time_end_text.setText(self.data_information["time_end"])
        self.calibration_text.setText(self.data_information["calibration_factor"].lstrip())
        self.tube_voltage_text.setText(self.data_information["tube_voltage"].lstrip())

        self.peak_total_index.setText(str(len(self.peak_data_indices)))

        # Update background and threshold text with the average values
        if self.background_data_average is not None:
            self.background_text.setText(f"{self.background_data_average:.2f}")
        else:
            self.background_text.setText("N/A")

        if self.threshold_data_average is not None:
            self.threshold_text.setText(f"{self.threshold_data_average:.2f}")
        else:
            self.threshold_text.setText("N/A")

    # FUNCTION TO GET CSV
    def open_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            csv_data = read_csv(file_path)
            processed_data = get_peak(csv_data["raw_data"])
            self.data_information = get_text(csv_data)

            self.peak_data_indices = processed_data["peak_indices"]

            self.background_data = processed_data["background_graph"]
            self.background_data_average = sum(self.background_data) / len(self.background_data) if self.background_data else None

            self.threshold_data = processed_data["threshold_graph"]
            self.threshold_data_average = sum(self.threshold_data) / len(self.threshold_data) if self.threshold_data else None

            self.date_start = csv_data["time_start"]
            self.raw_data = csv_data["raw_data"]

            self.current_peak_data_index = 0

            if self.peak_data_indices:
                self.plot_peak_data()
                self.plot_raw_data()

            # Update the text fields
            self.change_text()

    # GRAPHING THE PEAK
    def plot_peak_data(self):
        if not self.peak_data_indices:
            self.text_left.setText("No spike indices available!")
            return

        self.peak_data_figure.clear()
        ax = self.peak_data_figure.add_subplot(111)

        self.peak_index = self.peak_data_indices[self.current_peak_data_index]
        start = max(0, self.peak_index - 10)
        end = min(len(self.raw_data), self.peak_index + 15)

        x = range(start, end)
        y = self.raw_data[start:end]

        ax.plot(x, y, label='peak_data')
        ax.legend()

        self.peak_data_canvas.draw()

        current_peak_time = get_time(self.date_start, self.peak_index)
        self.peak_date_text.setText(current_peak_time["current_time"].strftime("%m-%d-%y"))
        self.peak_time_text.setText(current_peak_time["current_time"].strftime("%H:%M:%S"))

        highest_value = max(y)
        self.peak_value_text.setText(str(highest_value))

        self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    # SHOW NEXT SPIKE
    def next_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index + 1) % len(self.peak_data_indices)
            self.plot_peak_data()
            self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    # SHOW PREVIOUS SPIKE
    def previous_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index - 1) % len(self.peak_data_indices)
            self.plot_peak_data()
            self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    # GRAPHING THE RAW DATA
    def plot_raw_data(self):
        self.raw_data_figure.clear()
        ax = self.raw_data_figure.add_subplot(111)

        x = range(len(self.raw_data))
        y = self.raw_data

        ax.plot(x, y, label='raw_data')
        ax.legend()

        self.raw_data_canvas.draw()

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
