# NYBWD

BCT Minor project Kathmandu Engineering College. Flask API to control vehicle and interface with UI.

## Setup
- Enable VNC, SSH, REMOTE GPIO etc, I dont remember all XD
- Setup Samba server for seamless conncetion with vscode **Remote Connection** Extensiono
- Install all the requirements from **requirements.txt**
- Enable access to Ports eg. tty
- Run **app.py** inside the venv
- For video feed run **test/camera.py** in separate terminal
- Default port is 9000 for the API
- If problems occours, other hardware configuration might be needed


## Problems
1. GPS based autonomous part not completed
1. Should run **test/proximity.py** for the proximity of main app to work. This should not be necessary as the main app itself have this function but for the proximity of main app to work this exatra code should be run in separate terminal (weird)


