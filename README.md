# Construction Site's Camera Placement Optimization

This repository contains code for optimizing the placement of cameras on a construction site, based on a map divided into different phases. The process involves converting a site map into a colored map indicating various zones, running a python code for specifying camera specifications, and using IBM ILOG Cplex Optimization Studio to solve a mathematical model for optimal camera placement. Lastly representing results of the solver to see placement of cameras on the given map and phase.

## Description

The project workflow is as follows:

1. Map Preparation:
    - Convert the site map photo (.png) into a map with six colors:
        - Blue: (possible) Camera installation points
        - Black: Points where visibility is blocked
        - Red: High-risk or high-importance points
        - Orange: Medium-risk or medium-importance points
        - Yellow: Low-risk or low-importance points
        - White: Harmless or unimportant points

2. Run the DataConversion.py:
    - Execute DataConversion.py.
    - Input the following specifications when prompted:
        - C = Purchase cost of each camera
        - CR = Coverage desired by the project manager
        - distance = Camera view distance
        - AOV = Angle of view of the camera
        - number of phases = Number of phases considered for camera optimization
    - Enter the address of photo of each phase.

3. Animation:
    - An animation displays the coverage area of the candidate cameras at each installation point.

4. Data Conversion:
    - After processing all phases, save the data, primarily a .dat file named opl.dat will be created.

5. Optimization:
    - Open IBM ILOG Cplex Optimization Studio and load the mathematical model.
    - Enter the contents of opl.dat in the data section.
    - Run the solver of the model to generate a two-dimensional matrix representing candidate points and phases.

6. Visualization:
    - Run Visualization.py.
    - Enter the solution matrix from IBM.
    - View the schematic arrangement of cameras for each phase.

## Files

### Code
- DataConversion.py: A python script for entering camera specifications, candidate camera installation ponints and phase maps.
- OplModel.mod: Opl optimization model.
- Visualization.py: Script for visualizing the camera arrangement based on the solution matrix.
- Visualization Utility scripts: findDic.py, Categorized_Value_1.py

### Data
- opl.dat: Data file generated for optimization.
- map pictures (.png): plan of each phase.

### Other
- README.md: Project description and instructions (this file).
- *.json files: generated data.

## Getting Started

### Prerequisites

- Python 3.x
- IBM ILOG Cplex Optimization Studio
- requirements.txt


### Installation

1. Clone the repository:
        git clone https://github.com/smartconstructiongroup/Camera_Placement_Optimization.git
    
2. Navigate to the project directory:
        cd Farkhonde-CameraPlacementOptimization
    
3. Install the required Python packages:
        pip install -r requirements.txt


### Usage

1. Run the DataConversion for camera specifications and map processing:
        python DataConversion.py

2. Follow the prompts and upload the phase maps.
3. After generating opl.dat, open IBM ILOG Cplex Optimization Studio and solve the model which is in OplModel.mod
4. Run the visualization script:
        python Visualization.py
    
5. Enter the solution matrix to view the camera arrangement schematic.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---
