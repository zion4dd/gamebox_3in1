@REM # create venv with name 'venv':
@REM py -m venv venv

@REM # activate venv:
@REM venv/scripts/activate

@REM # install requirements:
@REM pip install -r requirements

@REM # change DEV variable in config.py to False
@REM DEV = False

@REM # run this file in terminal to build app.exe:
@REM ./build

pyinstaller -w -F -i icon.ico ^
--add-data "./venv/Lib/site-packages/customtkinter;customtkinter/" ^
--add-data "icon.ico;." ^
--add-data "minesweeper.ico;." ^
--add-data "tictactoe.ico;." ^
--add-data "seabattle.ico;." ^
app.py

@REM -w --windowed --- Do not provide a console window for standard i/o.
@REM -F --onefile / -D --onedir
@REM -i icon.ico
@REM --add-data "SRC;DEST" --- This option can be used multiple times.

