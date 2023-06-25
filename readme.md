## GAMEBOX 3 IN 1: TICTACTOE, SEABATTLE, MINESWEEPER

TICTACTOE
First move is determind randomly. Collect 3 crosses in a row or diagonal to win.

SEABATTLE
Spep-by-step game. Destroy the enemy fleet before he destroys yours.
There are 1 cruiser, 2 destroyers, 3 frigates, 4 corvettes on battlefield.
Ships move randomly one space according to their direction after each round.
Damaged ship stop moving and marked red. Dead ship marked black.
Also you can choose enemy IQ 70 or 90.

MINESWEEPER
There are 10 mines on the field. Number in cell shows number of mines around cell.
Mark potential mine location with right click. Open all free cells to win.


*To build EXE file*:

**create venv with name 'venv':**  
py -m venv venv  
**activate venv**:  
venv/scripts/activate  
**install requirements:**  
pip install -r requirements  
**change DEV variable in config.py to False:**  
DEV = False  
**run build.bat file in terminal to build app.exe:**  
./build.bat  

*build.bat command*:

pyinstaller -w -F -i icon.ico 
--add-data "./venv/Lib/site-packages/customtkinter;customtkinter/" 
--add-data "icon.ico;." 
--add-data "minesweeper.ico;." 
--add-data "tictactoe.ico;." 
--add-data "seabattle.ico;." 
app.py

Look for app.exe in /dist directory.

***Enjoy it!***