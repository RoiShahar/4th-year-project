import pandas as pd
import os

"""
with a given path of the recorded samples, concatenate all the CSV tables to
a merged CSV file (that contains all the data of the files)
"""
def merge_csvs_to_dataset(path):
    folder_path = path
    file_names = [path+"/"+f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    combined_csv = pd.concat([pd.read_csv(f) for f in file_names])
    combined_csv.drop_duplicates(inplace=True)  # drop duplicates (if needed)
    combined_csv.to_csv(path+"/"+"merged_data.csv", index=False)

if __name__ == "__main__":
    merge_csvs_to_dataset("C:/Users/Roi_Shahar/Desktop/לימודים/סמסטר ח/data_fro_proj/official recordings/16-7-24/validation")