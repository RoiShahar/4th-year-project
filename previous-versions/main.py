import serial
import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
# import PySimpleGUI as sg
from tkinter import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout


arduino_port = 'COM4' # need to be changed according to input
baud_rate = 9600

def read_serial_data(serial_port):
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        ser.flush()
        lines = []
        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "---":
                break
            lines.append(line)
        print(lines)
        return lines

def parse_sensor_values(sensor_values):
    matrix = np.zeros((1, 16), dtype=int)
    for i in range(len(sensor_values)):
        val = sensor_values[i]
        pin_number = i
        matrix[0, pin_number] = int(val)
    # gradient_mat = np.zeros((5,5), dtype=int)
    # for row in gradient_mat:
    #     for col in gradient_mat[0]:
    #         if row % 2 == 0 and col % 2 == 0:
    #             gradient_mat[row][col] = matrix[row][col]
    #         else gradient_mat[row][col]
    return matrix

def save_sensor_data(kind, carateristics, data_matrices, duration): # time in seconds
    # Create a folder for the specified number (e.g., "Folder1")
    dfs = [pd.DataFrame(matrix) for matrix in data_matrices]
    result_df = pd.concat(dfs, ignore_index=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}__{kind}__{carateristics}__{duration}sec"

    result_df.to_csv(f"C:/Users/Roi_Shahar/Desktop/לימודים/סמסטר ח/data_fro_proj/{filename}.csv", index=False)

    # folder_name = f"{folder_kind}"
    # os.makedirs(folder_name, exist_ok=True)

    # Generate a filename with the current timestamp

    # Save the sensor data (assuming 'sensor_data' is your matrix)


def record_for_duration(kind, carateristics, duration_seconds):
    start_time = time.time()  # Get the current time
    end_time = start_time + duration_seconds
    # raw_sensor_values = ''
    matrices = []
    while time.time() < end_time:
        raw_sensor_values = read_serial_data(arduino_port)
        matrix = parse_sensor_values(raw_sensor_values)
        matrices.append(matrix)
    save_sensor_data(kind, carateristics, matrices, duration_seconds)
    print("Done successfully")
        # raw_sensor_values = append_to_previous_line(raw_sensor_values, ", ".join(read_serial_data(arduino_port)))
    # print(raw_sensor_values)
    # return raw_sensor_values
    # return matrices

# def append_to_previous_line(current_line, new_line):
#     # Add a newline character and concatenate the new line
#     updated_line = current_line + "\n" + new_line
#     return updated_line


def record_button_click():
    characteristics = characteristics_line.text()
    position = position_line.text()
    duration = int(duration_line.text())
    record_for_duration(position, characteristics, duration)
    print(f"Recorded: Characteristics = {characteristics}, Position = {position}, Duration: {duration}")

app = QApplication([])
window = QWidget()
window.setWindowTitle("My Simple UI")

characteristics_label = QLabel("Characteristics:")
characteristics_line = QLineEdit()

position_label = QLabel("Position:")
position_line = QLineEdit()

duration_label = QLabel("Duration (sec):")
duration_line = QLineEdit()

record_button = QPushButton("Record")
record_button.clicked.connect(record_button_click)

layout = QVBoxLayout()
layout.addWidget(characteristics_label)
layout.addWidget(characteristics_line)
layout.addWidget(position_label)
layout.addWidget(position_line)
layout.addWidget(duration_label)
layout.addWidget(duration_line)
layout.addWidget(record_button)

window.setLayout(layout)
window.show()

app.exec_()




if __name__ == "__main__":
    # record_for_duration("_back", "_male_skinny", 20)
    record_button_click()
    # plt.ion()  # for interactive mode
    # while True:
        # raw_sensor_values = read_serial_data(arduino_port)
    #     matrix = parse_sensor_values(raw_sensor_values)
    #     print(raw_sensor_values)
    #     print(matrix)
    #     plt.imshow(matrix, cmap='hot', interpolation='nearest')
    #     plt.show()
    #     #
