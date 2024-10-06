import numpy as np
import pandas as pd
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import seaborn as sns

###############################################################################
# This file contains all the necessary functionality for the data interpolation
# process (for both neural network training and visualization).
###############################################################################

TAGGED_INTERPOLATED_VECTOR_SIZE = 257

"""
With a given 4x4 matrix, apply cubic interpolation to the matrix and return the
interpolated matrix.
"""
def interpulate_matrix(matrix):
    x_values = np.arange(4)  # X coordinates
    y_values = np.arange(4)  # Y coordinates
    data_values = matrix

    # Create a cubic interpolation function
    interp_func = interp2d(x_values, y_values, data_values, kind='cubic')

    # New grid for interpolated values (16x16)
    new_x_values = np.linspace(0, 3, 16)
    new_y_values = np.linspace(0, 3, 16)

    # Evaluate the interpolated function at the new grid points
    interpolated_matrix = interp_func(new_x_values, new_y_values)
    return interpolated_matrix

"""
With a given raw data vector (with the size of 16), transform it to a 4x4 
matrix, base on our physical sensors matrix.
"""
def vector_to_matrix(vector):
    # Initialize a 4x4 matrix
    matrix = np.zeros((4, 4))

    # Fill the matrix according to the specified structure
    matrix[0, 0] = vector[0]
    matrix[0, 1] = vector[1]
    matrix[1, 0] = vector[2]
    matrix[1, 1] = vector[3]
    matrix[0, 2] = vector[4]
    matrix[0, 3] = vector[5]
    matrix[1, 2] = vector[6]
    matrix[1, 3] = vector[7]
    matrix[2, 2] = vector[8]
    matrix[2, 3] = vector[9]
    matrix[3, 2] = vector[10]
    matrix[3, 3] = vector[11]
    matrix[2, 0] = vector[12]
    matrix[2, 1] = vector[13]
    matrix[3, 0] = vector[14]
    matrix[3, 1] = vector[15]

    return matrix

"""
The main Function. with a given source and destination paths and file name,
takes the source table of 16 vals vectors, interpolated each one to a 256 vals
vector, and saves it to a new CSV file.
"""
def create_interpolated_data_from_recordings(source_data_path, destanation_path, destenation_file_name):
    records_csv = pd.read_csv(source_data_path)
    interpulated_matrix = np.empty((0, TAGGED_INTERPOLATED_VECTOR_SIZE))
    for i in range(1, records_csv.shape[0]):
        cur_record = records_csv.iloc[i]
        tagged_class = cur_record[-1]
        raw_mat = vector_to_matrix(cur_record[:16])
        interpulated_mat = interpulate_matrix(raw_mat)
        interpulated_vector = np.reshape(interpulated_mat, 256)
        interpulated_vector = np.append(interpulated_vector, tagged_class)
        interpulated_matrix = np.vstack((interpulated_matrix, interpulated_vector))

    save_matrix_to_csv(interpulated_matrix, destanation_path, destenation_file_name)
    return interpulated_matrix

"""
Saves the data to a CSV file.
"""
def save_matrix_to_csv(matrix, destanation_path, destenation_file_name):
    df = pd.DataFrame(matrix)
    df.to_csv(destanation_path + "/" + destenation_file_name + ".csv", index=False)

"""
For maintenance usage, plots the matrix heatmap.
"""
def plot_heat_map(matrix):
    # Normalize the matrix values
    norm_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
    # Plot the heat map
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=False, cmap='viridis', cbar_kws={'label': 'Detected Pressure (o to 1023 scale)'})
    plt.title('Interpolated Heat Map of Pressure Distribution, male, 1.71m, left side')
    plt.xlabel('Matrix Columns')
    plt.ylabel('Matrix Rows')
    plt.show()
    # print(matrix)

"""
Running the interpolation process over the pre-interpolated data.
"""
# NOTE: change the paths and thr filename to your requested locations and names
if __name__ == "__main__":
    source_file = "C:/Users/Roi_Shahar/Desktop/לימודים/סמסטר ח/data_fro_proj/official recordings/16-7-24/validation/merged_data.csv"
    destenation_path = "C:/Users/Roi_Shahar/Desktop/לימודים/סמסטר ח/data_fro_proj/official recordings/16-7-24/validation"
    file_name = "merged_interpolated_train_data_full"
    create_interpolated_data_from_recordings(source_file, destenation_path, file_name)