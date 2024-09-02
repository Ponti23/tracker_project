from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QPushButton, QFrame, QHBoxLayout, QSizePolicy
from PyQt5 import uic, QtCore
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ALL_CODE import *
from exporting import generate_pdf

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
        self.peak_data = []
        self.raw_data = None
        self.background_data = None
        self.threshold_data = None
        
        self.data_information = None

        self.background_data_average = None
        self.threshold_data_average = None
        self.document_information = None

        # TRACK CURRENT SPIKE INDEX
        self.current_peak_data_index = 0

    def export_pdf(self):
        # Populate peak_data list
        for index in self.peak_data_indices:
            datapoint = self.get_peak_data(index)
            self.peak_data.append(datapoint)

        print(self.peak_data)

        # Pass the actual file name text to generate_pdf
        file_name = self.file_name_text.text()
        file_name= file_name.replace(".csv", "")
        generate_pdf(self.document_information, file_name)

    def get_peak_data(self, index, before=10, after=15):
        # Ensure index is within bounds
        start = max(0, index - before)
        end = min(len(self.raw_data), index + after)
        
        # Extract the x and y values
        x_axis = list(range(start, end))
        y_axis = self.raw_data[start:end]
        
        # Create and return the result dictionary
        result = {
            'index': index,
            'x-axis': x_axis,
            'y-axis': y_axis
        }
        
        return result

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

        recording_elapsed = get_time(self.csv_data["time_start"], len(self.raw_data))
        
        return {
            'file_name':            str(self.data_information["file_name"]),
            'date_start':           str(self.data_information["date_start"]),
            'date_end' :            str(self.data_information["date_end"]),
            'time_end'  :           str(self.data_information["time_end"]),
            'calibration_factor' :  str(self.data_information["calibration_factor"].lstrip()),
            'tube_voltage' :        str(self.data_information["tube_voltage"].lstrip()),
            'recording_elapsed' :   str(recording_elapsed["elapsed_days"]),
            'total_peak' :          str(len(self.peak_data_indices)),
            'peak_data' :           self.peak_data
        }

    def open_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            file_name = QtCore.QFileInfo(file_path).fileName()
            self.csv_data = read_csv(file_path)
            processed_data = get_peak(self.csv_data["raw_data"])
            self.data_information = get_text(self.csv_data)

            self.peak_data_indices = processed_data["peak_indices"]

            self.background_data = processed_data["background_graph"]
            self.background_data_average = sum(self.background_data) / len(self.background_data) if self.background_data else None

            self.threshold_data = processed_data["threshold_graph"]
            self.threshold_data_average = sum(self.threshold_data) / len(self.threshold_data) if self.threshold_data else None

            self.date_start = self.csv_data["time_start"]
            self.raw_data = self.csv_data["raw_data"]

            self.current_peak_data_index = 0

            if self.peak_data_indices:
                self.plot_peak_data()
                self.plot_raw_data()

            # Update the text fields
            self.document_information = self.change_text()
        
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
        self.peak_date_text.setText(current_peak_time["current_time"].strftime("%d-%m-%y"))
        self.peak_time_text.setText(current_peak_time["current_time"].strftime("%H:%M:%S"))

        highest_value = max(y)
        self.peak_value_text.setText(str(highest_value))

        self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    def next_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index + 1) % len(self.peak_data_indices)
            self.plot_peak_data()
            self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    def previous_spike(self):
        if self.peak_data_indices:
            self.current_peak_data_index = (self.current_peak_data_index - 1) % len(self.peak_data_indices)
            self.plot_peak_data()
            self.peak_current_index.setText((str(self.current_peak_data_index + 1)))

    def plot_raw_data(self):
        self.raw_data_figure.clear()
        ax = self.raw_data_figure.add_subplot(111)
        
        ax.plot(self.raw_data, label='raw_data')
        ax.legend()

        self.raw_data_canvas.draw()

app = QApplication(sys.argv)
window = UI()
app.exec_()
