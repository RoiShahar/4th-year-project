import serial
import datetime
import pandas as pd
import time
import interpulation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import predict_smart_mattress

###############################################################################
# This is the main file that contains most of the app functionality, containing
# the port readings, parsing, data recording and prediction.
###############################################################################

arduino_port = 'COM4' # Change it according to your current Arduino COM input
baud_rate = 9600

"""
Read the serial data from the port in which the Arduino is connected to.
"""
def read_serial_data(serial_port):
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        ser.flush()
        lines = []
        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "---":
                break
            lines.append(line)
        # print(lines)
        return lines

"""
FOR TRAIN DATA RECORDINGS
Parse the raw data of the sensors (that was transmitted via the USB from the
Arduino) into a vector of values, and the recorded pre-known position.
"""
def parse_sensor_values(sensor_values, position):
    vector = np.zeros((1, 17), dtype=int)
    for i in range(len(sensor_values)):
        val = sensor_values[i]
        pin_number = i
        vector[0, pin_number] = int(val)
    vector[0,16] = position
    return vector

"""
FOR PREDICTION DATA RECORDINGS
Parse the raw data of the sensors (that was transmitted via the USB from the
Arduino) into a vector of values.
"""
def parse_sensor_values_for_prediction(sensor_values):
    vector = np.zeros((1, 16), dtype=int)
    for i in range(len(sensor_values)):
        val = sensor_values[i]
        pin_number = i
        vector[0, pin_number] = int(val)
    return vector

"""
FOR TRAIN DATA RECORDING
With a given recorded raw data, position, and characteristics, saves the data
in the required path.
"""
def save_sensor_data(kind, carateristics, data_matrices, duration): # duration time in seconds
    dfs = [pd.DataFrame(matrix) for matrix in data_matrices]
    result_df = pd.concat(dfs, ignore_index=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}__{kind}__{carateristics}__{duration}sec"

    # TODO: replace with your required path for saving the data
    result_df.to_csv(f"C:/Users/Roi_Shahar/Desktop/לימודים/סמסטר ח/data_fro_proj/official recordings/{filename}.csv", index=False)

"""
FOR TRAIN DATA RECORDING
With a given duration (in seconds), the characteristics of the sampled person,
 and the sampled position, records the data from the sensors  for that duration,
and save it locally on the workstation.
"""
def record_for_duration(kind, characteristics, duration_seconds, position):
    start_time = time.time()  # Get the current time
    end_time = start_time + duration_seconds
    matrices = []
    while time.time() < end_time:
        raw_sensor_values = read_serial_data(arduino_port)
        matrix = parse_sensor_values(raw_sensor_values, position)
        matrices.append(matrix)
    save_sensor_data(kind, characteristics, matrices, duration_seconds)
    print("Done successfully")

"""
For maintenance usage, with a given matrix of values (after parsing the raw
data), prints a heatmap of the matrix.
"""
def plot_heat_map(matrix):
    # Plot the heat map
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, cmap='viridis', cbar_kws={'label': 'Normalized Pressure'})
    plt.title('Heat Map of Pressure Distribution')
    plt.xlabel('Matrix Columns')
    plt.ylabel('Matrix Rows')
    plt.show()
    # print(matrix)

"""
FOR MODELS THAT USES INTERPOLATION ONLY! (256vals vector input)
Record one interval of the sensors samples, interpolate the data
and predict the position of the recorded sample.
"""
def record_one_sample_and_calculate():
    raw_sensor_values = read_serial_data(arduino_port)
    raw_values = parse_sensor_values_for_prediction(raw_sensor_values)

    matrix = interpulation.vector_to_matrix(raw_values[0])
    interpolated_matrix = interpulation.interpulate_matrix(matrix)
    interpolated_matrix_as_vector = np.reshape(interpolated_matrix, 256)
    prediction = predict_smart_mattress.main(interpolated_matrix_as_vector)

    return interpolated_matrix, prediction

"""
FOR MODELS THAT DOESN'T USE INTERPOLATION! (16vals vector input)
Record one interval of the sensors samples and predict the position of the
recorded sample.
"""
def record_one_sample_and_calculate_without_interpolation():
    # prediction for the raw 16 vars input vector
    raw_sensor_values = read_serial_data(arduino_port)
    raw_values = parse_sensor_values_for_prediction(raw_sensor_values)
    prediction = predict_smart_mattress.main(raw_values)

    # interpolation for visual display only:
    matrix = interpulation.vector_to_matrix(raw_values[0])
    interpolated_matrix = interpulation.interpulate_matrix(matrix)

    return interpolated_matrix, prediction