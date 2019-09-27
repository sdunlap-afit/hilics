# Overview
The purpose of this project is automatic generation of nameplates for the Hardware-in-the-loop Industrial Control System training kit. The project uses Python and OpenSCAD to generate the models.

<img src="../../../docs/images/nameplate.png"  height="200">

# Installation
## OpenSCAD
### Download
  * http://www.openscad.org/downloads.html
  * For Windows: grab the exe installer to make it easier to install
### Install
  * Run the installation program
  * Add the OpenSCAD program to your PATH environment variable
## Python
### Download
  * https://www.python.org/downloads/
  * Get Python 3.7 
### Install
  * Run the installer
    * Make sure the Add to PATH option is selected.  Otherwise you will need to manually add Python to your PATH environment variable.
  * Open a command line interface (CLI)
    * On Windows run cmd.exe or powershell as administrator
    * Run the following commands:
      ```bash
      pip install -U pip
      pip install pipenv
      ```
## Fonts
  * Find fonts in the fonts directory
  * Select the font files, right-click and select Install
## Project
  * Once OpenSCAD and Python are installed you can setup the project.
  * Open a CLI in the project workspace.
  * Use pipenv to install the necessary libraries
    * pipenv installs libraries according to the Pipfile
    ```bash
    pipenv install
    ```
# Running
## Configuration
There is a configuration section at the top of `nameplates.py`. You can configure how many ids make, rough size of the nameplate, and the text and font.
## Run the script
You can run the python script in the development environment of your choice.  Or you can run the script with the following CLI command.  `pipenv shell` activates the python virtual environment used by the `nameplates.py` script.
```bash
pipenv shell
python nameplates.py
```
