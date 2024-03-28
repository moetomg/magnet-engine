# Magnet Engine
![GitHub repo size](https://img.shields.io/github/repo-size/moetomg/magnet-engine)
![GitHub top language](https://img.shields.io/github/languages/top/moetomg/magnet-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub last commit](https://img.shields.io/github/last-commit/moetomg/magnet-engine)

Welcome to the Magnetic Core Loss Modeling Web-Based GUI project! This project provides a user-friendly graphical user interface (GUI) for modeling magnetic core losses in power electronics. The underlying model is based on the IEEE PELS-Google-Enphase-Princeton [MagNet Challenge 2023](https://github.com/minjiechen/magnetchallenge/tree/main) competition models. The website is currently deployed at [Magnet Engine](https://magnet-engine-dfprepz3gq-ts.a.run.app) and maintained by The University of Sydney. 

<img src="icons/mclogo.jpg" width="1000">

## Features

- Customizable Parameters: Users can adjust various parameters (excitation waveform, operating frequency and temperature) to simulate different scenarios and analyze the impact of a periodic signal on core losses.
- Web-Based: Accessible through web browsers, eliminating the need for installation and providing convenience for users.
- Diverse Materials: Support up to 15 ferrites - 77, 78, 79, N27, N30, N49, N87, 3E6, 3F4, T37, 3C90, 3C92, 3C92, 3C94, ML95S

## GUI Usage 
- Access the GUI: Visit [MagNet Engine] in your web browser.
- Select Model: Choose the model and targed material in the sidebar. 
- Input Parameters: Enter the required excitation and operating parameters into the designated fields. 
- View Results: Once the simulation is complete, visualizations and relevant data will be displayed on the interface.
- Analysis and Export: Analyze the results and export data if necessary for further processing.

## Model Usage 
To test the model, clone the responsitory locally and excute the following code:
```r
import os
import numpy as np
from magnet-engine.[team] import [team]Model
# Select model
material="3C92"

# open magnet-engine as the working dir
mdl_path = "./[team]/models/"+material+".pt"

# instantiate material-specific model
mdl = SydneyModel(mdl_path, material="3C92")

# single cycle B excitation
t = np.linspace(0, 1, [resolution]) 
B = 0.1*np.sin((360*t+90*np.pi/180)
p,h = mdl(B,['frequency'],['temperature'])
```
Replace
- [team] with the name of university. (e.g., Sydney)
- [resolution] with the require steps for each model. (128 for Sydney, 1024 for Panderborn)
- ['frequency'] with the operating frequency in Hz. (50-450e3 Hz)
- ['temperature'] with the operating temperature in °C.

## Installation 
There is no installation required for this web-based GUI. Simply access it through your web browser using the provided link.

## License 
This project is licensed under the [MIT License](https://opensource.org/license/mit).

## Acknowledgements
- This project utilizes the Magnet Challenge 2023 competition model.
- We thank the power electronics community for their invaluable contributions to the libraries and tools used in this project.

## Contact
For any inquiries or support, please contact sinan.li@sydney.edu.au

## Other avaliable tools

- [MagNet Open Database](https://www.princeton.edu/~minjie/magnet.html) - maintained by Princeton University
- [MagNet-AI Platform](https://mag-net.princeton.edu/) - maintained by Princeton University
- [MagNet Toolkit](https://github.com/upb-lea/mag-net-hub) - maintained by Paderborn University

## Collaboration 
We're always open to collaborating with anyone interesting in this project. If you would like to display your model in "magnet-engine", please follow the steps below to set up your model. This will helps us better integrate your models into the "magnet-engine" GUI.

1. Define your model as a <ins>class</ins> in a .py file, naming it [team]Model (e.g., SydneyModel in Sydney.py file)
2. The class should have a constructor and can be invoked as a function. 
```r
class SydneyModel:
  # Initialized with the path of the well-trained model and targeted model 
  def __init__(self, mdl_path, material):
     """
     Parameters:
      - mdl_path: the path to the trained model file
      - material: target material name (e.g., 77, 78, 79)
    """
    pass
  def __call__(self, data_B, data_F, data_T, return_h_sequence=True):
    """
     Parameters:
      - data_B: the flux density sequence in nd.array format
      - data_F: the operating frequency in list (one set prediction)/ nd.array (one batch prediction)
      - data_T: the operating temperature in list (one set prediction)/ nd.array (one batch prediction)
      - return_h_sequence: a boolean variable tell whether the function return H sequence (optional)
    """
    pass
```
3. Name the trained model file with the name of the corresponding material, and place all files in a folder named "models".
- Main Folder
  - Sydney.py
  - models
    - 77
    - 78
    - ...
4. Make sure each of your models runs correctly.
5. Finally, zip your folder, or upload it to a public github responsitory.

For more details, please refer to the model definition in this responsitory. If you have any questions or are interested in cooperation, please feel free to contact us. 
