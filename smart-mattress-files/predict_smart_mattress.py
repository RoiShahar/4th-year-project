import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import interpulation

###############################################################################
# This file contains all the relevant Functionality for the neural network
# loading process (with a given pre-trained neural network weights file), and
# the prediction process of the network.
###############################################################################
"""
Defining the neural network architecture.
"""
class SmartMattressNet(nn.Module):
    def __init__(self, units_1, units_2, units_3, dropout_1, dropout_2, dropout_3):
        super(SmartMattressNet, self).__init__()
        self.fc1 = nn.Linear(256, units_1)
        self.bn1 = nn.BatchNorm1d(units_1)
        self.dropout1 = nn.Dropout(dropout_1)

        self.fc2 = nn.Linear(units_1, units_2)
        self.bn2 = nn.BatchNorm1d(units_2)
        self.dropout2 = nn.Dropout(dropout_2)

        self.fc3 = nn.Linear(units_2, units_3)
        self.bn3 = nn.BatchNorm1d(units_3)
        self.dropout3 = nn.Dropout(dropout_3)

        self.fc4 = nn.Linear(units_3, 6)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)
        x = self.fc4(x)
        return F.log_softmax(x, dim=1)


"""
Loading the pre-trained model from local
"""
def load_model(model_path, params):
    model = SmartMattressNet(**params)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

"""
Pre-processing the input
"""
def preprocess_input(input_vector, scaler_path):
    scaler = StandardScaler()
    scaler.mean_ = np.load(scaler_path + '_mean.npy')
    scaler.scale_ = np.load(scaler_path + '_scale.npy')
    scaler.n_features_in_ = scaler.mean_.shape[0]
    input_vector = scaler.transform([input_vector])
    return torch.tensor(input_vector, dtype=torch.float32)

"""
Predict function
"""
def predict(model, input_vector):
    with torch.no_grad():
        output = model(input_vector)
    prediction = output.argmax(dim=1).item()
    return prediction

"""
Main function to load the model and make a prediction
"""
def main(input_vector):
    model_path = 'C:/final_proj_model/smart_mattress_model.pth'
    scaler_path = 'scaler'

    params = {
        'units_1': 320,
        'units_2': 256,
        'units_3': 64,
        'dropout_1': 0.3,
        'dropout_2': 0.2,
        'dropout_3': 0.5,
    }

    model = load_model(model_path, params)
    input_tensor = preprocess_input(input_vector, scaler_path)
    return predict(model, input_tensor)

"""
Save the scaler's mean and scale values
"""
def preprocess_data_for_scaler(file_path):
    raw_data = pd.read_csv(file_path)
    raw_data.drop(index=0, inplace=True)  # Remove the first row which is the indexes
    X = raw_data.iloc[:, :-1].values  # First 256 columns as features
    return X
