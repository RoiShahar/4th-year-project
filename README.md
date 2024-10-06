# 🛏️ Smart Mattress: Sleep Position Monitoring System
A real-time monitoring solution designed to help users improve their sleeping posture and quality. 
The Smart Mattress monitors sleeping positions using force-sensitive resistors (FSRs) connected to 
an Arduino, sending data for analysis using a pre-trained neural network.

<!-- cool project cover image -->
![Project Cover Image](/media/project-cover-img.jpg)

<!-- table of content -->
## Table of Contents
- [The Team](#the-team)
- [Project Description](#project-description)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installing](#installing)
- [Testing](#testing)
- [Deployment](#deployment)
- [Built With](#built-with)
- [Acknowledgments](#acknowledgments)

## 👥 The Team 
*Team Members*
- [Roi Shahar](roi.shahar@mail.huji.ac.il)
- [Nir Rotem](nir.rotem2@mail.huji.ac.il)

*Mentor*
- [Qusay Muzaffar](qusay.muzaffar@mail.huji.ac.il)


## 📚 Project Description
The Smart Mattress aims to solve the challenge of monitoring and improving sleeping posture, especially 
in environments where constant supervision isn't available, like nursing homes or private homes.

### Features
- **Real-time Data Collection:** FSR sensors embedded in a mattress surface collect data on body position.
- **Data Analysis with Machine Learning:** A neural network model predicts sleeping positions and potential
  health risks.
- **User-Friendly Interface:** Visualizes sleep posture in real-time, including a heatmap of pressure points.

### Components
- **Hardware:** Arduino Mega 2560, FSR406 sensors, power supply.
- **Software:** Python for data analysis and visualization, Arduino code for sampling, and a neural network
  model for sleep posture detection.

### Technologies Used
- **Hardware:** Arduino Mega 2560, Force Sensitive Resistors (FSR406).
- **Programming Languages:** Python, C++ (Arduino IDE).
- **Machine Learning:** PyTorch library for training the neural network.
- **Web Framework:** Flask for the user interface.

## ⚡ Getting Started

Follow these instructions to set up and run the Smart Mattress system locally.

### 🧱 Prerequisites
- [Arduino IDE](https://www.arduino.cc/en/software) - for verifing the correct COM port for the connected Arduino, and for flashing the Arduino with the sampling code if needed.
- [Python 3.8+](https://www.python.org/downloads/) - for running backend services.
- Pandas, NumPy, PyTorch, Flask - Python libraries used in the project.

### 🏗️ Installing
1. Clone repository:

       git clone https://github.com/RoiShahar/4th-year-project/
   
2. Physically Position the Mattress Sensors:
   - The Arduino is connected to 16 FSR406 sensors, which must be positioned in a specific layout on the mattress.
   - Use the following reference diagram to place the sensors correctly:
   
   - Make sure each sensor is securely fixed in the correct location, and that the connection wires are properly routed to the Arduino, ensuring there is no movement during testing.


3. Connect the Arduino to the Computer:
   - Connect the Arduino Mega 2560, which is already attached to the sensors, to the computer via USB.

4. Verify COM Port in Arduino IDE:
   - Open the Arduino IDE on the computer.
   - Go to **Tools > Port** and note the COM number assigned to the Arduino (e.g., COM3, COM4, etc.).
   - Make sure that the Arduino is powered on and successfully recognized by the computer.

5. Set the Correct COM Port in the Python Code:
   - Navigate to the cloned repository directory and open the main.py file in a code editor.
   - Locate the line where the COM port is defined for connecting to the Arduino.
   - Update the COM port to match the one you identified in Arduino IDE:
     
         arduino_port = 'COMX' # Change it according to your current Arduino COM input

6. Update the Neural Network Model Path:
   - Open the predict_smart_mattress.py file.
   - Locate the main function where the model path (model_path) is defined.
   - Update the model_path to point to the correct location of the neural network model in the cloned repository:

         model_path = 'C:/YOUR_CLONED_REPOSITORY_PATH/smart_mattress_model.pth'


End with an example of getting some data out of the system or using it
for a little demo

## 🧪 Testing
Explain how to run tests for this project

### Sample Tests
Explain what these tests test and why

    Give an example

## 🚀 Deployment
Add additional notes on how to deploy this on a live system

## ⚙️ Built With
  - [Based on the amazing work of reserch group xxxx](https://www.example.com)
  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose the license


## 🙏 Acknowledgments
  - Hat tip to anyone whose code is used
  - Inspiration
  - etc
