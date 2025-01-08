# Magnet Engine
![GitHub repo size](https://img.shields.io/github/repo-size/moetomg/magnet-engine)
![GitHub top language](https://img.shields.io/github/languages/top/moetomg/magnet-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub last commit](https://img.shields.io/github/last-commit/moetomg/magnet-engine)

Welcome to the Magnet Engine! This GUI platform offers a comprehensive and user-friendly interface for modeling magnetic core losses in power electronic applications. Designed to assist engineers, researchers, and professionals, the GUI simplifies the process of simulating and analyzing core losses, enhancing both the design and optimization of power electronics systems.

## About the Project
This project utilizes state-of-the-art modeling techniques based on the models developed for the IEEE PELS-Google-Enphase-Princeton [MagNet Challenge 2023](https://github.com/minjiechen/magnetchallenge/tree/main). Our goal is to provide an accessible, web-based tool that empowers users to explore and apply advanced core loss models in a straightforward and effective manner.

The platform is currently deployed at: https://magnet-engine-app.sydney.edu.au/ and is actively maintained by The University of Sydney. Our team is committed to continuous improvement, regularly updating the tool to incorporate the latest research findings and industry best practices.

<img src="icons/mclogo.jpg" width="1000">

## Features

- Customizable Parameters: Users can adjust various parameters (excitation waveform, operating frequency and temperature) to simulate different scenarios and analyze the impact of a periodic signal on core losses.
- Web-Based: Accessible through web browsers, eliminating the need for installation and providing convenience for users.
- Diverse Materials: Support up to 15 ferrites - 77, 78, 79, N27, N30, N49, N87, 3E6, 3F4, T37, 3C90, 3C92, 3C92, 3C94, ML95S
- MagNet Toolkit package integrated: https://github.com/upb-lea/mag-net-hub

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
from .\src\[team] import [team]
# Select model
material="3C92"

# open magnet-engine as the working dir
mdl_path = "./src/[team]/models/"+material+".pt"

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

## Collaboration 
We're always open to collaborating with anyone interesting in this project. If you would like to display your model in "**magnet-engine**", please follow these steps:

1. **Submit a Pull Request to MagNet Toolkit**

Add your model to the [MagNet Toolkit](https://github.com/upb-lea/mag-net-hub) repository by creating a pull request. Ensure your model and associated files follow the repository's contribution guidelines.

2. **Notify Us**

After your pull request has been merged in the MagNet Toolkit repository, please notify the editors of this repository. We will update the necessary files to display the new model in the "magnet-engine" GUI. 

### **Additional Notes**
The `team` folder in this repository is a duplicate of the structure in the MagNet Toolkit. It is intended solely for displaying model structures and will not be used in the final GUI. However, it can serve as a reference or be used by users to test models locally.

Feel free to contact us if you have any questions or require assistance during the process.
## Local Installation
To run the project locally, follow these steps:
1. Build the Docker containers:
```
docker-compose build
```
2. Start the Docker containers:
```
docker-compose up
```
3. Once the containers are running, open your web browser and navigate to: http://localhost:8080

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

## Project Reference Papers

- Q. Huang, Y. Li, J. Zhu and S. Li, "Magnetization Mechanism-Inspired Neural Networks for Core Loss Estimation," in IEEE Transactions on Power Electronics, doi: 10.1109/TPEL.2024.3450897. [Paper] (https://ieeexplore.ieee.org/document/10654567)
- Förster, Nikolas, Wilhelm Kirchgässner, Till Piepenbrock, Oliver Schweins, and Oliver Wallscheid. "HARDCORE: H-field and power loss estimation for arbitrary waveforms with residual, dilated convolutional neural networks in ferrite cores." arXiv preprint arXiv:2401.11488 (2024). [Paper] (https://arxiv.org/abs/2401.11488)


